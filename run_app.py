# Gerekli kütüphaneler
import subprocess  # Harici komut veya programları çalıştırmak için kullanılır
import sys         # Python yorumlayıcısının yolunu almak için kullanılır
import os          # Ortam değişkenlerini okumak için

def main():  
    app_path = os.path.join("frontend", "app.py")  # frontend klasöründeki app.py dosya yolunu oluştur
    
    # Streamlit uygulamasını başlatmak için subprocess ile komut çalıştırılır
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])

# Eğer bu dosya doğrudan çalıştırılıyorsa main() fonksiyonu çalıştırılır
if __name__ == "__main__":
    main()