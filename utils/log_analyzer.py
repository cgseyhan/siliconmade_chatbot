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
    Analyzes the logs in the database and produces a summary.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 1. Total message count
        cursor.execute("SELECT COUNT(*) as total FROM chat_logs")
        total_logs = cursor.fetchone()['total']

        # 2. Model usage distribution
        cursor.execute("SELECT model, COUNT(*) as count FROM chat_logs GROUP BY model")
        model_dist = cursor.fetchall()

        # 3. Most common words (Simple topic analysis)
        cursor.execute("SELECT user_input FROM chat_logs")
        inputs = cursor.fetchall()
        
        all_words = []
        stop_words = {"what", "how", "and", "a", "an", "the", "for", "in", "on", "at", "to", "of", "with"}
        
        for row in inputs:
            words = re.findall(r'\w+', row['user_input'].lower())
            all_words.extend([w for w in words if w not in stop_words and len(w) > 3])
        
        common_words = Counter(all_words).most_common(5)

        # 4. Last 5 interactions
        cursor.execute("SELECT timestamp, user_input, response FROM chat_logs ORDER BY timestamp DESC LIMIT 5")
        recent_chats = cursor.fetchall()

        cursor.close()
        conn.close()

        # Print Analysis Results
        print("\n--- CHATBOT LOG ANALYSIS ---")
        print(f"Total Interactions: {total_logs}")
        print("\nModel Distribution:")
        for m in model_dist:
            print(f"- {m['model']}: {m['count']}")
        
        print("\nMost Popular Topics (Words):")
        for word, count in common_words:
            print(f"- {word} ({count} times)")
        
        print("\nRecent Interactions:")
        for chat in recent_chats:
            print(f"[{chat['timestamp']}] User: {chat['user_input'][:50]}...")
            print(f"    Bot: {chat['response'][:50]}...")
            print("-" * 20)

    except Exception as e:
        print(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    analyze_logs()
