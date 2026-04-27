# Gerekli kütüphaneler
import subprocess  # Harici komut veya programları çalıştırmak için kullanılır
import sys         # Python yorumlayıcısının yolunu almak için kullanılır
import os          # Ortam değişkenlerini okumak için

def main():  
    app_path = os.path.join("frontend", "app.py")
    
    # Sanal ortamdaki (venv) Python yolunu kontrol et
    venv_python = os.path.join(".venv", "Scripts", "python.exe")
    python_exe = venv_python if os.path.exists(venv_python) else sys.executable

    print(f"DEBUG: Başlatılıyor -> {python_exe}")
    
    # Uygulamayı başlat
    subprocess.run([python_exe, "-m", "streamlit", "run", app_path])

# Eğer bu dosya doğrudan çalıştırılıyorsa main() fonksiyonu çalıştırılır
if __name__ == "__main__":
    main()