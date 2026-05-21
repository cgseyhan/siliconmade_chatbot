import json
import os
from datetime import datetime

# Log directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # Create directory if it doesn't exist

def log_interaction(user_input: str, response: str, model: str):
    # New filename for each chat record
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR, f"{timestamp_str}.json")

    # Log entry data
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "user_input": user_input,
        "response": response
    }

    # Create JSON file
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_entry, f, indent=4, ensure_ascii=False)

    print(f"DEBUG: New log file created -> {log_file}")