import serial
import time

# Auto-detect port on Raspberry Pi
PORT = "/dev/ttyACM0"   # may become /dev/ttyUSB0 on your Pi
BAUD = 9600

def send_to_braille(text):
    try:
        arduino = serial.Serial(PORT, BAUD, timeout=1)
        time.sleep(2)  # wait for Arduino reset
        print("Connected to Arduino")

        text = text.lower().strip()
        print(f"Sending: {text}")

        arduino.write((text + "\n").encode())
        time.sleep(0.5)

        arduino.close()

    except Exception as e:
        print("Braille error:", e)
