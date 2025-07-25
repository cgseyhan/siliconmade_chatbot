# Gerekli kütüphaneler
import os                       # Ortam değişkenlerine erişmek için
from openai import OpenAI       # OpenAI istemcisi
from dotenv import load_dotenv  # .env dosyasından ortam değişkenlerini yüklemek için

# .env dosyasındaki ortam değişkenlerini belleğe yükler
load_dotenv()

# Ortam değişkeninden OpenAI API anahtarını alır
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# OpenAI sohbet fonksiyonu
def chat_with_openai(system_prompt: str, user_input: str) -> str:
    # OpenAI'nin Chat Completion API'ı çağrılır
    response = client.chat.completions.create(
        model="gpt-4o",                                    # Kullanılacak model
        messages=[                                         # Mesaj listesi: önce sistem mesajı, sonra kullanıcı girdisi
            {"role": "system", "content": system_prompt},  # Sistem mesajı (modelin genel davranışını belirler)
            {"role": "user", "content": user_input},       # Kullanıcı girdisi
        ]
    )
    # OpenAI yanıtından baştaki/sondaki boşlukları temizleyerek döndürür
    return response.choices[0].message.content.strip()