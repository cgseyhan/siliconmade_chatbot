import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# OpenRouter client (using OpenAI SDK, only base_url and headers are different)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        # These two headers are recommended by OpenRouter for accurate rate/quota and statistics tracking
        "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost"),
        "X-Title": os.getenv("OPENROUTER_APP_NAME", "Chatbot"),
    },
)

def chat_with_openrouter(system_prompt: str, user_input: str, model: str | None = None) -> str:
    """
    Chats using the selected model via OpenRouter.
    The model name comes from OPENROUTER_MODEL in .env; it can also be passed as a parameter.
    """
    model_name = model or os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")

    resp = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
    )
    return (resp.choices[0].message.content or "").strip()