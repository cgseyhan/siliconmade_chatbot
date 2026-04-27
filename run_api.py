import os
import sys
import subprocess

def main():
    # Sanal ortamdaki python yolunu belirle
    if os.name == 'nt':  # Windows
        python_exe = os.path.join(".venv", "Scripts", "python.exe")
    else:
        python_exe = os.path.join(".venv", "bin", "python")

    # Eğer sanal ortam yoksa sistem python'ını kullan
    if not os.path.exists(python_exe):
        python_exe = sys.executable

    print(f"DEBUG: API Başlatılıyor -> {python_exe}")
    
    # FastAPI'yi uvicorn ile çalıştır
    # --reload parametresi kod değiştikçe otomatik yeniler
    subprocess.run([
        python_exe, "-m", "uvicorn", "api.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000", 
        "--reload"
    ])

if __name__ == "__main__":
    main()
