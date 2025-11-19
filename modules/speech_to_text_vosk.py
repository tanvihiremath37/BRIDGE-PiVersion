# modules/speech_to_text_vosk.py
import os, json, sounddevice as sd
from vosk import Model, KaldiRecognizer

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models/vosk-model")
MIC_DEVICE = 1  # update this if needed (use `arecord -l`)

def listen_and_transcribe(duration=5):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Vosk model missing in models/vosk-model/")
    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, 16000)
    fs = 16000

    print("🎙 Listening... Speak now.")
    recording = sd.rec(int(duration * fs),
                       samplerate=fs,
                       channels=1,
                       dtype="int16",
                       device=MIC_DEVICE)
    sd.wait()
    data = recording.tobytes()

    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())
    else:
        res = json.loads(rec.FinalResult())

    text = res.get("text", "")
    print(f"🧾 Recognized (offline): {text}")
    return text.lower().strip()
