import json
import os

class ChatMemory:
    def __init__(self, session_id: str, limit: int = 10):
        self.session_id = session_id
        self.limit = limit
        self.memory_dir = "logs/chat_history"
        os.makedirs(self.memory_dir, exist_ok=True)
        self.file_path = os.path.join(self.memory_dir, f"{session_id}.json")

    def save_message(self, role: str, content: str):
        """Mesajı hafızaya ekler ve dosyaya kaydeder."""
        history = self.get_history()
        history.append({"role": role, "content": content})
        
        # Sınırı aşan eski mesajları temizle (System prompt hariç)
        if len(history) > self.limit:
            system_msg = [m for m in history if m["role"] == "system"]
            other_msgs = [m for m in history if m["role"] != "system"]
            history = system_msg + other_msgs[-(self.limit-1):]

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    def get_history(self) -> list:
        """Kayıtlı mesaj geçmişini döner."""
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def clear_memory(self):
        """Hafızayı siler."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
