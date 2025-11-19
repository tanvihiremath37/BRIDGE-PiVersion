import pyttsx3

# Initialize offline TTS engine
engine = pyttsx3.init()

# Optional: Tune the voice
engine.setProperty("rate", 150)      # speaking speed
engine.setProperty("volume", 1.0)    # max volume


def speak_text(text):
    """
    Offline Text → Speech using pyttsx3  
    Works on Windows & Raspberry Pi.
    """
    if not text or text.strip() == "":
        return

    print(f"🔊 Speaking: {text}")
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    speak_text("Text to speech module is working.")
