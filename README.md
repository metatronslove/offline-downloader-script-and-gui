# Offline Page Downloader

Bu proje, bir web sayfasını çevrimdışı kullanılabilir hale getirmek için tasarlanmıştır. Hem terminal üzerinden hem de kullanıcı dostu bir GUI aracılığıyla kullanılabilir.

## Özellikler
- Web sayfasını indirir ve çevrimdışı kullanılabilir hale getirir.
- CSS, JavaScript, resimler, medya dosyaları ve SVG'leri Base64 formatına dönüştürerek HTML dosyasına gömülü hale getirir.
- Terminalden veya GUI üzerinden kullanım seçeneği sunar.

## Kurulum

1. Projeyi klonlayın:
   ```bash
   git clone https://github.com/kullanici_adi/offline-page-downloader.git
   cd offline-page-downloader
   ```

2. Gerekli bağımlılıkları kurun:
   ```bash
   pip install -r requirements.txt
   ```

3. GTK4 kurulumu (Linux için):
   - Ubuntu/Debian:
     ```bash
     sudo apt install libgtk-4-dev
     ```
   - Fedora:
     ```bash
     sudo dnf install gtk4-devel
     ```

## Kullanım

### Terminalden Kullanım
Terminalden bir web sayfasını indirmek için aşağıdaki komutu kullanın:
```bash
python3 offline_downloader.py <URL> <output_filename>
```

Örnek:
```bash
python3 offline_downloader.py https://example.com example.html
```

### GUI ile Kullanım
GUI uygulamasını başlatmak için aşağıdaki komutu kullanın:
```bash
python3 offline_downloader_gui.py
```

- URL'yi ve çıktı dosya adını girin.
- "Download" butonuna tıklayarak indirme işlemini başlatın.

## Katkıda Bulunma
Katkıda bulunmak için lütfen bir "Pull Request" açın. Sorunlarınızı "Issues" bölümünde bildirebilirsiniz.

## Lisans
Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

## 🎁 Destek Ol
**Çalışmalarımın sürmesine olanak sağlamak için bağışta bulunabilirsiniz.**
*Lütfen bağış yapmadan önce en az iki kere düşünün çünkü geri ödemeler için ayıracak hiç zamanım ve imkanım yok.*
**Katkılarınız için paylaştıklarımı kullanan herkes adına teşekkürlerimi kabul edin.**

## 🎁 Support Me
**You can support me to keep my projects alive.**
*Please think twice before donating because I have no time or means to handle refunds.*
**On behalf of everyone who uses what I share, I accept your thanks for your contributions.**

[![Papara ile Destekle](https://img.shields.io/badge/Bağış%20Yap-%E2%9D%A4-blue)](https://ppr.ist/1T9dx8tUT)
[![Donate using Papara](https://img.shields.io/badge/Donate-%E2%9D%A4-blue)](https://ppr.ist/1T9dx8tUT)

[![Papara ile Desteklen](1513592797QR.png)](https://ppr.ist/1T99dYF5X)