# 🩺 SwasthyaSathi

**A multilingual, voice-first protocol copilot that helps India's last-mile
health workers navigate approved health guidance and escalation pathways in
their own language, without searching through complex documents.**

Built for the **Build for India with Sarvam** challenge (Coding Ninjas 10X Club × Sarvam AI).

## What it does

A community health worker (e.g. an ASHA worker) speaks a case description
out loud, in her own language. The app:

1. Transcribes it (Saaras STT)
2. Retrieves the single closest-matching **approved protocol chunk** from a
   curated knowledge base (RAG via Pinecone)
3. Asks a Sarvam chat model to explain that protocol clearly, in a
   structured, safety-first format -- grounded *only* in the retrieved text
4. Speaks the guidance back (Bulbul TTS), in the worker's language

**Sarvam APIs used:**
- **Saaras v3** (Speech-to-Text)
- **Sarvam Chat Completions** (`sarvam-30b`)
- **Bulbul v3** (Text-to-Speech)

## ⚠️ Safety framing — read this before you demo

SwasthyaSathi is a **protocol-navigation and escalation assistant**, not a
diagnostic tool. It does not diagnose conditions or prescribe treatment. The
LLM is explicitly instructed to answer only from the retrieved protocol
text, and to default to recommending escalation to a qualified healthcare
professional whenever the case doesn't clearly match, or a danger sign is
present. Every response shows:
- the **matched protocol name and source**, for transparency
- an **urgency level** (Routine / Monitor at home / Refer soon / Refer immediately)
- the **reason** the model matched that protocol

`protocols_data.py` contains **simplified, illustrative** protocol summaries
written for this demo, clearly labeled as such — not verified official
medical guidance. State this explicitly in your project write-up.

## Setup

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

pip install -r requirements.txt

cp .env.example .env
# edit .env: SARVAM_API_KEY (dashboard.sarvam.ai), PINECONE_API_KEY (app.pinecone.io)

python ingest_protocols.py   # loads the protocol knowledge base into Pinecone, run once

python main.py   # starts backend at http://localhost:8000
```

## Try it

Open `test.html` in a browser (or serve it with `python -m http.server`).
Hold the button, describe a case, release, and see + hear the structured
guidance.

Test phrases (matching the 8 seeded protocols):
- "3 month old baby has fever and is not feeding"
- "my child has loose motions since morning, drinking water fine"
- "pregnant woman has swelling in her face and a bad headache"
- "newborn baby feels cold and won't feed"
- "child has cough and is breathing fast"
- "someone was bitten by a snake in the field"
- "elderly man suddenly can't speak properly and one side is weak"
- "child looks very thin, ribs showing"

## Project structure

```
swasthya-sathi/
├── main.py               # FastAPI app: STT -> retrieval -> structured chat -> TTS
├── retriever.py           # Pinecone query helper
├── ingest_protocols.py     # One-time script to embed + upsert protocols
├── protocols_data.py       # Sample protocol knowledge base (with sources)
├── test.html                # Minimal browser test/demo page
├── requirements.txt
└── .env.example
```

## For your submission

See `PROJECT_DESCRIPTION_DRAFT.md` for text ready to paste into your
required Google Doc.
