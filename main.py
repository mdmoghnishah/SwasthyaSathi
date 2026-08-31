"""
SwasthyaSathi — voice-first protocol navigation copilot for last-mile
health workers.

IMPORTANT SAFETY FRAMING: this app does NOT diagnose or prescribe treatment.
It retrieves an approved protocol chunk relevant to what the worker
describes, and asks the LLM to explain that protocol clearly and flag
whether escalation is needed -- grounded strictly in the retrieved text.
If nothing relevant is found, or a danger sign is present, it defaults to
recommending escalation to a qualified healthcare professional.
"""

import json
import os
import tempfile

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sarvamai import SarvamAI

from retriever import retrieve_protocol

load_dotenv()

SARVAM_API_KEY = os.environ["SARVAM_API_KEY"]
CHAT_MODEL = os.environ.get("SARVAM_CHAT_MODEL", "sarvam-105b-conversations")
TTS_SPEAKER = os.environ.get("TTS_SPEAKER", "shubh")
TTS_LANGUAGE_CODE = os.environ.get("TTS_LANGUAGE_CODE", "hi-IN")

client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

app = FastAPI(title="SwasthyaSathi")

# Loosen CORS for hackathon demo purposes only.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryResponse(BaseModel):
    transcript: str
    protocol_title: str
    protocol_source: str
    match_score: float
    urgency: str
    protocol_reference: str
    guidance: str
    reason: str
    questions: list[str]
    audio_base64: str


SYSTEM_PROMPT = """You are SwasthyaSathi, a protocol-navigation assistant \
for a community health worker in the field. You are NOT a doctor. You do \
NOT diagnose conditions or prescribe medication or dosages.

You will be given ONE retrieved, approved protocol chunk and a worker's \
spoken description of a case.

Rules:
- Base your response ONLY on the given protocol text. Never add medical \
facts, drug names, or dosages that are not in it.
- If the worker's description does not clearly match the protocol, say so \
in "reason" and set urgency to "Refer soon" or higher -- when in doubt, \
recommend escalation to a qualified healthcare professional rather than \
guessing.
- Respond with ONLY a single JSON object, no other text, in exactly this \
shape:
{
  "urgency": "Routine" | "Monitor at home" | "Refer soon" | "Refer immediately",
  "protocol_reference": "<short name of the matched protocol>",
  "guidance": "<one or two calm, plain-language sentences telling the worker what to do next>",
  "reason": "<one short sentence on why, referencing the matched symptoms>",
  "questions": ["<optional follow-up question the worker could ask the family, if useful>"]
}
- Keep language simple and calm. No medical jargon. "questions" can be an \
empty list if none are needed.
"""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
async def query(audio: UploadFile = File(...)):
    # 1. Save uploaded audio to a temp file (Sarvam SDK wants a file handle/path)
    suffix = os.path.splitext(audio.filename or "")[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    try:
        # 2. Speech-to-text (Saaras v3, auto language detection, same-language transcript)
        audio_size_bytes = os.path.getsize(tmp_path)
        print(f"[DEBUG] Received audio file: {audio_size_bytes} bytes, saved at {tmp_path}")

        with open(tmp_path, "rb") as f:
            stt_response = client.speech_to_text.transcribe(
                file=f,
                model="saaras:v3",
                mode="transcribe",
            )
        print(f"[DEBUG] Raw Saaras response: {stt_response}")

        transcript = stt_response.transcript
        if not transcript or not transcript.strip():
            raise HTTPException(
                status_code=422,
                detail=(
                    "Could not transcribe audio. Try holding the record button "
                    "longer and speaking clearly right after it starts."
                ),
            )

        # 3. Retrieve the closest matching approved protocol from Pinecone
        matches = retrieve_protocol(transcript, top_k=1)
        if not matches:
            raise HTTPException(status_code=404, detail="No matching protocol found.")
        top_match = matches[0]

        # 4. Ask the chat model for a structured, grounded, escalation-aware response
        user_message = (
            f'Worker\'s description: "{transcript}"\n\n'
            f"Retrieved protocol ({top_match['title']}):\n{top_match['text']}"
        )
        chat_response = client.chat.completions(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            max_tokens=1500,
            temperature=0.2,
        )
        print(f"[DEBUG] Raw chat response: {chat_response}")

        raw_content = chat_response.choices[0].message.content
        if not raw_content or not raw_content.strip():
            finish_reason = getattr(chat_response.choices[0], "finish_reason", "unknown")
            raise HTTPException(
                status_code=502,
                detail=(
                    f"Chat model returned no content (finish_reason={finish_reason}). "
                    "Check backend logs for the full response."
                ),
            )
        raw_content = raw_content.strip()

        try:
            # Model may wrap JSON in a code fence despite instructions -- strip it if so.
            cleaned = raw_content.strip("` \n")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].strip()
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            # Fail safe: never invent structured fields -- surface the raw text
            # and default to the most cautious urgency level.
            parsed = {
                "urgency": "Refer soon",
                "protocol_reference": top_match["title"],
                "guidance": raw_content,
                "reason": "Could not parse a structured response; showing raw model output.",
                "questions": [],
            }

        # 5. Build a natural spoken sentence (not raw JSON) for Bulbul
        spoken_text = f"{parsed.get('urgency', '')}. {parsed.get('guidance', '')}"

        tts_response = client.text_to_speech.convert(
            text=spoken_text,
            language_code=TTS_LANGUAGE_CODE,
            model="bulbul:v3",
            speaker=TTS_SPEAKER,
        )
        audio_base64 = tts_response.audios[0]

        return QueryResponse(
            transcript=transcript,
            protocol_title=top_match["title"],
            protocol_source=top_match["source"],
            match_score=top_match["score"],
            urgency=parsed.get("urgency", "Refer soon"),
            protocol_reference=parsed.get("protocol_reference", top_match["title"]),
            guidance=parsed.get("guidance", ""),
            reason=parsed.get("reason", ""),
            questions=parsed.get("questions", []),
            audio_base64=audio_base64,
        )
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)