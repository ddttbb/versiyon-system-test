# Python Uygulama Güncelleme Sistemi

Bu proje, GitHub'dan versiyon kontrolü ve otomatik güncellemeler yapmak için kullanılan bir Python uygulama güncelleme sistemini içerir. Uygulama, GitHub'daki `version.txt` dosyasını kullanarak yerel ve uzak versiyonları karşılaştırır ve güncellemeleri yönetir.

## Özellikler

- GitHub'daki `version.txt` dosyasından uygulama versiyonunu kontrol eder.
- Yerel versiyonla karşılaştırarak güncellemeleri uygular.
- Güncellemeleri yaparken kullanıcıya bilgi verir ve bir ilerleme çubuğu gösterir.
- Güncellemeler tamamlandığında, ana uygulama (`pzr.py`) yeni bir komut penceresinde çalıştırılır ve mevcut pencere kapanır.

## Gereksinimler

- Python 3.6 veya üstü
- `requests` kütüphanesi (HTTP istekleri için)
- `Pillow` kütüphanesi (GUI simgeleri için)
- Tkinter (GUI bileşenleri için)

## Kurulum

1. **Gereksinimleri Yükleyin**:
   ```bash
   pip install requests Pillow
