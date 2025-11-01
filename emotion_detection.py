#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yüz Tanıma ve Duygu Analizi Sistemi
Bu program webcam kullanarak gerçek zamanlı yüz tanıma ve duygu analizi yapar.
"""

import cv2
from deepface import DeepFace
import numpy as np

class EmotionDetector:
    def __init__(self):
        """Duygu algılama sınıfını başlat"""
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Duygu renkleri (BGR formatında)
        self.emotion_colors = {
            'happy': (0, 255, 0),      # Yeşil
            'sad': (255, 0, 0),        # Mavi
            'angry': (0, 0, 255),      # Kırmızı
            'surprise': (0, 255, 255), # Sarı
            'fear': (128, 0, 128),     # Mor
            'disgust': (0, 128, 128),  # Kahverengi
            'neutral': (255, 255, 255) # Beyaz
        }
        
        # Duygu Türkçe karşılıkları
        self.emotion_tr = {
            'happy': 'Mutlu',
            'sad': 'Üzgün',
            'angry': 'Kızgın',
            'surprise': 'Şaşkın',
            'fear': 'Korkmuş',
            'disgust': 'İğrenmiş',
            'neutral': 'Nötr'
        }
    
    def detect_emotions(self, frame):
        """
        Görüntüdeki yüzleri tespit et ve duygularını analiz et
        
        Args:
            frame: OpenCV görüntü frame'i
            
        Returns:
            İşlenmiş görüntü frame'i
        """
        # Gri tonlamaya çevir (yüz tespiti için)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Yüzleri tespit et
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        # Her yüz için
        for (x, y, w, h) in faces:
            # Yüz bölgesini kes
            face_roi = frame[y:y+h, x:x+w]
            
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
                color = self.emotion_colors.get(emotion, (255, 255, 255))
                
                # Türkçe duygu adı
                emotion_tr = self.emotion_tr.get(emotion, emotion)
                
                # Yüzün etrafına dikdörtgen çiz
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                
                # Duygu etiketini yaz
                label = f"{emotion_tr}"
                cv2.putText(
                    frame, 
                    label, 
                    (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.9, 
                    color, 
                    2
                )
                
                # Duygu yüzdelerini göster (küçük yazıyla)
                y_offset = y + h + 20
                for emo, score in result['emotion'].items():
                    if score > 5:  # Sadece %5'ten yüksek olanları göster
                        emo_tr = self.emotion_tr.get(emo, emo)
                        text = f"{emo_tr}: {score:.1f}%"
                        cv2.putText(
                            frame, 
                            text, 
                            (x, y_offset), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.4, 
                            color, 
                            1
                        )
                        y_offset += 15
                        
            except Exception as e:
                # Hata durumunda sadece yüzü işaretle
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
                cv2.putText(
                    frame, 
                    "Analiz Ediliyor...", 
                    (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, 
                    (255, 255, 255), 
                    1
                )
        
        return frame
    
    def run(self):
        """Webcam'den görüntü al ve duygu analizi yap"""
        # Webcam'i başlat
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Hata: Kamera açılamadı!")
            return
        
        print("Duygu Analizi Sistemi Başlatıldı")
        print("Çıkmak için 'q' tuşuna basın")
        print("-" * 50)
        
        while True:
            # Frame oku
            ret, frame = cap.read()
            
            if not ret:
                print("Hata: Frame okunamadı!")
                break
            
            # Duygu analizi yap
            processed_frame = self.detect_emotions(frame)
            
            # Kullanım talimatını ekle
            cv2.putText(
                processed_frame,
                "Cikmak icin 'q' tusuna basin",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
            
            # Sonucu göster
            cv2.imshow('Yuz Tanima ve Duygu Analizi', processed_frame)
            
            # 'q' tuşuna basılırsa çık
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Temizlik
        cap.release()
        cv2.destroyAllWindows()
        print("\nProgram sonlandırıldı.")


def main():
    """Ana program"""
    detector = EmotionDetector()
    detector.run()


if __name__ == "__main__":
    main()

