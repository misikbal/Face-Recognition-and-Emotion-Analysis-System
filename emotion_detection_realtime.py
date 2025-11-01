#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yüz Tanıma ve Duygu Analizi Sistemi - Gerçek Zamanlı Görüntüleme
Webcam görüntüsünü anlık olarak ekranda gösterir ve duygu analizi yapar.
"""

import cv2
from deepface import DeepFace
import numpy as np
import time

class EmotionDetector:
    def __init__(self, analyze_interval=30):
        """
        Duygu algılama sınıfını başlat
        
        Args:
            analyze_interval: Kaç frame'de bir duygu analizi yapılacak (performans için)
        """
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.analyze_interval = analyze_interval
        self.frame_count = 0
        
        # Son analiz sonuçlarını sakla
        self.last_emotions = {}
        
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
            'sad': 'Uzgun',
            'angry': 'Kizgin',
            'surprise': 'Saskin',
            'fear': 'Korkmus',
            'disgust': 'Igrenmis',
            'neutral': 'Notr'
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
        for face_idx, (x, y, w, h) in enumerate(faces):
            face_key = f"face_{face_idx}"
            
            # Performans için sadece belirli aralıklarla analiz yap
            should_analyze = (self.frame_count % self.analyze_interval == 0)
            
            if should_analyze:
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
                    
                    # Son analiz sonucunu sakla
                    self.last_emotions[face_key] = {
                        'dominant': result['dominant_emotion'],
                        'scores': result['emotion']
                    }
                    
                except Exception as e:
                    # Hata durumunda
                    if face_key not in self.last_emotions:
                        self.last_emotions[face_key] = {
                            'dominant': 'neutral',
                            'scores': {}
                        }
            
            # Mevcut veya son bilinen duyguyu göster
            if face_key in self.last_emotions:
                emotion_data = self.last_emotions[face_key]
                emotion = emotion_data['dominant']
                scores = emotion_data['scores']
                
                # Renk seç
                color = self.emotion_colors.get(emotion, (255, 255, 255))
                
                # Türkçe duygu adı
                emotion_tr = self.emotion_tr.get(emotion, emotion)
                
                # Yüzün etrafına dikdörtgen çiz
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
                
                # Duygu etiketini yaz
                label = f"{emotion_tr}"
                cv2.putText(
                    frame, 
                    label, 
                    (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1.2, 
                    color, 
                    3
                )
                
                # Duygu yüzdelerini göster (en yüksek 3 duygu)
                if scores:
                    sorted_emotions = sorted(
                        scores.items(), 
                        key=lambda x: x[1], 
                        reverse=True
                    )[:3]
                    
                    y_offset = y + h + 25
                    for emo, score in sorted_emotions:
                        emo_tr = self.emotion_tr.get(emo, emo)
                        text = f"{emo_tr}: {score:.1f}%"
                        cv2.putText(
                            frame, 
                            text, 
                            (x, y_offset), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.5, 
                            color, 
                            2
                        )
                        y_offset += 20
            else:
                # Henüz analiz edilmemiş
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
                cv2.putText(
                    frame, 
                    "Analiz ediliyor...", 
                    (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, 
                    (255, 255, 255), 
                    2
                )
        
        return frame
    
    def run(self):
        """Webcam'den görüntü al ve gerçek zamanlı duygu analizi yap"""
        # Webcam'i başlat
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Hata: Kamera açılamadı!")
            print("Lütfen webcam'in bağlı olduğundan ve izinlerin verildiğinden emin olun.")
            return
        
        # Pencere adı
        window_name = 'Yuz Tanima ve Duygu Analizi - Anlik Goruntuleme'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        
        print("=" * 60)
        print("Duygu Analizi Sistemi - Gerçek Zamanlı Görüntüleme")
        print("=" * 60)
        print(f"Analiz aralığı: Her {self.analyze_interval} frame'de bir")
        print("Çıkmak için 'q' tuşuna veya ESC'ye basın")
        print("=" * 60)
        print()
        
        fps_start_time = time.time()
        fps_frame_count = 0
        fps = 0
        
        while True:
            # Frame oku
            ret, frame = cap.read()
            
            if not ret:
                print("Hata: Frame okunamadı!")
                break
            
            # FPS hesapla
            fps_frame_count += 1
            if fps_frame_count >= 30:
                fps_end_time = time.time()
                fps = fps_frame_count / (fps_end_time - fps_start_time)
                fps_start_time = fps_end_time
                fps_frame_count = 0
            
            # Duygu analizi yap
            processed_frame = self.detect_emotions(frame)
            
            # Bilgi paneli oluştur
            info_height = 80
            info_panel = np.zeros((info_height, frame.shape[1], 3), dtype=np.uint8)
            
            # FPS ve frame sayısı
            cv2.putText(
                info_panel,
                f"FPS: {fps:.1f}  |  Frame: {self.frame_count}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
            
            # Kullanım talimatı
            cv2.putText(
                info_panel,
                "Cikmak icin 'q' veya ESC tusuna basin",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (200, 200, 200),
                1
            )
            
            # Bilgi panelini frame'e ekle
            combined = np.vstack([info_panel, processed_frame])
            
            # Sonucu göster
            cv2.imshow(window_name, combined)
            
            self.frame_count += 1
            
            # Klavye kontrolü
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' veya ESC
                break
        
        # Temizlik
        cap.release()
        cv2.destroyAllWindows()
        print()
        print("=" * 60)
        print(f"Program sonlandırıldı. Toplam {self.frame_count} frame işlendi.")
        print("=" * 60)


def main():
    """Ana program"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Gerçek zamanlı webcam ile duygu analizi'
    )
    parser.add_argument(
        '--interval', 
        type=int, 
        default=30,
        help='Kaç frame\'de bir duygu analizi yapılacak (varsayılan: 30)'
    )
    
    args = parser.parse_args()
    
    detector = EmotionDetector(analyze_interval=args.interval)
    detector.run()


if __name__ == "__main__":
    main()

