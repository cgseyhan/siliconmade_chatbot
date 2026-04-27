import sqlite3
import os

db_path = 'chatbot.db'

def migrate():
    if not os.path.exists(db_path):
        print("Database not found, skipping migration (it will be created by app).")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Mevcut kolonları kontrol et
    cursor.execute("PRAGMA table_info(chat_logs)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'sentiment' not in columns:
        try:
            cursor.execute("ALTER TABLE chat_logs ADD COLUMN sentiment TEXT DEFAULT 'Unknown'")
            print("Added 'sentiment' column.")
        except Exception as e:
            print(f"Error adding sentiment: {e}")
            
    if 'intent' not in columns:
        try:
            cursor.execute("ALTER TABLE chat_logs ADD COLUMN intent TEXT DEFAULT 'Unknown'")
            print("Added 'intent' column.")
        except Exception as e:
            print(f"Error adding intent: {e}")
            
    conn.commit()
    conn.close()
    print("Migration finished.")

if __name__ == "__main__":
    migrate()
