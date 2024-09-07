import os
import requests
import subprocess
import sys
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk  # Pillow kütüphanesinden Image ve ImageTk

# DEBUG mode (0 = Off, 1 = On)
DEBUG = 0

# GitHub'daki version.txt dosyasının URL'si
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/ddttbb/versiyon-system-test/main/version.txt"
# GitHub repository URL'si
GITHUB_REPO_URL = "https://api.github.com/repos/ddttbb/versiyon-system-test/contents/"

# Yerel version.txt dosyası
LOCAL_VERSION_FILE = "version.txt"

# Debug function to print only when DEBUG is enabled
def debug_print(message):
    if DEBUG:
        print(message)

def get_github_version():
    """GitHub'daki versiyon numarasını alır"""
    try:
        response = requests.get(GITHUB_VERSION_URL)
        response.raise_for_status()
        github_version = response.text.strip()
        debug_print(f"GitHub versiyonu: {github_version}")
        return github_version
    except Exception as e:
        debug_print(f"GitHub versiyonu alınırken hata oluştu: {e}")
        return None

def get_local_version():
    """Yerel versiyon numarasını okur"""
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            local_version = f.read().strip()
            debug_print(f"Yerel versiyon: {local_version}")
            return local_version
    return None

def version_compare(v1, v2):
    """Versiyon numaralarını karşılaştırır (büyükse 1, küçükse -1, eşitse 0)"""
    v1_parts = list(map(int, v1.split('.')))
    v2_parts = list(map(int, v2.split('.')))
    
    for i in range(max(len(v1_parts), len(v2_parts))):
        part1 = v1_parts[i] if i < len(v1_parts) else 0
        part2 = v2_parts[i] if i < len(v2_parts) else 0
        if part1 > part2:
            return 1
        elif part1 < part2:
            return -1
    return 0

def update_application(progress, label_text):
    """pzr.py ve aynı dizindeki diğer dosyaları GitHub'dan günceller"""
    label_text.set("Güncellemeler Yükleniyor...")
    progress['value'] += 10
    debug_print("Güncelleme işlemi başlıyor...")
    
    # GitHub API üzerinden repo içeriğini al
    try:
        response = requests.get(GITHUB_REPO_URL)
        response.raise_for_status()
        contents = response.json()
    except Exception as e:
        debug_print(f"Repo içeriği alınırken hata oluştu: {e}")
        return

    for item in contents:
        file_name = item['name']
        if file_name == 'main.py':
            continue  # main.py dosyasını güncellemiyoruz
        elif item['type'] == 'file':
            download_url = item['download_url']
            try:
                file_response = requests.get(download_url)
                file_response.raise_for_status()
                # Dosyayı kaydet
                with open(file_name, 'wb') as f:
                    f.write(file_response.content)
                debug_print(f"{file_name} güncellendi.")
            except Exception as e:
                debug_print(f"{file_name} indirilemedi: {e}")
        elif item['type'] == 'dir':
            update_directory(item['path'], progress, label_text)
    
    label_text.set("Güncelleme Tamamlandı.")
    progress['value'] += 50
    debug_print("Güncelleme tamamlandı.")

def update_directory(dir_path, progress, label_text):
    """Belirtilen dizindeki dosyaları günceller"""
    url = f"https://api.github.com/repos/ddttbb/versiyon-system-test/contents/{dir_path}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        contents = response.json()
    except Exception as e:
        debug_print(f"Dizin içeriği alınırken hata oluştu: {e}")
        return

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for item in contents:
        file_name = item['name']
        path = os.path.join(dir_path, file_name)  
        if item['type'] == 'file':
            download_url = item['download_url']
            try:
                file_response = requests.get(download_url)
                file_response.raise_for_status()
                with open(path, 'wb') as f:
                    f.write(file_response.content)
                debug_print(f"{path} güncellendi.")
            except Exception as e:
                debug_print(f"{path} indirilemedi: {e}")
        elif item['type'] == 'dir':
            update_directory(path, progress, label_text)

def check_for_updates(progress, label_text):
    """Güncellemeyi kontrol eder"""
    github_version = get_github_version()
    local_version = get_local_version()

    if github_version and local_version:
        compare_result = version_compare(local_version, github_version)
        if compare_result == -1:
            debug_print(f"Güncelleme mevcut: {local_version} -> {github_version}")
            update_application(progress, label_text)
            with open(LOCAL_VERSION_FILE, 'w') as f:
                f.write(github_version)
        elif compare_result == 0:
            label_text.set("Uygulamanız Güncel.")
            progress['value'] = 100
            debug_print("Uygulamanız güncel.")
        else:
            label_text.set(f"Yerel sürüm daha yeni: {local_version} -> {github_version}")
    else:
        debug_print("Versiyon bilgileri alınamadı.")

def run_pzr_py():
    """pzr.py dosyasını yeni bir komut penceresinde çalıştırır ve mevcut pencereleri kapatır"""
    if os.path.exists('pzr.py'):
        debug_print("pzr.py yeni bir komut penceresinde çalıştırılıyor...")
        # Windows için yeni bir komut penceresinde çalıştırma
        if sys.platform == "win32":
            subprocess.Popen(['start', 'python', 'pzr.py'], shell=True)
        # Unix tabanlı sistemler için (Linux, macOS)
        else:
            subprocess.Popen(['xterm', '-e', 'python pzr.py'])
        # Mevcut script'i kapat
        sys.exit()
    else:
        debug_print("pzr.py bulunamadı.")

def create_gui():
    """GUI'yi oluşturur ve güncellemeleri kontrol eder"""
    root = Tk()
    root.title("Güncelleme Kontrol Sistemi")
    root.geometry("500x300")
    root.config(bg='#2E2E2E')

    # Simgeyi yeniden boyutlandırma
    try:
        img = Image.open("icon.png")
        img = img.resize((120, 120), Image.ANTIALIAS)  # Simge boyutunu ayarlama
        icon = ImageTk.PhotoImage(img)
        icon_label = Label(root, image=icon, bg='#2E2E2E')
        icon_label.place(relx=0.5, rely=0.3, anchor=CENTER)
    except Exception as e:
        debug_print(f"Icon yüklenemedi: {e}")
    
    # Progress Bar
    progress = ttk.Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate')
    progress.place(relx=0.5, rely=0.8, anchor=CENTER)

    # Label for displaying messages
    label_text = StringVar()
    label_text.set("Güncellemeler Kontrol Ediliyor...")
    label = Label(root, textvariable=label_text, bg='#2E2E2E', fg='white')
    label.place(relx=0.5, rely=0.9, anchor=CENTER)

    # İlk 1 saniyeden sonra güncelleme kontrolü başlar
    root.after(1000, lambda: check_for_updates(progress, label_text))

    # Güncellemeden 5 saniye sonra pzr.py çalıştırılır
    root.after(6000, run_pzr_py)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
