# Gerekli kütüphaneler içe aktarılıyor
import subprocess  # Harici işlemler çalıştırmak için kullanılır
import sys         # Python yolunu almak için kullanılır

def main():
    # Streamlit frontend uygulamasını başlatmak için terminal komutu çalıştırılır
    subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])
    # sys.executable: aktif Python yorumlayıcısının yolu (örneğin venv kullanılıyorsa doğru ortamı garantiler)
    # "-m streamlit run frontend/app.py": Streamlit komutunu çalıştırır ve ilgili uygulamayı açar

# Eğer bu dosya çalıştırılıyorsa main() fonksiyonu çağrılır
if __name__ == "__main__":
    main()