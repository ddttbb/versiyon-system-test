import tkinter as tk

def create_gui():
    # Ana pencereyi oluştur
    root = tk.Tk()
    root.title("Basit Tkinter GUI")
    root.geometry("300x150")  # Pencere boyutunu ayarla

    # Merhaba yazısını gösteren bir etiket (Label) oluştur
    label = tk.Label(root, text="Merhaba!", font=("Arial", 24))
    label.pack(pady=20)  # Label'i pencerenin ortasına yerleştir ve 20px padding ekle

    # Pencereyi başlat
    root.mainloop()

if __name__ == "__main__":
    create_gui()
