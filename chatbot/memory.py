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
        """Adds a message to the memory buffer and writes it to file."""
        history = self.get_history()
        history.append({"role": role, "content": content})
        
        # Prune old messages exceeding limit (except system prompt)
        if len(history) > self.limit:
            system_msg = [m for m in history if m["role"] == "system"]
            other_msgs = [m for m in history if m["role"] != "system"]
            history = system_msg + other_msgs[-(self.limit-1):]

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    def get_history(self) -> list:
        """Returns the saved message history list."""
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def clear_memory(self):
        """Deletes/clears the conversation memory file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
