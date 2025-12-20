import pyttsx3

class SpeechOutput:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)   # speed
        self.engine.setProperty("volume", 1.0)

    def speak(self, text):
        print("🔊 Speaking...")
        self.engine.say(text)
        self.engine.runAndWait()
