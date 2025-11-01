#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kurulum Kontrol Scripti
Gerekli tüm kütüphanelerin doğru şekilde kurulduğunu kontrol eder.
"""

import sys

def check_imports():
    """Gerekli kütüphaneleri kontrol et"""
    print("=" * 60)
    print("Yüz Tanıma ve Duygu Analizi - Kurulum Kontrolü")
    print("=" * 60)
    print()
    
    required_packages = {
        'cv2': 'opencv-python',
        'deepface': 'deepface',
        'tensorflow': 'tensorflow',
        'numpy': 'numpy',
        'pandas': 'pandas'
    }
    
    all_ok = True
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✓ {package:20s} - Kurulu")
        except ImportError:
            print(f"✗ {package:20s} - KURULU DEĞİL!")
            all_ok = False
    
    print()
    
    if all_ok:
        print("=" * 60)
        print("✓ Tüm kütüphaneler başarıyla kuruldu!")
        print("=" * 60)
        print()
        
        # Webcam kontrolü
        print("Webcam kontrol ediliyor...")
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                print("✓ Webcam başarıyla tespit edildi!")
                ret, frame = cap.read()
                if ret:
                    print(f"✓ Webcam çözünürlüğü: {frame.shape[1]}x{frame.shape[0]}")
                cap.release()
            else:
                print("✗ Webcam açılamadı! Kamera izinlerini kontrol edin.")
        except Exception as e:
            print(f"✗ Webcam kontrolünde hata: {e}")
        
        print()
        print("Sistem hazır! Şimdi şu komutları çalıştırabilirsiniz:")
        print()
        print("  Gerçek zamanlı analiz için:")
        print("    python emotion_detection.py")
        print()
        print("  Görüntü dosyası analizi için:")
        print("    python image_emotion_detection.py resim.jpg")
        print()
    else:
        print("=" * 60)
        print("✗ Bazı kütüphaneler kurulu değil!")
        print("=" * 60)
        print()
        print("Lütfen eksik kütüphaneleri yükleyin:")
        print()
        print("  pip install -r requirements.txt")
        print()
        sys.exit(1)


def main():
    """Ana fonksiyon"""
    try:
        check_imports()
    except KeyboardInterrupt:
        print("\n\nKontrol iptal edildi.")
        sys.exit(0)


if __name__ == "__main__":
    main()

