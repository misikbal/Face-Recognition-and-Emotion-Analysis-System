#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yüz Tanıma ve Duygu Analizi Sistemi - Webcam Video Kaydedici Versiyon
Headless sistemler için (GUI olmadan çalışır, video dosyasına kaydeder)
"""

import cv2
from deepface import DeepFace
import numpy as np
from datetime import datetime
import os

class EmotionDetector:
    def __init__(self, save_video=True):
        """Duygu algılama sınıfını başlat"""
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.save_video = save_video
        
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
            İşlenmiş görüntü frame'i ve duygu bilgisi
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
        
        emotions_detected = []
        
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
                emotions_detected.append(emotion)
                
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
        
        return frame, emotions_detected
    
    def run(self, duration=30):
        """
        Webcam'den görüntü al ve duygu analizi yap
        
        Args:
            duration: Kayıt süresi (saniye), None ise sınırsız
        """
        # Webcam'i başlat
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Hata: Kamera açılamadı!")
            return
        
        # Video özellikleri
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 20
        
        # Video kaydedici
        video_writer = None
        if self.save_video:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"emotion_analysis_{timestamp}.avi"
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            video_writer = cv2.VideoWriter(
                output_filename, 
                fourcc, 
                fps, 
                (frame_width, frame_height)
            )
            print(f"Video kaydediliyor: {output_filename}")
        
        print("Duygu Analizi Sistemi Başlatıldı")
        if duration:
            print(f"Kayıt süresi: {duration} saniye")
        print("Durdurmak için Ctrl+C yapın")
        print("-" * 50)
        
        frame_count = 0
        max_frames = duration * fps if duration else None
        
        try:
            while True:
                # Frame oku
                ret, frame = cap.read()
                
                if not ret:
                    print("Hata: Frame okunamadı!")
                    break
                
                # Duygu analizi yap
                processed_frame, emotions = self.detect_emotions(frame)
                
                # Bilgi ekle
                info_text = f"Frame: {frame_count} | Yuzler: {len(emotions)}"
                cv2.putText(
                    processed_frame,
                    info_text,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )
                
                # Duygular tespit edildiyse yazdır
                if emotions:
                    emotions_str = ", ".join([self.emotion_tr.get(e, e) for e in emotions])
                    print(f"Frame {frame_count}: {emotions_str}")
                
                # Video dosyasına kaydet
                if video_writer:
                    video_writer.write(processed_frame)
                
                frame_count += 1
                
                # Süre kontrolü
                if max_frames and frame_count >= max_frames:
                    print(f"\n{duration} saniye tamamlandı!")
                    break
                
        except KeyboardInterrupt:
            print("\n\nKullanıcı tarafından durduruldu.")
        
        finally:
            # Temizlik
            cap.release()
            if video_writer:
                video_writer.release()
            print(f"\nToplam {frame_count} frame işlendi.")
            if self.save_video:
                print(f"Video kaydedildi: {output_filename}")


def main():
    """Ana program"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Webcam ile duygu analizi')
    parser.add_argument(
        '--duration', 
        type=int, 
        default=30,
        help='Kayıt süresi (saniye), 0 = sınırsız (varsayılan: 30)'
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Video kaydetme'
    )
    
    args = parser.parse_args()
    
    duration = None if args.duration == 0 else args.duration
    save_video = not args.no_save
    
    detector = EmotionDetector(save_video=save_video)
    detector.run(duration=duration)


if __name__ == "__main__":
    main()

