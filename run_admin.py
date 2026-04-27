import subprocess
import sys
import os

def main():  
    admin_path = os.path.join("frontend", "admin.py")
    
    # Sanal ortamdaki (venv) Python yolunu kontrol et
    venv_python = os.path.join(".venv", "Scripts", "python.exe")
    python_exe = venv_python if os.path.exists(venv_python) else sys.executable

    print(f"DEBUG: Başlatılıyor -> {python_exe}")
    
    # Admin panelini başlat
    subprocess.run([python_exe, "-m", "streamlit", "run", admin_path])

if __name__ == "__main__":
    main()
