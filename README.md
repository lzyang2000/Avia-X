# Avia-X
Avia-X: Real-time Passenger Experience System  
Daher General Aviathon Team 15, 1st Place in User Experience

This repo contains an interface with a control panel and info display panel. It supports login from one user. The user can set, modify and customize their preferences. It also responds to user's emotion captured from the device's webcam.

In addition to the user interface, we have built a Raspberry Pi circuit that supports input from Picamera, light and pressure sensors and output with LED light and music player.

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

### User Interface

Run the following launch script to start the user interface:
```bash
python3 final_launch.py
```

To run on the Raspberry Pi circuit, run
```bash
python3 final_launch.py rpi=True
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

## Citations
<b id="f1">[1]</b> https://github.com/oarriaga/face_classification [↩](#a1)

