# Gerekli kütüphaneler
import mysql.connector                     # MySQL veritabanına bağlanmak için gerekli kütüphane
from datetime import datetime              # Zaman damgası eklemek için
import os                                  # Ortam değişkenlerini okumak için

def init_db():                             # Veritabanı ve tabloyu oluşturmak veya kontrol etmek için fonksiyon
    try:
        conn = mysql.connector.connect(                 # MySQL'e bağlantı oluşturulur
            host=os.getenv("MYSQL_HOST", "localhost"),  # MYSQL_HOST ortam değişkeni okunur, yoksa localhost varsayılan olarak kullanılır
            user=os.getenv("MYSQL_USER", "root"),       # MYSQL_USER ortam değişkeni okunur, yoksa root varsayılan olarak kullanılır
            password=os.getenv("MYSQL_PASSWORD", "")    # MYSQL_PASSWORD ortam değişkeni okunur, yoksa boş parola varsayılan olarak kullanılır
        )
        cursor = conn.cursor()             # SQL sorgularını çalıştırmak için cursor oluşturulur

        cursor.execute("CREATE DATABASE IF NOT EXISTS chatbot_db")  # chatbot_db veritabanı yoksa oluşturulur
        cursor.execute("USE chatbot_db")                            # Kullanılacak veritabanı seçilir

        # Sohbet kayıtlarını tutacak tablo yoksa oluşturulur
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME NOT NULL,
                model VARCHAR(50) NOT NULL,
                user_input TEXT NOT NULL,
                response TEXT NOT NULL
            )
        """)
        conn.commit()                      # Veritabanındaki değişiklikler kaydedilir
        cursor.close()                     # Cursor kapatılır
        conn.close()                       # Bağlantı kapatılır

        print("DEBUG: Veritabanı ve tablo kontrol edildi/oluşturuldu.")  # Başarılı işlem mesajı yazdırılır
    except Exception as e:                 # Hata yakalanır
        print(f"ERROR: Veritabanı veya tablo oluşturulamadı → {e}")  # Hata mesajı yazdırılır

def get_connection():                      # MySQL bağlantısı oluşturmak için fonksiyon
    return mysql.connector.connect(                        # Bağlantı oluşturulur ve döndürülür, bu noktada ortam değişkenleri kullanılır
        host=os.getenv("MYSQL_HOST", "localhost"),         
        user=os.getenv("MYSQL_USER", "root"),              
        password=os.getenv("MYSQL_PASSWORD", ""),          
        database=os.getenv("MYSQL_DATABASE", "chatbot_db")
    )

def log_interaction(user_input: str, response: str, model: str):  # Kullanıcı etkileşimini kaydeden fonksiyon
    try:
        conn = get_connection()            # Veritabanına bağlanılır
        cursor = conn.cursor()             # SQL sorgularını çalıştırmak için cursor oluşturulur

        # Sohbet kaydını veritabanına eklemek için SQL sorgusu hazırlanır
        query = """
            INSERT INTO chat_logs (timestamp, model, user_input, response)
            VALUES (%s, %s, %s, %s)
        """
        values = (datetime.now(), model, user_input, response)  # Kayıt için değerler hazırlanır
        cursor.execute(query, values)                           # Sorgu çalıştırılır
        conn.commit()                                           # Değişiklikler veritabanına kaydedilir

        cursor.close()                                          # Cursor kapatılır
        conn.close()                                            # Bağlantı kapatılır

        print(f"DEBUG: MySQL log kaydı eklendi → {model}")  
    except Exception as e:                                      # Hata durumunda
        print(f"ERROR: MySQL log kaydedilemedi → {e}")     