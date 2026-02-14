# 🎮 Last Move Game Visualization

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web-000000?style=for-the-badge&logo=flask&logoColor=white)

Last Move, oyuncuların stratejik hamlelerle rakiplerini kısıtlamaya çalıştığı bir masa oyunudur. Bu proje, oyunun dinamiklerini modern bir **GUI (Grafiksel Kullanıcı Arayüzü)** üzerinden, SVG grafik desteğiyle görselleştirir.

## ✨ Özellikler

- **Esnek Tahta Boyutları:** 3x3, 5x5 veya 7x7 boyutlarında özelleştirilebilir oyun alanı.
- **SVG Entegrasyonu:** Yüksek kaliteli `svgwrite` ile oluşturulmuş vektörel taş ve tahta grafikleri.
- **İnteraktif GUI:** PyQt5 kullanılarak tasarlanmış, kullanıcı dostu hamle yönetimi.
- **Oyun Mekaniği:** Büyük taş hareketleri ve küçük taş yerleştirme (bloklama) sisteminin tam simülasyonu.

## 📂 Proje Yapısı

```text
last-move-visualization
├── src
│   ├── main.py          # Ana oyun mantığı ve döngüsü
│   ├── gui.py           # PyQt5 arayüz tanımlamaları
│   ├── utils.py         # Yardımcı fonksiyonlar
│   └── assets/          # SVG Grafikleri
│       ├── board_*.svg  # Tahta tasarımları
│       └── stone_*.svg  # Taş tasarımları
├── requirements.txt     # Bağımlılıklar
└── README.md            # Dokümantasyon
```
## 🛠️ Setup Instructions
Projeyi yerel makinenizde çalıştırmak için şu adımları izleyin:


1. **Depoyu Klonlayın**:
   Python'un yüklü olduğundan emin olun ve ardından gerekli bağımlılıkları yükleyin:
   
2. **Oyunu Çalıştırın**:
   Ana scripti çalıştırarak oyunu başlatın:

## 🎮 Usage Guidelines
Tahta Seçimi: Oyun başladığında 3x3, 5x5 veya 7x7 boyutlarından birini seçmeniz istenir.

Sıra Tabanlı Hamle: Oyuncular sırayla büyük taşlarını hareket ettirir ve stratejik noktalara küçük taşlar yerleştirir.

Oyun Sonu: Geçerli bir hamle yapma imkanı kalmayan (hareket alanı kısıtlanan) oyuncu oyunu kaybeder.


## 📦 Requirements
Projenin kararlı çalışması için aşağıdaki sürümler kullanılmaktadır:

Flask==2.0.1

PyQt5==5.15.4

svgwrite==1.4.1

Pillow==8.2.0

## 🤝 Contributing
Katkıda bulunmak isterseniz, lütfen bir Pull Request gönderin veya iyileştirme önerileriniz için bir Issue açın. Her türlü katkı memnuniyetle karşılanır!

## 📄 License
Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için LICENSE dosyasına göz atabilirsiniz.
