from collections import deque
import time

class AffectiveState:
    def __init__(self, max_history=50):
        self.history = deque(maxlen=max_history)

    def update(self, face_emotion, voice_fatigue):
        """
        Called continuously (per frame / cycle)
        """
        if not face_emotion:
            return

        valence = (
            face_emotion.get("happy", 0)
            - face_emotion.get("sad", 0)
            - face_emotion.get("angry", 0)
        )

        arousal = (
            face_emotion.get("angry", 0)
            + face_emotion.get("happy", 0)
            - face_emotion.get("neutral", 0)
        )

        self.history.append({
            "time": time.time(),
            "valence": valence,
            "arousal": arousal,
            "voice_fatigue": voice_fatigue
        })

    def peek(self):
        """
        Lightweight snapshot for UI / demo
        """
        if not self.history:
            return {
                "avg_valence": 0.0,
                "avg_arousal": 0.0,
                "voice_fatigue_ratio": 0.0
            }

        valences = [x["valence"] for x in self.history]
        arousals = [x["arousal"] for x in self.history]
        voice = [x["voice_fatigue"] for x in self.history]

        return {
            "avg_valence": sum(valences) / len(valences),
            "avg_arousal": sum(arousals) / len(arousals),
            "voice_fatigue_ratio": sum(voice) / len(voice)
        }

    def summarize(self):
        """
        Heavier summary for LLM & reports
        """
        snap = self.peek()

        if snap["avg_valence"] < -0.3 and snap["voice_fatigue_ratio"] > 0.5:
            state = "Sustained fatigue"
        elif snap["avg_valence"] < -0.3:
            state = "Negative mood"
        else:
            state = "Neutral / engaged"

        snap["state"] = state
        return snap
