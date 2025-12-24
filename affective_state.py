from collections import deque
import time

class AffectiveState:
    def __init__(self, max_history=50, voice_weight=0.5):
        self.history = deque(maxlen=max_history)
        self.voice_weight = float(voice_weight)

    def update(self, face_emotion, voice_fatigue):
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
        if not self.history:
            return {
                "avg_valence": 0.0,
                "avg_arousal": 0.0,
                "voice_fatigue_ratio_raw": 0.0,
                "voice_fatigue_ratio": 0.0,  # weighted
            }

        valences = [x["valence"] for x in self.history]
        arousals = [x["arousal"] for x in self.history]
        voice = [x["voice_fatigue"] for x in self.history]

        raw = sum(voice) / len(voice)                  # 0..1
        weighted = raw * self.voice_weight             # halve influence

        return {
            "avg_valence": sum(valences) / len(valences),
            "avg_arousal": sum(arousals) / len(arousals),
            "voice_fatigue_ratio_raw": raw,
            "voice_fatigue_ratio": weighted,
        }

    def summarize(self):
        snap = self.peek()

        # Use the *weighted* ratio for decisions
        if snap["avg_valence"] < -0.3 and snap["voice_fatigue_ratio"] > 0.5:
            state = "Sustained fatigue"
        elif snap["avg_valence"] < -0.3:
            state = "Negative mood"
        else:
            state = "Neutral / engaged"

        snap["state"] = state
        snap["voice_weight"] = self.voice_weight
        return snap
