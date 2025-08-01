import json
import os
from datetime import datetime

# Proje kök dizinine chat_logs.json oluştur
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE = os.path.join(BASE_DIR, "chat_logs.json")

def log_interaction(user_input: str, response: str, model: str):

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "user_input": user_input,
        "response": response
    }

    # Eğer dosya yoksa oluştur
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)

    # Logları oku, JSON hatası varsa boş liste olarak devam et
    with open(LOG_FILE, "r+", encoding="utf-8") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

        logs.append(log_entry)
        f.seek(0)
        json.dump(logs, f, indent=4, ensure_ascii=False)
        f.truncate()

    print("DEBUG: Log kaydı başarıyla eklendi.")