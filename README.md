![Status: In Progress](https://img.shields.io/badge/Status-In%20Progress-yellow)
BRIDGE – Autonomous Raspberry Pi Accessibility System

BRIDGE is an offline-first, multimodal accessibility system designed for the Raspberry Pi 4 with a 4.3-inch touchscreen.
This version operates autonomously and supports sign language recognition, braille output, text-based communication, and speech-based modules.

1. System Features
1.1 Sign to Text

Uses MediaPipe Hand Landmark Detector and a custom trained classification model.

Recognizes A–Z and selected sign language gestures.

Live camera feed with bounding box and predicted label overlay.

1.2 Speech to Sign

Offline automatic speech recognition using VOSK.

Converts recognized text to:

Pre-recorded sign language GIFs for known phrases

Letter-by-letter display for general text

Automatic GIF window focus.

1.3 Text to Sign

Displays full ISL GIFs for supported phrases.

Displays alphabet images for individual characters.

Compatible with both lowercase and uppercase input.

1.4 Speech to Text

Offline speech-to-text conversion using VOSK.

5-second buffered audio recording.

Output displayed in a scrollable textbox.

1.5 Text to Speech

Cloud-based text-to-speech using Google gTTS.

MP3 playback through pygame audio backend.

Temporary audio file automatically deleted after playback.(pyttsx for offline)

1.6 Text to Braille Output

Sends text to an Arduino-based Refreshable Braille cell.

Each character is converted to a 6-bit Braille pattern:

1 4
2 5
3 6


Arduino controls six solenoids (one per dot).



2. Hardware Requirements
2.1 Raspberry Pi Module

Raspberry Pi 4 Model B (4 GB recommended)

USB Camera

4.3-inch Raspberry Pi Touchscreen (800 × 480)

MicroSD card (32 GB or higher)

USB A-to-B cable (for Arduino communication)

2.2 Braille Display Hardware (Arduino Unit)

The Braille module consists of a single 6-dot refreshable cell.

Microcontroller

Arduino Uno or Arduino Nano

Actuators(here-coin vibrators)

6 × nos

Switching Components

6 × IRFZ44N N-Channel MOSFETs

Used to drive each solenoid independently

6 × 1N4007 diodes

Flyback protection for solenoid coils

6 × 220 Ω gate resistors (optional but recommended)

Input Devices

1 × Tactile pushbutton (advance to next character)

Power

External 5V supply capable of driving 6 solenoids

Common ground shared between Arduino and MOSFET source pins

Connections

MOSFET drain → solenoid negative

Solenoid positive → +5V

MOSFET source → GND

1N4007 diode across solenoid (reverse biased)

Arduino digital pins 2–7 → MOSFET gates

Arduino pin 8 → pushbutton input


3. Installation Instructions (Raspberry Pi)
3.1 System Dependencies
sudo apt update
sudo apt install python3-pip python3-pil python3-tk \
                 portaudio19-dev espeak

3.2 Python Dependencies
pip3 install pygame numpy mediapipe opencv-python vosk \
             sounddevice gTTS pillow matplotlib pyserial

4. Autostart Configuration

To launch BRIDGE automatically on boot:

sudo nano /etc/xdg/lxsession/LXDE-pi/autostart


Add this line:

@/usr/bin/python3 /home/pi/Desktop/projects/BRIDGE/gui/main_ui.py


Save and reboot.

5. Braille Module Communication
Raspberry Pi → Arduino

Serial port: /dev/ttyACM0

Baud rate: 9600

Each text request ends with a newline (\n)

Arduino processes text character-by-character

Waits for tactile button press before advancing

Arduino Responsibilities

Map each letter to its 6-bit Braille array

Activate motors through MOSFETs according to the pattern

Move to the next character

6. Author

Tanvi Basavaraj Hiremath
Autonomous Raspberry Pi Implementation of BRIDGE Accessibility System
