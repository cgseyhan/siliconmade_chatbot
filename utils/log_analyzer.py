import mysql.connector
import os
from collections import Counter
import re

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "chatbot_db")
    )

def analyze_logs():
    """
    MySQL'deki logları analiz eder ve özet çıkarır.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 1. Toplam mesaj sayısı
        cursor.execute("SELECT COUNT(*) as total FROM chat_logs")
        total_logs = cursor.fetchone()['total']

        # 2. Model kullanım dağılımı
        cursor.execute("SELECT model, COUNT(*) as count FROM chat_logs GROUP BY model")
        model_dist = cursor.fetchall()

        # 3. En çok kullanılan kelimeler (Basit konu analizi)
        cursor.execute("SELECT user_input FROM chat_logs")
        inputs = cursor.fetchall()
        
        all_words = []
        stop_words = {"ne", "nasıl", "ve", "bir", "mi", "mı", "için", "da", "de", "bu", "şu"}
        
        for row in inputs:
            words = re.findall(r'\w+', row['user_input'].lower())
            all_words.extend([w for w in words if w not in stop_words and len(w) > 3])
        
        common_words = Counter(all_words).most_common(5)

        # 4. Son 5 etkileşim
        cursor.execute("SELECT timestamp, user_input, response FROM chat_logs ORDER BY timestamp DESC LIMIT 5")
        recent_chats = cursor.fetchall()

        cursor.close()
        conn.close()

        # Analiz Sonuçlarını Yazdır
        print("\n--- CHATBOT LOG ANALİZİ ---")
        print(f"Toplam Etkileşim: {total_logs}")
        print("\nModel Dağılımı:")
        for m in model_dist:
            print(f"- {m['model']}: {m['count']}")
        
        print("\nEn Popüler Konular (Kelimeler):")
        for word, count in common_words:
            print(f"- {word} ({count} kez)")
        
        print("\nSon Etkileşimler:")
        for chat in recent_chats:
            print(f"[{chat['timestamp']}] Kullanıcı: {chat['user_input'][:50]}...")
            print(f"    Bot: {chat['response'][:50]}...")
            print("-" * 20)

    except Exception as e:
        print(f"Analiz sırasında hata oluştu: {e}")

if __name__ == "__main__":
    analyze_logs()
