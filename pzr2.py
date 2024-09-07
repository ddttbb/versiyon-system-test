import os
import subprocess
import sys

def run_pzr_exe():
    """pzr.exe dosyasını yeni bir komut penceresinde çalıştırır"""
    if os.path.exists('pzr.exe'):
        try:
            # Windows komut penceresinde pzr.exe'yi başlat
            subprocess.Popen(['cmd', '/c', 'start', 'pzr.exe'], shell=True)
            sys.exit()  # Mevcut pencereyi kapat
        except Exception as e:
            print(f"pzr.exe çalıştırılırken hata oluştu: {e}")
            sys.exit(1)
    else:
        print("pzr.exe bulunamadı.")
        sys.exit(1)

if __name__ == "__main__":
    run_pzr_exe()
