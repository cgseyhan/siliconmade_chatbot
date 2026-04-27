import os
import tempfile
import uuid
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio_openai(file_bytes: bytes, filename: str) -> str:
    """
    Upload edilen ses dosyasını Whisper-1 ile metne çevirir ve ardından dosyayı siler.
    """
    # Geçici dosya yarat
    suffix = os.path.splitext(filename)[1] or ".wav"
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
            )
        return transcript.text.strip()
    finally:
        # İşlem bittiğinde dosyayı temizle
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

def synthesize_tts_openai(text: str, voice: str = "alloy") -> str:
    out_path = os.path.join(tempfile.gettempdir(), f"tts_{uuid.uuid4().hex}.mp3")
    audio = client.audio.speech.create(
        model="tts-1",     # alternatif: "gpt-4o-mini-tts" hesabında açıksa
        voice=voice,       # alloy, verse, coral, etc.
        input=text,
    )
    with open(out_path, "wb") as f:
        f.write(audio.content)
    return out_path