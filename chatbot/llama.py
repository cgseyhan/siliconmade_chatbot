import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = None

def get_openrouter_client():
    global client
    if client is None:
        api_key = os.getenv("OPENROUTER_API_KEY") or "dummy"
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost"),
                "X-Title": os.getenv("OPENROUTER_APP_NAME", "Chatbot"),
            },
        )
    return client

def _resolve_llama_model(name: str | None) -> str:
    # explicit -> env -> fallback
    model = (name or os.getenv("OPENROUTER_LLAMA_MODEL") or "meta-llama/llama-3.3-70b-instruct:free").strip()
    if not model:
        raise ValueError("Model name for LLaMA could not be resolved (OPENROUTER_LLAMA_MODEL is empty).")
    return model

class LlamaChatbot:
    def __init__(self, model_name: str | None = None):
        self.model_name = _resolve_llama_model(model_name)

    def chat(self, messages: list) -> str:
        """
        Sends the list of messages to the LLaMA model via OpenRouter.
        """
        key = os.getenv("OPENROUTER_API_KEY")
        if not key or key == "dummy":
            return "WARNING: OPENROUTER_API_KEY is not configured."

        resp = get_openrouter_client().chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        return (resp.choices[0].message.content or "").strip()