![Status: In Progress](https://img.shields.io/badge/Status-In%20Progress-yellow)
BRIDGE – Assistive Multi-Modal Communication Device
Sign Language ↔ Speech ↔ Text ↔ Braille Translator
Designed for Deaf, Mute, and Blind Accessibility
Overview

BRIDGE is an integrated assistive communication system that enables seamless interaction between individuals with hearing, speech, and visual disabilities. It uses a Raspberry Pi 4, Arduino-driven refreshable Braille output, vision-based sign detection, offline speech recognition, and a custom touchscreen interface.

The system converts information across multiple modalities:
Sign Language to Text
Speech to Sign Language (GIFs)
Text to Sign Language
Text to Braille (using an Arduino braille cell)
Speech to Text
Text to Speech
User Profiles for accessibility customization
The device runs fully offline, making it suitable for low-connectivity environments.

System Features
1. Sign-to-Text (ASL/ISL)

Uses Mediapipe Hand Landmarks
Random Forest classifier
Works with standard USB camera or Pi Camera
Displays recognized characters/words on the touchscreen

2. Speech-to-Sign Language

Offline recognition using VOSK
Maps recognized words/phrases to pre-stored ISL GIF animations
Displays animations full-screen with looped playback

3. Text-to-Sign Language

Converts typed text into alphabet GIFs or word-level ISL GIFs
Supports fallback to character-by-character if GIF unavailable

4. Text-to-Braille Output

Sends text to Arduino via serial
Arduino drives 6-pin solenoid braille cell
User presses a physical button to load next character
Designed for tactile readability and low power draw

5. Speech-to-Text

Offline using VOSK English Model
Displays recognized text on the touchscreen
Can be forwarded to Braille output or sign GIFs

6. Text-to-Speech

Uses an offline TTS engine
Helps mute individuals communicate verbally
Configurable voice output

7. User Profile Setup

Profiles control:
Preferred input mode (sign/speech/text)
Output mode (text/sign/braille/voice)
Accessibility options
Profiles are stored in a JSON file and loaded automatically on boot.

Hardware Requirements:

Raspberry Pi 4B	Main computation and GUI
4.3" DSI Touchscreen (800x480)	Main UI
Pi Camera or USB Camera	Sign recognition
USB Microphone + Speaker (via splitter)	Speech I/O
Arduino UNO	Braille cell driver
Solenoid vibration motors (6x)	Braille dots
NMOS (IRFZ44N)	Drives solenoids
1N4007 diodes	Back-EMF protection
Breadboard + jumpers	Circuit assembly
5V/9V power bank	Portable power


How to Run
1. Install dependencies
pip install -r requirements.txt

2. Run the UI
python gui/main_ui.py

3. Upload Arduino Code

Upload the provided .ino file through Arduino IDE.

4. Connect Arduino to Raspberry Pi

The Pi communicates via USB-Serial (/dev/ttyACM0).

How to use:
Home Screen
Touchscreen-based
Mascot animation
Large pink rounded-corner buttons
Modes
Select your mode from the menu
Corresponding module runs full-screen
Press Back to return home


If you wish to extend the project:
Add more GIFs
Train a better sign classifier
Expand braille cell to multi-cell
Add Hindi or regional language speech models
