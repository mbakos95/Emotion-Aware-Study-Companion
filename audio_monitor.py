import sounddevice as sd
import numpy as np
from collections import deque

class AudioMonitor:
    def __init__(self, window=10, threshold=5):
        self.energy_window = deque(maxlen=window)
        self.threshold = threshold

    def audio_callback(self, indata, frames, time, status):
        energy = np.linalg.norm(indata) * 10
        self.energy_window.append(energy)

    def start(self):
        self.stream = sd.InputStream(
            callback=self.audio_callback,
            channels=1,
            samplerate=16000
        )
        self.stream.start()

    def is_fatigued(self):
        if len(self.energy_window) < self.energy_window.maxlen:
            return False
        return sum(self.energy_window) / len(self.energy_window) < self.threshold

    def stop(self):
        self.stream.stop()
