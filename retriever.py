import os
from functools import lru_cache

from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "swasthyasathi-protocols")
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedder() -> SentenceTransformer:
    return SentenceTransformer(EMBED_MODEL_NAME)


@lru_cache(maxsize=1)
def get_index():
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    return pc.Index(INDEX_NAME)


def retrieve_protocol(query_text: str, top_k: int = 1) -> list[dict]:
    """
    Embed the query and return the top-k matching protocol chunks as
    [{"title": ..., "text": ..., "source": ..., "score": ...}, ...]
    """
    embedder = get_embedder()
    index = get_index()

    query_vector = embedder.encode(query_text).tolist()
    result = index.query(vector=query_vector, top_k=top_k, include_metadata=True)

    matches = []
    for match in result.get("matches", []):
        meta = match.get("metadata", {})
        matches.append(
            {
                "title": meta.get("title", ""),
                "text": meta.get("text", ""),
                "source": meta.get("source", ""),
                "score": match.get("score", 0.0),
            }
        )
    return matches
