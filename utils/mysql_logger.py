# Gerekli kütüphaneler
import sqlite3                              # SQLite veritabanı için (kurulum gerektirmez)
from datetime import datetime              # Zaman damgası eklemek için
import os                                  # Dosya yollarını yönetmek için

# Veritabanı dosyasının mutlak yolunu belirle (Hangi klasörden çalışırsa çalışsın aynı dosyayı kullanır)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "chatbot.db")

def init_db():                             # Veritabanı ve tabloları oluşturmak için fonksiyon
    try:
        conn = sqlite3.connect(DB_PATH)    # Dosyaya bağlan (yoksa oluşturur)
        cursor = conn.cursor()

        # Sohbet kayıtlarını tutacak tablo
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                model TEXT NOT NULL,
                user_input TEXT NOT NULL,
                response TEXT NOT NULL,
                sentiment TEXT,
                intent TEXT
            )
        """)

        # Aday müşteri (Lead) tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                name TEXT,
                email TEXT,
                phone TEXT,
                course_interest TEXT,
                notes TEXT
            )
        """)
        conn.commit()
        conn.close()
        print(f"DEBUG: SQLite Veritabanı kontrol edildi ({DB_PATH}).")
    except Exception as e:
        print(f"ERROR: Veritabanı oluşturulamadı → {e}")

def get_connection():                      # SQLite bağlantısı oluşturmak için fonksiyon
    return sqlite3.connect(DB_PATH)

def log_interaction(user_input: str, response: str, model: str, sentiment: str = "Unknown", intent: str = "Unknown"):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO chat_logs (timestamp, model, user_input, response, sentiment, intent)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (datetime.now(), model, user_input, response, sentiment, intent)
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        print(f"DEBUG: [OK] SQLite'a log kaydedildi. (Sentiment: {sentiment})")  
    except Exception as e:
        print(f"ERROR: [FAIL] SQLite log hatası → {e}")

def save_lead(name=None, email=None, phone=None, course=None, notes=None):
    """Aday müşteri bilgilerini SQLite veritabanına kaydeder."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO leads (timestamp, name, email, phone, course_interest, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (datetime.now(), name, email, phone, course, notes)
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        print(f"DEBUG: Yeni LEAD kaydedildi → {name or email}")
    except Exception as e:
        print(f"ERROR: Lead kaydedilemedi → {e}")