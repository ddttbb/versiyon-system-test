import os
import requests
import subprocess

# GitHub'daki version.txt dosyasının URL'si
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/kullanici/repo/ana/version.txt"

# Yerel version.txt dosyası
LOCAL_VERSION_FILE = "version.txt"

def get_github_version():
    """GitHub'daki versiyon numarasını alır"""
    try:
        response = requests.get(GITHUB_VERSION_URL)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        print(f"GitHub versiyonu alınırken hata oluştu: {e}")
        return None

def get_local_version():
    """Yerel versiyon numarasını okur"""
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    return None

def update_application():
    """Uygulamayı GitHub'dan günceller"""
    print("Güncelleme işlemi başlıyor...")
    subprocess.run(["git", "clone", "https://github.com/kullanici/repo.git", "update_folder"])
    # Burada eski dosyaları değiştirme ve güncelleme işlemi yapılabilir
    print("Güncelleme tamamlandı. Uygulama yeniden başlatılacak.")
    
def check_for_updates():
    """Güncellemeyi kontrol eder"""
    github_version = get_github_version()
    local_version = get_local_version()

    if github_version and local_version:
        if github_version > local_version:
            print(f"Güncelleme mevcut: {local_version} -> {github_version}")
            update_application()
        else:
            print("Uygulamanız güncel.")
    else:
        print("Versiyon bilgileri alınamadı.")

if __name__ == "__main__":
    check_for_updates()

def main_application():
    print("Deneme 2")

if __name__ == "__main__":
    check_for_updates()
    main_application()
