import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost"),
        "X-Title": os.getenv("OPENROUTER_APP_NAME", "Chatbot"),
    },
)

def _resolve_llama_model(name: str | None) -> str:
    # explicit -> env -> fallback
    model = (name or os.getenv("OPENROUTER_LLAMA_MODEL") or "meta-llama/llama-3.3-70b-instruct:free").strip()
    if not model:
        raise ValueError("LLaMA için model adı bulunamadı (OPENROUTER_LLAMA_MODEL boş).")
    return model

class LlamaChatbot:
    def __init__(self, model_name: str | None = None):
        self.model_name = _resolve_llama_model(model_name)

    def chat(self, messages: list) -> str:
        """
        OpenRouter üzerinden mesaj listesini LLaMA modeline gönderir.
        """
        resp = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        return (resp.choices[0].message.content or "").strip()