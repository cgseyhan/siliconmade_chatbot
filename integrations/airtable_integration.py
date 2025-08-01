# Gerekli kütüphaneler
from pyairtable import Table       # Airtable API'sine bağlanmak için pyairtable kütüphanesi
import os                          # Ortam değişkenlerine erişmek için

def log_interaction(user_input: str, response: str, model: str):
    try:
        api_key = os.getenv("AIRTABLE_API_KEY")                     # Airtable API anahtarı
        base_id = os.getenv("AIRTABLE_BASE_ID")                     # Airtable Base ID
        table_name = os.getenv("AIRTABLE_TABLE_NAME", "chat_logs")  # Tablo adı

        # Airtable tablosuna bağlanmak için bir Table nesnesi oluşturulur
        table = Table(api_key, base_id, table_name)

        # Kaydedilecek verileri içeren nesne
        record = {
            "model": model,           # Modelin adı
            "user_input": user_input, # Kullanıcının girdisi
            "bot_response": response  # Chatbot yanıtı
        }

        # Veriyi Airtable'a ekler
        table.create(record)
        print(f"DEBUG: Airtable kaydı eklendi → {model}")  # Başarılı ekleme durumunda debug çıktısı
    except Exception as e:
        # Herhangi bir hata durumunda hatayı ekrana yazdırır
        print(f"ERROR: Airtable kaydedilemedi → {e}")
