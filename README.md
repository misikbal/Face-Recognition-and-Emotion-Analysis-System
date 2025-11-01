# Yüz Tanıma ve Duygu Analizi Sistemi

Python ile geliştirilmiş gerçek zamanlı yüz tanıma ve duygu analizi uygulaması. Bu sistem, webcam görüntüsünden yüzleri tespit eder ve 7 farklı duygu durumunu analiz eder.

## Özellikler

✨ **Gerçek Zamanlı Analiz**: Webcam'den anlık görüntü işleme  
🎭 **7 Farklı Duygu**: Mutlu, Üzgün, Kızgın, Şaşkın, Korkmuş, İğrenmiş, Nötr  
🎨 **Renkli Gösterim**: Her duygu için farklı renk kodlaması  
📊 **Detaylı İstatistikler**: Her duygu için yüzde oranları  
🚀 **Kolay Kullanım**: Tek komutla çalışır

## Tespit Edilen Duygular

| Duygu | İngilizce | Renk |
|-------|-----------|------|
| 😊 Mutlu | Happy | Yeşil |
| 😢 Üzgün | Sad | Mavi |
| 😠 Kızgın | Angry | Kırmızı |
| 😲 Şaşkın | Surprise | Sarı |
| 😨 Korkmuş | Fear | Mor |
| 🤢 İğrenmiş | Disgust | Kahverengi |
| 😐 Nötr | Neutral | Beyaz |

## Gereksinimler

- Python 3.8 veya üzeri
- Webcam
- İşletim Sistemi: Linux, Windows, macOS

## Kurulum

### 1. Depoyu klonlayın veya dosyaları indirin

```bash
cd /home/ikbal/Desktop/ai
```

### 2. Sanal ortam oluşturun (önerilen)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 3. Gerekli kütüphaneleri yükleyin

```bash
pip install -r requirements.txt
```

**Not**: İlk kurulum biraz zaman alabilir çünkü TensorFlow gibi büyük kütüphaneler indirilecektir.

## Kullanım

### Webcam ile Video Kaydı (Headless - GUI Olmadan)

**Not**: Sistem headless (GUI olmadan) çalışacak şekilde yapılandırılmıştır. Webcam görüntüsü ekranda gösterilmez ancak analiz edilmiş video dosyasına kaydedilir.

```bash
# 30 saniye kayıt yap (varsayılan)
python emotion_detection_webcam.py

# 60 saniye kayıt yap
python emotion_detection_webcam.py --duration 60

# Sınırsız kayıt (Ctrl+C ile durdurun)
python emotion_detection_webcam.py --duration 0

# Video kaydetmeden sadece konsol çıktısı
python emotion_detection_webcam.py --no-save
```

Program açıldığında:
- Webcam otomatik olarak başlayacak
- Her frame'de tespit edilen duygular konsola yazılacak
- İşlenmiş video `emotion_analysis_TARIH_SAAT.avi` olarak kaydedilecek
- Kayıt bitince video dosyasını oynatıcı ile izleyebilirsiniz

### Görüntü Dosyasından Analiz

Eğer bir görüntü dosyasından duygu analizi yapmak isterseniz, aşağıdaki scripti kullanabilirsiniz:

```bash
python image_emotion_detection.py resim.jpg
```

## Nasıl Çalışır?

1. **Yüz Tespiti**: OpenCV'nin Haar Cascade algoritması ile yüzler tespit edilir
2. **Duygu Analizi**: DeepFace kütüphanesi ile yüz ifadeleri analiz edilir
3. **Görselleştirme**: Tespit edilen duygular renkli çerçeveler ve etiketlerle gösterilir

## Teknik Detaylar

### Kullanılan Kütüphaneler

- **OpenCV**: Görüntü işleme ve yüz tespiti
- **DeepFace**: Derin öğrenme tabanlı yüz analizi
- **TensorFlow**: DeepFace'in backend'i
- **NumPy**: Sayısal işlemler

### Duygu Analizi Modeli

DeepFace, Facebook AI Research tarafından geliştirilen güçlü bir yüz tanıma framework'üdür. Bu projede:
- Önceden eğitilmiş modeller kullanılır
- 7 temel duygu kategorisi desteklenir
- Yüksek doğruluk oranı sağlar

## Sorun Giderme

### Kamera Açılamıyor

```bash
# Kamera izinlerini kontrol edin
# Linux'ta: kullanıcıyı video grubuna ekleyin
sudo usermod -a -G video $USER
```

### TensorFlow Uyarıları

TensorFlow bazı uyarılar verebilir, ancak bunlar genellikle performansla ilgilidir ve programın çalışmasını etkilemez.

### Yavaş Çalışma

- İlk çalıştırmada modeller yüklendiği için yavaş olabilir
- GPU desteği için TensorFlow-GPU kurabilirsiniz
- Düşük çözünürlüklü webcam kullanmayı deneyin

## Geliştirme Fikirleri

- [ ] Çoklu yüz tespiti optimizasyonu
- [ ] Duygu geçmişi grafiği
- [ ] Video dosyasından analiz
- [ ] Duygu verilerini CSV'ye kaydetme
- [ ] Web arayüzü ekleme

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Ticari kullanım için ilgili kütüphanelerin lisanslarını kontrol edin.

## İletişim

Sorularınız veya önerileriniz için issue açabilirsiniz.

---

**Not**: Bu sistem gerçek zamanlı duygu analizi yapar ancak %100 doğru olmayabilir. Sonuçlar kişinin yüz ifadesine, ışık koşullarına ve kamera kalitesine bağlıdır.

