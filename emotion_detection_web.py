#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yüz Tanıma ve Duygu Analizi - Web Arayüzü
Tarayıcıda gerçek zamanlı webcam görüntüsü ile duygu analizi
"""

from flask import Flask, render_template, Response, jsonify
import cv2
from deepface import DeepFace
import numpy as np
import time
import json

app = Flask(__name__)

class EmotionDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.frame_count = 0
        self.last_emotions = {}
        self.analyze_interval = 15  # Her 15 frame'de bir analiz
        
        # Duygu renkleri (BGR formatında)
        self.emotion_colors = {
            'happy': (0, 255, 0),
            'sad': (255, 0, 0),
            'angry': (0, 0, 255),
            'surprise': (0, 255, 255),
            'fear': (128, 0, 128),
            'disgust': (0, 128, 128),
            'neutral': (255, 255, 255)
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
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        
        for face_idx, (x, y, w, h) in enumerate(faces):
            face_key = f"face_{face_idx}"
            should_analyze = (self.frame_count % self.analyze_interval == 0)
            
            if should_analyze:
                face_roi = frame[y:y+h, x:x+w]
                try:
                    result = DeepFace.analyze(
                        face_roi, 
                        actions=['emotion'],
                        enforce_detection=False,
                        silent=True
                    )
                    if isinstance(result, list):
                        result = result[0]
                    
                    self.last_emotions[face_key] = {
                        'dominant': result['dominant_emotion'],
                        'scores': result['emotion']
                    }
                except:
                    if face_key not in self.last_emotions:
                        self.last_emotions[face_key] = {
                            'dominant': 'neutral',
                            'scores': {}
                        }
            
            if face_key in self.last_emotions:
                emotion_data = self.last_emotions[face_key]
                emotion = emotion_data['dominant']
                scores = emotion_data['scores']
                
                color = self.emotion_colors.get(emotion, (255, 255, 255))
                emotion_tr = self.emotion_tr.get(emotion, emotion)
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
                cv2.putText(frame, emotion_tr, (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
                
                if scores:
                    sorted_emotions = sorted(scores.items(), 
                                           key=lambda x: x[1], reverse=True)[:3]
                    y_offset = y + h + 25
                    for emo, score in sorted_emotions:
                        emo_tr = self.emotion_tr.get(emo, emo)
                        text = f"{emo_tr}: {score:.1f}%"
                        cv2.putText(frame, text, (x, y_offset), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        y_offset += 20
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
                cv2.putText(frame, "Analiz ediliyor...", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame

detector = EmotionDetector()
camera = None

def get_camera():
    global camera
    if camera is None or not camera.isOpened():
        camera = cv2.VideoCapture(0)
    return camera

def generate_frames():
    while True:
        camera = get_camera()
        success, frame = camera.read()
        if not success:
            break
        
        detector.frame_count += 1
        processed_frame = detector.detect_emotions(frame)
        
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    html = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yüz Tanıma ve Duygu Analizi</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 30px;
            max-width: 1200px;
            width: 100%;
        }
        
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        .video-container {
            position: relative;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            background: #000;
        }
        
        #video-feed {
            width: 100%;
            height: auto;
            display: block;
        }
        
        .info-panel {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 10px;
            background: white;
            border-radius: 5px;
        }
        
        .emotion-legend {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 20px;
        }
        
        .emotion-item {
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            color: white;
        }
        
        .happy { background: linear-gradient(135deg, #00ff00, #00cc00); }
        .sad { background: linear-gradient(135deg, #0000ff, #0000cc); }
        .angry { background: linear-gradient(135deg, #ff0000, #cc0000); }
        .surprise { background: linear-gradient(135deg, #ffff00, #cccc00); color: #333; }
        .fear { background: linear-gradient(135deg, #800080, #600060); }
        .disgust { background: linear-gradient(135deg, #008080, #006060); }
        .neutral { background: linear-gradient(135deg, #ffffff, #e0e0e0); color: #333; }
        
        .footer {
            text-align: center;
            margin-top: 20px;
            color: white;
            font-size: 0.9em;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .status {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #00ff00;
            animation: pulse 2s infinite;
            margin-right: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 Yüz Tanıma ve Duygu Analizi</h1>
        <p class="subtitle">
            <span class="status"></span>
            Gerçek Zamanlı Webcam Görüntüsü
        </p>
        
        <div class="video-container">
            <img id="video-feed" src="{{ url_for('video_feed') }}" alt="Webcam Feed">
        </div>
        
        <div class="info-panel">
            <h3>📊 Duygu Renk Kodları</h3>
            <div class="emotion-legend">
                <div class="emotion-item happy">😊 Mutlu</div>
                <div class="emotion-item sad">😢 Üzgün</div>
                <div class="emotion-item angry">😠 Kızgın</div>
                <div class="emotion-item surprise">😲 Şaşkın</div>
                <div class="emotion-item fear">😨 Korkmuş</div>
                <div class="emotion-item disgust">🤢 İğrenmiş</div>
                <div class="emotion-item neutral">😐 Nötr</div>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background: #e7f3ff; border-radius: 8px; border-left: 4px solid #667eea;">
                <strong>💡 Kullanım İpuçları:</strong>
                <ul style="margin-left: 20px; margin-top: 10px; line-height: 1.8;">
                    <li>Yüzünüzü kameraya net bir şekilde gösterin</li>
                    <li>İyi aydınlatma altında olun</li>
                    <li>Farklı mimikler yaparak sistemi test edin</li>
                    <li>Sistem gerçek zamanlı analiz yapıyor</li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Python + DeepFace + Flask ile geliştirilmiştir</p>
        <p>Çıkmak için terminalde Ctrl+C yapın</p>
    </div>
</body>
</html>
    '''
    return html

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    print("\n" + "=" * 60)
    print("🎭 Yüz Tanıma ve Duygu Analizi - Web Arayüzü")
    print("=" * 60)
    print()
    print("Sunucu başlatılıyor...")
    print()
    print("Tarayıcınızda şu adresi açın:")
    print()
    print("    👉 http://localhost:5000")
    print()
    print("veya")
    print()
    print("    👉 http://127.0.0.1:5000")
    print()
    print("Durdurmak için Ctrl+C yapın")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

if __name__ == '__main__':
    main()

