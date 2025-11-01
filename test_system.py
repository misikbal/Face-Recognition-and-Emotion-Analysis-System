#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistem Test Scripti - Tüm bileşenlerin çalıştığını doğrular
"""

import sys
import os

def test_imports():
    """Kütüphaneleri test et"""
    print("=" * 60)
    print("1. Kütüphane Testi")
    print("=" * 60)
    
    try:
        import cv2
        print(f"✓ OpenCV: {cv2.__version__}")
    except Exception as e:
        print(f"✗ OpenCV hatası: {e}")
        return False
    
    try:
        import tensorflow as tf
        print(f"✓ TensorFlow: {tf.__version__}")
    except Exception as e:
        print(f"✗ TensorFlow hatası: {e}")
        return False
    
    try:
        from deepface import DeepFace
        print(f"✓ DeepFace: Yüklendi")
    except Exception as e:
        print(f"✗ DeepFace hatası: {e}")
        return False
    
    print()
    return True


def test_face_cascade():
    """Yüz tanıma modelini test et"""
    print("=" * 60)
    print("2. Yüz Tanıma Modeli Testi")
    print("=" * 60)
    
    try:
        import cv2
        cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        if cascade.empty():
            print("✗ Haar Cascade yüklenemedi!")
            return False
        print("✓ Haar Cascade yüklendi")
    except Exception as e:
        print(f"✗ Hata: {e}")
        return False
    
    print()
    return True


def test_webcam():
    """Webcam erişimini test et"""
    print("=" * 60)
    print("3. Webcam Testi")
    print("=" * 60)
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Webcam açılamadı!")
            print("  Webcam bağlı ve izinler verilmiş olduğundan emin olun.")
            return False
        
        ret, frame = cap.read()
        if not ret or frame is None:
            print("✗ Frame okunamadı!")
            cap.release()
            return False
        
        height, width = frame.shape[:2]
        print(f"✓ Webcam çalışıyor")
        print(f"  Çözünürlük: {width}x{height}")
        print(f"  FPS: {cap.get(cv2.CAP_PROP_FPS)}")
        
        cap.release()
    except Exception as e:
        print(f"✗ Webcam hatası: {e}")
        return False
    
    print()
    return True


def test_deepface_model():
    """DeepFace modelini test et"""
    print("=" * 60)
    print("4. DeepFace Modeli Testi")
    print("=" * 60)
    print("DeepFace modellerini indiriyor (ilk çalıştırmada zaman alır)...")
    
    try:
        import numpy as np
        from deepface import DeepFace
        
        # Test için sahte bir yüz görüntüsü oluştur
        test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        # DeepFace analizi
        result = DeepFace.analyze(
            test_image,
            actions=['emotion'],
            enforce_detection=False,
            silent=True
        )
        
        print("✓ DeepFace modeli çalışıyor")
        print(f"  Tespit edilen duygular: {list(result[0]['emotion'].keys())}")
    except Exception as e:
        print(f"✗ DeepFace hatası: {e}")
        return False
    
    print()
    return True


def main():
    """Ana test fonksiyonu"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "Yüz Tanıma Sistemi - Tam Test" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    tests = [
        ("Kütüphane Yükleme", test_imports),
        ("Yüz Tanıma Modeli", test_face_cascade),
        ("Webcam Erişimi", test_webcam),
        ("DeepFace Modeli", test_deepface_model),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} testi başarısız: {e}\n")
            results.append((name, False))
    
    # Özet
    print("=" * 60)
    print("TEST SONUÇLARI")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ Başarılı" if result else "✗ Başarısız"
        print(f"{name:25s}: {status}")
    
    print()
    
    if all(r[1] for r in results):
        print("╔" + "=" * 58 + "╗")
        print("║" + " " * 10 + "✓ TÜM TESTLER BAŞARILI!" + " " * 23 + "║")
        print("╚" + "=" * 58 + "╝")
        print()
        print("Sistem kullanıma hazır! Şunları deneyebilirsiniz:")
        print()
        print("  1. Görüntü analizi:")
        print("     python image_emotion_detection.py resim.jpg")
        print()
        print("  2. Webcam kaydı:")
        print("     python emotion_detection_webcam.py")
        print()
        return 0
    else:
        print("⚠ Bazı testler başarısız oldu.")
        print("Lütfen hataları kontrol edin ve düzeltin.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

