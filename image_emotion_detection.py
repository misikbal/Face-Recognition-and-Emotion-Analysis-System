#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Görüntü Dosyasından Duygu Analizi
Bir görüntü dosyasındaki yüzleri tespit eder ve duygu analizi yapar.
"""

import cv2
import sys
from deepface import DeepFace
import os

def analyze_image(image_path):
    """
    Görüntü dosyasındaki yüzleri tespit et ve duygularını analiz et
    
    Args:
        image_path: Analiz edilecek görüntü dosyasının yolu
    """
    
    # Duygu renkleri (BGR formatında)
    emotion_colors = {
        'happy': (0, 255, 0),      # Yeşil
        'sad': (255, 0, 0),        # Mavi
        'angry': (0, 0, 255),      # Kırmızı
        'surprise': (0, 255, 255), # Sarı
        'fear': (128, 0, 128),     # Mor
        'disgust': (0, 128, 128),  # Kahverengi
        'neutral': (255, 255, 255) # Beyaz
    }
    
    # Duygu Türkçe karşılıkları
    emotion_tr = {
        'happy': 'Mutlu',
        'sad': 'Üzgün',
        'angry': 'Kızgın',
        'surprise': 'Şaşkın',
        'fear': 'Korkmuş',
        'disgust': 'İğrenmiş',
        'neutral': 'Nötr'
    }
    
    # Dosya kontrolü
    if not os.path.exists(image_path):
        print(f"Hata: '{image_path}' dosyası bulunamadı!")
        return
    
    # Görüntüyü oku
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Hata: '{image_path}' görüntüsü yüklenemedi!")
        return
    
    print(f"Analiz ediliyor: {image_path}")
    print("-" * 60)
    
    # Yüz tespiti için cascade classifier
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    # Gri tonlamaya çevir
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Yüzleri tespit et
    faces = face_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(30, 30)
    )
    
    if len(faces) == 0:
        print("Görüntüde yüz tespit edilemedi!")
        return
    
    print(f"{len(faces)} adet yüz tespit edildi.\n")
    
    # Her yüz için
    for i, (x, y, w, h) in enumerate(faces, 1):
        # Yüz bölgesini kes
        face_roi = image[y:y+h, x:x+w]
        
        try:
            # DeepFace ile duygu analizi yap
            result = DeepFace.analyze(
                face_roi, 
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )
            
            # Sonuç liste ise ilk elemanı al
            if isinstance(result, list):
                result = result[0]
            
            # Baskın duyguyu al
            emotion = result['dominant_emotion']
            
            # Renk seç
            color = emotion_colors.get(emotion, (255, 255, 255))
            
            # Türkçe duygu adı
            emotion_tr_name = emotion_tr.get(emotion, emotion)
            
            # Yüzün etrafına dikdörtgen çiz
            cv2.rectangle(image, (x, y), (x+w, y+h), color, 3)
            
            # Duygu etiketini yaz
            label = f"Yuz #{i}: {emotion_tr_name}"
            cv2.putText(
                image, 
                label, 
                (x, y-10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.9, 
                color, 
                2
            )
            
            # Konsola yazdır
            print(f"Yüz #{i}:")
            print(f"  Baskın Duygu: {emotion_tr_name}")
            print(f"  Duygu Dağılımı:")
            
            # Duygu skorlarını sırala
            sorted_emotions = sorted(
                result['emotion'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            for emo, score in sorted_emotions:
                emo_tr_name = emotion_tr.get(emo, emo)
                bar = "█" * int(score / 5)
                print(f"    {emo_tr_name:12s}: {score:5.2f}% {bar}")
            
            print()
                    
        except Exception as e:
            print(f"Yüz #{i} analiz edilemedi: {str(e)}")
            # Hata durumunda sadece yüzü işaretle
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 255), 2)
    
    # Sonuç dosyasını kaydet
    output_path = image_path.rsplit('.', 1)[0] + '_analyzed.' + image_path.rsplit('.', 1)[1]
    cv2.imwrite(output_path, image)
    print(f"Analiz edilmiş görüntü kaydedildi: {output_path}")
    
    print(f"\nAnaliz tamamlandı!")
    print(f"Sonuç dosyası: {output_path}")
    print("\nNot: opencv-python-headless kullanıldığı için görüntü ekranda gösterilemiyor.")
    print(f"Lütfen '{output_path}' dosyasını bir görüntü görüntüleyici ile açın.")


def main():
    """Ana program"""
    if len(sys.argv) < 2:
        print("Kullanım: python image_emotion_detection.py <görüntü_dosyası>")
        print("\nÖrnek:")
        print("  python image_emotion_detection.py foto.jpg")
        print("  python image_emotion_detection.py /home/kullanici/resimler/portre.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    analyze_image(image_path)


if __name__ == "__main__":
    main()

