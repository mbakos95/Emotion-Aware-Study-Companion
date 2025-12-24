import time
import cv2
import threading

from camera import CameraEmotionDetector
from audio_monitor import AudioMonitor
from affective_state import AffectiveState
from llm_agent import LLMAgent
from speech_input import SpeechInput
from speech_output import SpeechOutput
from report_generator import StudyReport

# -------------------------
# Initialization
# -------------------------
cam = CameraEmotionDetector()
audio = AudioMonitor()
state = AffectiveState()
llm = LLMAgent()
speech = SpeechInput()
speaker = SpeechOutput()
report = StudyReport()

audio.start()
running = True

print("Emotion-Aware Study Companion started")
print("Press ENTER to talk | Ctrl+C to exit")


# -------------------------
# CAMERA LOOP (NON-BLOCKING)
# -------------------------
def camera_loop():
    global running

    window_name = "Affective Camera (Demo)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while running:
        emotions, frame = cam.read_emotion()
        if frame is None:
            continue

        voice_fatigue = audio.is_fatigued()
        state.update(emotions, voice_fatigue)

        peek = state.summarize()  # or state.peek()

        cv2.putText(frame, f"Valence: {peek['avg_valence']:.2f}",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.putText(frame, f"Arousal: {peek['avg_arousal']:.2f}",
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.putText(frame, f"Voice fatigue ratio: {peek['voice_fatigue_ratio']:.2f}",
                    (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 255), 2)
        
        cv2.putText(frame, f"Voice fatigue raw: {peek['voice_fatigue_ratio_raw']:.2f}",
            (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 255), 2)

        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            running = False
            break

    cv2.destroyAllWindows()




# -------------------------
# INTERACTION LOOP
# -------------------------
def interaction_loop():
    global running
    try:
        while running:
            input("\n[Press ENTER to talk] ")

            text = speech.listen()
            if not text or not text.strip():
                print("No speech detected. Try again.")
                continue

            import json
            summary = state.summarize()

            print("\n[DEBUG] Affective summary sent to LLM:")
            print(json.dumps(summary, indent=2, ensure_ascii=False))

            print("\n[DEBUG] User text sent to LLM:")
            print(text)

            try:
                response = llm.get_recommendation(summary, text)
            except Exception as e:
                print(f"LLM call failed: {repr(e)}")
                continue

            print("\nRecommendation:")
            print(response)

            speaker.speak(response)

            report.add(
                affective_summary=summary,
                user_text=text,
                llm_response=response
            )

    except KeyboardInterrupt:
        running = False



# -------------------------
# RUN THREADS
# -------------------------
camera_thread = threading.Thread(target=camera_loop, daemon=True)
camera_thread.start()

interaction_loop()

# -------------------------
# CLEANUP
# -------------------------
audio.stop()
cam.release()
filename = report.export()
print(f"\nStudy feedback report saved as: {filename}")
