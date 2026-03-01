import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# OpenRouter istemcisi (OpenAI SDK ile, sadece base_url ve header'lar farklı)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        # Bu iki header, OpenRouter'ın isabetli oran/kota ve istatistikler için önerdiği başlıklar
        "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost"),
        "X-Title": os.getenv("OPENROUTER_APP_NAME", "Chatbot"),
    },
)

def chat_with_openrouter(system_prompt: str, user_input: str, model: str | None = None) -> str:
    """
    OpenRouter üstünden seçili modeli kullanarak sohbet eder.
    Model adı .env'deki OPENROUTER_MODEL'den gelir; parametreyle de geçilebilir.
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