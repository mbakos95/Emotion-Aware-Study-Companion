import streamlit as st
import cv2
import time
import numpy as np
import sounddevice as sd
from fer import FER
from collections import deque, Counter
from openai import OpenAI

# =================================================
# CONFIGURATION
# =================================================
WINDOW_SIZE = 15            # frames for facial smoothing
AUDIO_WINDOW = 10           # audio energy window
TIME_WINDOW = 10            # seconds for affective summaries
VOICE_ENERGY_THRESHOLD = 5
WINDOWS_TO_USE = 6          # 6 x 10s = last 1 minute

# OpenAI
client = OpenAI(api_key="")

# =================================================
# STREAMLIT SESSION STATE
# =================================================
if "session_summaries" not in st.session_state:
    st.session_state.session_summaries = []

if "temporal_buffer" not in st.session_state:
    st.session_state.temporal_buffer = []

if "last_window_time" not in st.session_state:
    st.session_state.last_window_time = time.time()

if "audio_started" not in st.session_state:
    st.session_state.audio_started = False

# =================================================
# AUDIO (VOICE FUSION)
# =================================================
energy_window = deque(maxlen=AUDIO_WINDOW)

def audio_callback(indata, frames, time_info, status):
    volume_norm = np.linalg.norm(indata) * 10
    energy_window.append(volume_norm)

def estimate_voice_fatigue():
    if len(energy_window) < AUDIO_WINDOW:
        return False
    return (sum(energy_window) / len(energy_window)) < VOICE_ENERGY_THRESHOLD

if not st.session_state.audio_started:
    sd.InputStream(
        callback=audio_callback,
        channels=1,
        samplerate=16000
    ).start()
    st.session_state.audio_started = True

# =================================================
# LLM FUNCTION
# =================================================
def ask_study_companion(user_input, summaries):
    lines = []
    for i, s in enumerate(summaries, 1):
        lines.append(
            f"Window {i}: "
            f"valence={s['avg_valence']}, "
            f"arousal={s['avg_arousal']}, "
            f"voice_ratio={s['voice_ratio']}, "
            f"state={s['state']}, "
            f"conclusion={s['conclusion']}"
        )

    context = "\n".join(lines)

    prompt = f"""
You are an emotion-aware study companion.

The following are affective summaries collected every 10 seconds:
{context}

User says:
"{user_input}"

Respond in a calm, supportive and human way.
Do not mention sensors, models or data collection.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    return response.choices[0].message.content

# =================================================
# STREAMLIT UI
# =================================================
st.set_page_config(layout="wide")
st.title("🎓 Emotion-Aware Study Companion")

left, right = st.columns([2, 1])

run_camera = right.checkbox("Start camera")

user_input = right.text_input(
    "Talk to your study companion",
    placeholder="e.g. I feel tired, should I take a break?"
)

ask_button = right.button("Ask Companion")

frame_box = left.empty()
status_box = right.empty()

# =================================================
# CAMERA + AFFECTIVE LOOP
# =================================================
if run_camera:
    cap = cv2.VideoCapture(0)
    detector = FER(mtcnn=True)
    emotion_window = deque(maxlen=WINDOW_SIZE)

    while run_camera:
        ret, frame = cap.read()
        if not ret:
            break

        emotions = detector.detect_emotions(frame)

        if emotions:
            emotions_dict = emotions[0]["emotions"]
            emotion_window.append(emotions_dict)

            avg = {e: np.mean([f[e] for f in emotion_window]) for e in emotions_dict}

            valence = avg["happy"] - avg["sad"] - avg["angry"]
            arousal = avg["angry"] + avg["happy"] - avg["neutral"]
            voice_fatigue = estimate_voice_fatigue()

            st.session_state.temporal_buffer.append({
                "valence": valence,
                "arousal": arousal,
                "voice_fatigue": voice_fatigue,
                "state": "Fatigue" if voice_fatigue else "Engaged"
            })

        # ---------- 10s TEMPORAL SUMMARY ----------
        now = time.time()
        if now - st.session_state.last_window_time >= TIME_WINDOW:
            buf = st.session_state.temporal_buffer
            if buf:
                avg_val = np.mean([b["valence"] for b in buf])
                avg_aro = np.mean([b["arousal"] for b in buf])
                voice_ratio = np.mean([b["voice_fatigue"] for b in buf])
                state = Counter([b["state"] for b in buf]).most_common(1)[0][0]

                if avg_val < -0.3 and voice_ratio > 0.6:
                    conclusion = "Sustained fatigue – break recommended"
                elif avg_val < -0.3:
                    conclusion = "Negative mood – slow down"
                else:
                    conclusion = "Stable / engaged"

                summary = {
                    "timestamp": now,
                    "avg_valence": round(avg_val, 2),
                    "avg_arousal": round(avg_aro, 2),
                    "voice_ratio": round(voice_ratio, 2),
                    "state": state,
                    "conclusion": conclusion
                }

                st.session_state.session_summaries.append(summary)

                status_box.markdown(f"""
                **Last 10s summary**
                - Valence: `{summary['avg_valence']}`
                - Arousal: `{summary['avg_arousal']}`
                - Voice fatigue ratio: `{summary['voice_ratio']}`
                - State: **{summary['state']}**
                - Conclusion: _{summary['conclusion']}_
                """)

            st.session_state.temporal_buffer.clear()
            st.session_state.last_window_time = now

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_box.image(frame)
        time.sleep(0.1)

    cap.release()

# =================================================
# LLM BUTTON ACTION
# =================================================
if ask_button:
    if len(st.session_state.session_summaries) < WINDOWS_TO_USE:
        st.warning("Not enough affective data yet. Keep studying a bit longer.")
    elif not user_input.strip():
        st.warning("Please enter a message.")
    else:
        with st.spinner("Thinking..."):
            reply = ask_study_companion(
                user_input,
                st.session_state.session_summaries[-WINDOWS_TO_USE:]
            )
        st.success(reply)

# =================================================
# DEBUG / TRANSPARENCY (OPTIONAL)
# =================================================
if st.session_state.session_summaries:
    st.markdown("### 🧠 Latest affective summary (debug)")
    st.json(st.session_state.session_summaries[-1])
