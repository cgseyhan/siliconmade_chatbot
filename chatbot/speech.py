import os
import tempfile
import uuid
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = None

def get_speech_client():
    global client
    if client is None:
        key = os.getenv("OPENAI_API_KEY") or "dummy"
        client = OpenAI(api_key=key)
    return client

def is_api_key_valid():
    key = os.getenv("OPENAI_API_KEY")
    return bool(key and key.strip() and key != "dummy")

def transcribe_audio_openai(file_bytes: bytes, filename: str) -> str:
    """
    Transcribes the uploaded audio file to text using Whisper-1, then deletes the temporary file.
    """
    if not is_api_key_valid():
        return "WARNING: OpenAI API Key is not configured for transcription."

    # Create temporary file
    suffix = os.path.splitext(filename)[1] or ".wav"
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as f:
            transcript = get_speech_client().audio.transcriptions.create(
                model="whisper-1",
                file=f,
            )
        return transcript.text.strip()
    except Exception as e:
        print(f"Error during audio transcription: {e}")
        return ""
    finally:
        # Clean up temporary file after processing
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

def synthesize_tts_openai(text: str, voice: str = "alloy") -> str:
    """
    Synthesizes speech from text using the OpenAI TTS-1 API.
    """
    if not is_api_key_valid():
        print("WARNING: OpenAI API Key is not configured for text-to-speech synthesis.")
        return ""

    try:
        out_path = os.path.join(tempfile.gettempdir(), f"tts_{uuid.uuid4().hex}.mp3")
        audio = get_speech_client().audio.speech.create(
            model="tts-1",
            voice=voice,       # alloy, echo, fable, onyx, nova, shimmer
            input=text,
        )
        with open(out_path, "wb") as f:
            f.write(audio.content)
        return out_path
    except Exception as e:
        print(f"Error during speech synthesis: {e}")
        return ""