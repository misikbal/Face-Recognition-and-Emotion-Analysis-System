#!/bin/bash
# Yüz Tanıma ve Duygu Analizi Sistemi - Kurulum Scripti

echo "=========================================="
echo "Yüz Tanıma ve Duygu Analizi Sistemi"
echo "Kurulum Başlıyor..."
echo "=========================================="
echo ""

# Python kontrolü
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 bulunamadı! Lütfen Python 3.8 veya üzerini yükleyin."
    exit 1
fi

echo "✓ Python bulundu: $(python3 --version)"
echo ""

# Sanal ortam oluştur
echo "📦 Sanal ortam oluşturuluyor..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Sanal ortam oluşturulamadı!"
    echo "Lütfen python3-venv paketini yükleyin:"
    echo "  sudo apt install python3-venv  (Ubuntu/Debian)"
    exit 1
fi

echo "✓ Sanal ortam oluşturuldu"
echo ""

# Sanal ortamı aktifleştir
echo "🔄 Sanal ortam aktifleştiriliyor..."
source venv/bin/activate

# pip güncellemesi
echo "📦 pip güncelleniyor..."
pip install --upgrade pip > /dev/null 2>&1

# Bağımlılıkları yükle
echo "📦 Gerekli kütüphaneler yükleniyor..."
echo "   (Bu işlem birkaç dakika sürebilir...)"
echo ""

pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Kütüphaneler yüklenemedi!"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Kurulum tamamlandı!"
echo "=========================================="
echo ""

# Kurulum kontrolü
echo "🔍 Kurulum kontrol ediliyor..."
python check_setup.py

echo ""
echo "Kullanmak için sanal ortamı aktifleştirin:"
echo "  source venv/bin/activate"
echo ""
echo "Ardından programı çalıştırın:"
echo "  python emotion_detection.py"
echo ""

