# Offline Page Downloader

Bu proje, bir web sayfasını çevrimdışı kullanılabilir hale getirmek için tasarlanmıştır. Hem terminal üzerinden hem de kullanıcı dostu bir GUI aracılığıyla kullanılabilir.

## Özellikler
- Web sayfasını indirir ve çevrimdışı kullanılabilir hale getirir.
- CSS, JavaScript, resimler, medya dosyaları ve SVG'leri HTML dosyasına gömülü hale getirir.
- Terminalden veya GUI üzerinden kullanım seçeneği sunar.
- Birden fazla indirmeyi sıraya koyar ve ilerleme durumunu gösterir.
- İndirme tamamlandığında klasörü otomatik olarak açar.

## Debian/Ubuntu Linux'te Kullanmak İçin Kurulum

`debian-install-offline-downloader.sh` dosyasını indirin ve çalıştırılabilir olarak işaretleyip çalıştırın:

```bash
sudo ./debian-install-offline-downloader.sh
```

## Arch Linux'te Kullanmak İçin Kurulum

### Yay ile Kurulum (AUR)
Eğer sisteminizde `yay` kuruluysa, paketi AUR'den aşağıdaki komutla kurabilirsiniz:

```bash
yay -S offline-page-downloader
```

### Manuel Kurulum (makepkg ile)
Eğer `yay` kullanmak istemiyorsanız, paketi manuel olarak da kurabilirsiniz:

1. Paketin AUR sayfasından `PKGBUILD` dosyasını indirin veya `git` ile klonlayın:

   ```bash
   git clone https://aur.archlinux.org/offline-page-downloader.git
   cd offline-page-downloader
   ```

2. Paketi derleyin ve kurun:

   ```bash
   makepkg -si
   ```

---

## Kullanım

### Terminal Üzerinden Kullanım
Terminal üzerinden web sayfası indirmek için:

```bash
offline_downloader <URL> <filename.html>
```

Örnek:

```bash
offline_downloader https://example.com filename.html
```

### Grafik Arayüz (GUI) ile Kullanım
Grafik arayüzü başlatmak için:

```bash
offline_downloader_gui
```

Bu komut, kullanıcı dostu bir arayüz açacaktır. İndirmek istediğiniz web sayfasının URL'sini girin ve "İndir" butonuna tıklayın.

## Python'da Geliştirme için Kurulum

1. Projeyi klonlayın:
   ```bash
   git clone https://github.com/metatronslove/offline-downloader-script-and-gui.git
   cd offline-downloader-script-and-gui-main
   ```

2. Gerekli bağımlılıkları kurun:
   ```bash
   pip install -r requirements.txt
   ```

3. PyQt5 kurulumu (Linux için):
   - Arch Linux:
     ```bash
     sudo pacman -S python-pyqt5
     ```
   - Ubuntu/Debian:
     ```bash
     sudo apt install python3-pyqt5
     ```
   - Fedora:
     ```bash
     sudo dnf install python3-qt5
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
- "Add to Queue" butonuna tıklayarak indirmeyi sıraya ekleyin.
- İndirme ilerlemesini tabloda takip edin.
- "Choose Download Folder" butonu ile indirme klasörünü seçin.
- "Show Download Folder" butonu ile indirme klasörünü dosya yöneticisinde açın.

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
