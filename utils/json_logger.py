import json
import os
from datetime import datetime

# Log klasörü
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # Klasör yoksa oluştur

def log_interaction(user_input: str, response: str, model: str):
    # Her sohbet kaydı için yeni dosya adı
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR, f"{timestamp_str}.json")

    # Kayıt verisi
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "user_input": user_input,
        "response": response
    }

    # JSON dosyasını oluştur
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_entry, f, indent=4, ensure_ascii=False)

    print(f"DEBUG: Yeni log dosyası oluşturuldu → {log_file}")