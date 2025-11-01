#!/bin/bash
# OpenCV sorununu düzeltmek için alternatif kurulum

echo "OpenCV sorunu düzeltiliyor..."
echo ""

source venv/bin/activate

# Mevcut opencv-python'u kaldır
pip uninstall -y opencv-python opencv-python-headless 2>/dev/null

# opencv-python-headless yükle (GUI bağımlılıkları olmadan)
pip install opencv-python-headless==4.8.1.78

echo ""
echo "✓ opencv-python-headless kuruldu"
echo ""
echo "NOT: Bu sürüm GUI gösterimi desteklemez."
echo "Programı test etmek için 'python quick_test.py' çalıştırın"

