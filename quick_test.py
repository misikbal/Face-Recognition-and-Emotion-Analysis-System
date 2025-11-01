#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hızlı Test Scripti - Kütüphanelerin çalışıp çalışmadığını kontrol eder
"""

print("Kütüphaneler test ediliyor...")
print("-" * 50)

try:
    import cv2
    print("✓ OpenCV başarıyla import edildi")
    print(f"  Versiyon: {cv2.__version__}")
except Exception as e:
    print(f"✗ OpenCV hatası: {e}")

try:
    import tensorflow as tf
    print("✓ TensorFlow başarıyla import edildi")
    print(f"  Versiyon: {tf.__version__}")
except Exception as e:
    print(f"✗ TensorFlow hatası: {e}")

try:
    import numpy as np
    print("✓ NumPy başarıyla import edildi")
    print(f"  Versiyon: {np.__version__}")
except Exception as e:
    print(f"✗ NumPy hatası: {e}")

try:
    import pandas as pd
    print("✓ Pandas başarıyla import edildi")
    print(f"  Versiyon: {pd.__version__}")
except Exception as e:
    print(f"✗ Pandas hatası: {e}")

try:
    from deepface import DeepFace
    print("✓ DeepFace başarıyla import edildi")
except Exception as e:
    print(f"✗ DeepFace hatası: {e}")

print("-" * 50)
print("\nTüm testler tamamlandı!")

