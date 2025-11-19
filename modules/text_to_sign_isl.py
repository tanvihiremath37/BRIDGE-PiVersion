import numpy as np
import matplotlib.pyplot as plt
import cv2
from easygui import *
import os
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string
import json
import sounddevice as sd

# -----------------------------
# OFFLINE SPEECH RECOGNITION (VOSK)
# -----------------------------
from vosk import Model, KaldiRecognizer

VOSK_MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models",
    "vosk-model"
)

vosk_model = Model(VOSK_MODEL_PATH)
recognizer = KaldiRecognizer(vosk_model, 16000)

# ---------------------------------
# RECORD AUDIO WITHOUT PYAUDIO
# ---------------------------------
def record_audio(seconds=4, samplerate=16000):
    print("Listening...")
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate,
                   channels=1, dtype='int16')
    sd.wait()
    return audio.tobytes()

# -----------------------------
# MAIN FUNCTION (same logic)
# -----------------------------
def func():

    isl_gif = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
                'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office',
                'do you have money', 'do you want something to drink', 'do you want tea or coffee', 'do you watch TV',
                'dont worry', 'flower is beautiful', 'good afternoon', 'good evening', 'good morning', 'good night',
                'good question', 'had your lunch', 'happy journey', 'hello what is your name',
                'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing', 'i am fine',
                'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre',
                'i love to shop', 'i had to say something but i forgot', 'i have headache', 'i like pink colour',
                'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker', 'my name is john',
                'nice to meet you', 'no smoking please', 'open the door', 'please call me later', 'please clean the room',
                'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime',
                'shall I help you', 'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up',
                'take care', 'there was traffic jam', 'wait I am thinking', 'what are you doing', 'what is the problem',
                'what is todays date', 'what is your father do', 'what is your job', 'what is your mobile number',
                'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
                'where is the bathroom', 'where is the police station', 'you are wrong', 'address', 'agra', 'ahemdabad',
                'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras', 'banglore', 'bihar',
                'bihar', 'bridge', 'cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut',
                'crocodile', 'dasara', 'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday',
                'fruits', 'glass', 'grapes', 'gujrat', 'hello', 'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job',
                'july', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango', 'may', 'mile', 'monday', 'mumbai',
                'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station', 'post office',
                'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep',
                'southafrica', 'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato',
                'town', 'tuesday', 'usa', 'village', 'voice', 'wednesday', 'weight', 'please wait for sometime',
                'what is your mobile number', 'what are you doing', 'are you busy']

    arr = list(string.ascii_lowercase)

    while True:
        try:
            data = record_audio()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                a = result.get("text", "")
            else:
                result = json.loads(recognizer.PartialResult())
                a = result.get("partial", "")

            a = a.lower()
            print("You Said:", a)

            # punctuation remove
            for c in string.punctuation:
                a = a.replace(c, "")

            if a in ["goodbye", "good bye", "bye"]:
                print("Exiting...")
                break

            # -------------------------
            # GIF DISPLAY
            # -------------------------
            if a in isl_gif:

                class ImageLabel(tk.Label):
                    """plays gif"""
                    def load(self, im):
                        if isinstance(im, str):
                            im = Image.open(im)
                        self.frames = []
                        try:
                            for i in count(1):
                                self.frames.append(ImageTk.PhotoImage(im.copy()))
                                im.seek(i)
                        except EOFError:
                            pass

                        try:
                            self.delay = im.info['duration']
                        except:
                            self.delay = 100

                        if len(self.frames) == 1:
                            self.config(image=self.frames[0])
                        else:
                            self.next_frame()

                    def next_frame(self):
                        if self.frames:
                            self.loc = (getattr(self, 'loc', 0) + 1) % len(self.frames)
                            self.config(image=self.frames[self.loc])
                            self.after(self.delay, self.next_frame)

                root = tk.Tk()
                lbl = ImageLabel(root)
                lbl.pack()

                gif_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "ISL_Gifs",
                    f"{a}.gif"
                )

                if os.path.exists(gif_path):
                    lbl.load(gif_path)
                    root.mainloop()
                else:
                    print("GIF not found:", gif_path)

            # -------------------------
            # LETTER FALLBACK
            # -------------------------
            else:
                for ch in a:
                    if ch in arr:
                        img_path = os.path.join(
                            os.path.dirname(os.path.dirname(__file__)),
                            "letters",
                            f"{ch}.jpg"
                        )

                        if os.path.exists(img_path):
                            img = Image.open(img_path)
                            img_np = np.asarray(img)
                            plt.imshow(img_np)
                            plt.draw()
                            plt.pause(0.8)

        except Exception as e:
            print("Error:", e)

        plt.close()

# --------------- RUN LOOP ----------------
while True:
    image = "signlang.png"
    msg = "HEARING IMPAIRMENT ASSISTANT"
    choices = ["Live Voice", "All Done!"]
    reply = buttonbox(msg, image=image, choices=choices)

    if reply == choices[0]:
        func()
    if reply == choices[1]:
        quit()
