# Gerekli kütüphaneler
import os                       # Ortam değişkenlerine erişmek ve dosya yollarını yönetmek için
from openai import OpenAI       # OpenAI API istemcisini kullanmak için
from dotenv import load_dotenv  # .env dosyasından ortam değişkenlerini yüklemek için

# .env dosyasını tam yol ile yükle
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(os.path.dirname(current_dir), ".env")
load_dotenv(env_path)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print(f"WARNING: OPENAI_API_KEY bulunamadı! Aranan yol: {env_path}")

# Ortam değişkeninden OpenAI API anahtarını alır ve OpenAI istemcisini başlatır
client = OpenAI(api_key=api_key)

def chat_with_openai(messages: list, image_b64: str = None) -> dict:
    """
    OpenAI API'sine mesaj listesini gönderir ve YAPILANDIRILMIŞ (JSON) bir yanıt döndürür.
    """
    if image_b64:
        image_msg = {
            "role": "user",
            "content": [
                {"type": "text", "text": messages[-1]["content"] if messages else "Bu resmi analiz et."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
                }
            ]
        }
        messages = messages[:-1] + [image_msg]

    # Sistem mesajına JSON kuralını ekleyelim
    system_instruction = "\nYanıtını DAİMA şu JSON formatında ver: {\"answer\": \"...\", \"sentiment\": \"...\", \"intent\": \"...\"}"
    if messages[0]["role"] == "system":
        messages[0]["content"] += system_instruction

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        response_format={ "type": "json_object" }
    )
    
    import json
    return json.loads(response.choices[0].message.content)
