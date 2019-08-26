# Avia-X
Avia-X: Real-time Supervised Aviation Experience System  
The General Aviathon Team 15

## Installation
Clone the repo on your device:
```bash
git clone https://github.com/lzyang2000/Avia-X.git
```

## Usage

First, run 
```bash
pip install -r requirements.txt
```

### Emotion Recognition Demo

TensorFlow model for emotion recognition, using a face object detector to localize faces and runs a emotion classifier on each face<sup id="a1">[1](#f1)</sup>.

If you are running on a Raspberry Pi, install picamera:
```bash
pip install picamera
```

To start the demo, run
```bash
source demo.sh
```

### Mock User Interface

Run the following launch script to start a mock user agent:
```bash
python3 launch.py
```

## Citations
<b id="f1">[1]</b> https://github.com/oarriaga/face_classification [↩](#a1)

