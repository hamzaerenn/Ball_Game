# Top Animasyonu Projesi

Python ve Tkinter kullanılarak geliştirilmiş interaktif top animasyonu uygulaması.

## Özellikler

- ✨ Farklı boyutlarda (küçük, orta, büyük) toplar ekleme
- 🎨 Farklı renklerde (kırmızı, mavi, sarı) toplar ekleme
- 🖱️ Canvas üzerine tıklayarak top ekleme
- ▶️ Animasyonu başlatma ve durdurma
- ⚡ Hız kontrolü (Speed Up)
- 🗑️ Tüm topları silme (Reset)
- 🎯 Kenar çarpışma tespiti ve sekme davranışı
- 🎬 Gerçek zamanlı animasyon (~60 FPS)

## Gereksinimler

- Python 3.x
- tkinter (Python ile birlikte gelir)

## Kurulum

1. Projeyi klonlayın veya indirin
2. Python'un yüklü olduğundan emin olun

## Kullanım

### Uygulamayı Çalıştırma

```bash
python ball_animation.py
```

veya

```bash
python3 ball_animation.py
```

### Kullanım Adımları

1. Uygulama açıldığında canvas alanı ve kontrol paneli görünür
2. İstediğiniz **boyut** (Küçük, Orta, Büyük) ve **renk** (Kırmızı, Mavi, Sarı) seçin
3. Canvas üzerine **tıklayarak** top ekleyin
4. **BAŞLAT** butonuna tıklayarak animasyonu başlatın
5. **DURDUR** butonu ile animasyonu durdurabilirsiniz
6. **Speed Up** butonu ile animasyon hızını artırabilirsiniz
7. **SİL** butonu ile tüm topları silebilirsiniz

```

Test uygulaması, projenin tüm bileşenlerini test eder ve sonuçları raporlar.

## Proje Yapısı

```
yazlabodev/
├── ball_animation.py      # Ana uygulama dosyası
└── README.md              # Bu dosya
```

## Teknolojiler

- **Python 3.x**: Programlama dili
- **tkinter**: Grafik kullanıcı arayüzü
- **math**: Matematiksel işlemler
- **random**: Rastgele değer üretimi
- **unittest**: Test framework'ü

## Özellikler Detayı

### Top Ekleme
- Canvas üzerine tıklayarak top ekleyebilirsiniz
- Seçili boyut ve renkte top eklenir
- Toplar başlangıçta hareketsizdir

### Animasyon Kontrolü
- **BAŞLAT**: Toplara rastgele hız verir ve animasyonu başlatır
- **DURDUR**: Animasyonu durdurur (toplar durmaz, sadece animasyon döngüsü durur)
- **SİL**: Tüm topları siler ve hızı sıfırlar

### Hız Kontrolü
- **Speed Up**: Her tıklamada hız çarpanını 0.5 artırır
- Mevcut hız çarpanı ekranda gösterilir
- Hareket eden topların hızı anında güncellenir

### Çarpışma Tespiti
- Toplar canvas kenarlarına çarptığında sekme davranışı gösterir
- Toplar canvas sınırları dışına çıkmaz
- Her kenar için ayrı çarpışma kontrolü yapılır

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.

---


