# Gerekli kütüphaneler
import os                       # Ortam değişkenlerine erişmek ve dosya yollarını yönetmek için
from openai import OpenAI       # OpenAI API istemcisini kullanmak için
from dotenv import load_dotenv  # .env dosyasından ortam değişkenlerini yüklemek için

# .env dosyasındaki ortam değişkenlerini belleğe yükler
load_dotenv()

# Ortam değişkeninden OpenAI API anahtarını alır ve OpenAI istemcisini başlatır
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# OpenAI sohbet fonksiyonu
def chat_with_openai(system_prompt: str, user_input: str) -> str:

    # Bir nesne ile OpenAI çağrılır
    response = client.chat.completions.create(
        model="gpt-4o",                                    # Kullanılacak model
        messages=[                                         # Mesaj listesi
            {"role": "system", "content": system_prompt},  # Sistem mesajı
            {"role": "user", "content": user_input},       # Kullanıcı girdisi
        ]
    )
    
    # OpenAI yanıtından modelin cevabını alır, baştaki ve sondaki boşlukları temizleyerek döndürür
    return response.choices[0].message.content.strip()
