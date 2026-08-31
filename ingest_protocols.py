"""
Run this once to load protocols_data.py into Pinecone.

Usage:
    python ingest_protocols.py
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

from protocols_data import PROTOCOLS

load_dotenv()

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "swasthyasathi-protocols")

# Small, fast, good-enough embedding model for a hackathon demo.
# 384-dim output -> matches the index dimension created below.
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"


def main():
    print(f"Loading embedding model '{EMBED_MODEL_NAME}'...")
    embedder = SentenceTransformer(EMBED_MODEL_NAME)

    pc = Pinecone(api_key=PINECONE_API_KEY)

    existing = [idx["name"] for idx in pc.list_indexes()]
    if INDEX_NAME not in existing:
        print(f"Creating Pinecone index '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=embedder.get_sentence_embedding_dimension(),
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    index = pc.Index(INDEX_NAME)

    print(f"Embedding {len(PROTOCOLS)} protocol chunks...")
    vectors = []
    for p in PROTOCOLS:
        embedding = embedder.encode(p["text"]).tolist()
        vectors.append(
            {
                "id": p["id"],
                "values": embedding,
                "metadata": {
                    "title": p["title"],
                    "text": p["text"],
                    "source": p["source"],
                },
            }
        )

    print("Upserting into Pinecone...")
    index.upsert(vectors=vectors)
    print(f"Done. {len(vectors)} protocols indexed in '{INDEX_NAME}'.")


if __name__ == "__main__":
    main()
