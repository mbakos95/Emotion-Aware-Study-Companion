# Emotion-Aware Study Companion 🎥🎙️🧠  
**Real-time multimodal affective computing + human-in-the-loop interaction + LLM-based adaptive study coaching.**

This project is a **portfolio-grade** demonstration of *how to build an emotionally aware system properly*:  
the model does **not** “guess emotions from text” and call it a day. Instead, it **continuously senses** affective cues locally (face + voice), **fuses** them into interpretable features (valence/arousal/fatigue), and uses an LLM **only** at interaction time to generate **context-adaptive, study-focused recommendations**.

> ✅ **Privacy-first**: the LLM receives **only text** (transcript + affective summary). **No raw video/audio** is sent.

---

## 🚀 One-minute pitch 
Most “emotion-aware” demos are gimmicks: they ask an LLM “how do I look?” and pretend it’s affective computing.  
This project does the real thing: a **multimodal pipeline** that extracts **implicit affect signals** locally, combines them with **explicit user intent**, and produces **adaptive guidance** with transparent, auditable inputs. It’s a clean bridge between **affective computing theory** and a practical, interactive system.

---

## ✨ What makes this project stand out
- **Affective computing (done right)**  
  Emotion is inferred from measurable cues and mapped to **interpretable features** (valence/arousal) rather than vague “vibes”.
- **Human-in-the-loop by design**  
  The user controls the interaction (**press-to-talk**) and provides intent; the system supports, it doesn’t “decide” alone.
- **Multimodal fusion**  
  Facial affect + vocal fatigue/activity are fused into a rolling affective state snapshot.
- **LLM used for reasoning, not detection**  
  The LLM is given structured affective features + transcript to generate actionable study advice.
- **Auditability & transparency**  
  The system can print/log exactly what it sent to the LLM (summary + transcript), enabling explainable demos.

---

## 🎬 Demo preview
### 1) Continuous sensing (background)
A live webcam window displays:
- **Valence** (positive ↔ negative)
- **Arousal** (calm ↔ activated)
- **Voice fatigue ratio** (proxy from voice activity)

### 2) Explicit interaction (human-in-the-loop)
Press **ENTER** to talk:
- Speech is transcribed to text  
- Affective summary is generated  
- LLM produces a personalized study recommendation  
- Response is spoken via TTS  
- Interaction is logged for reporting

---

## 🧩 Architecture (high level)

### Continuous sensing (local, real-time)
- **Camera → Facial affect**: Webcam frames → emotion probabilities  
- **Audio → Vocal fatigue/activity**: Mic input → fatigue proxy  
- **Fusion → Affective state**: rolling window aggregation → valence/arousal/fatigue + label

### On-demand reasoning (LLM call only when user interacts)
At interaction time, the LLM receives:
1. **User transcript (text)**
2. **Affective summary (text JSON-like)**  
Then it generates **adaptive study recommendations**.

> 🔒 No webcam frames, no raw audio, no biometric media leaves the device.

---

## 📦 Repository structure

```

emotion_aware_companion/
│
├── main.py              # Orchestrates threads + interaction loop
├── camera.py            # Webcam capture + facial emotion inference
├── audio_monitor.py     # Voice activity / fatigue proxy
├── speech_input.py      # Recording + transcription
├── speech_output.py     # Text-to-speech
├── affective_state.py   # Fusion: valence/arousal + rolling summary
├── llm_agent.py         # Prompt creation + OpenAI API call
├── report_generator.py  # Logging/reporting
│
├── requirements.txt
└── README.md

````

---

## 🧾 What data is sent to the LLM?
Only text:
- **Transcript** (what the user said)
- **Affective summary** (computed locally), e.g.

```json
{
  "avg_valence": -0.12,
  "avg_arousal": 0.34,
  "voice_fatigue_ratio": 0.22,
  "state": "Neutral / engaged"
}
````

That’s the “emotion-awareness” mechanism: the LLM **reacts** to *your computed affective features*.

---

## 🛠️ Skills demonstrated 

* **Real-time systems**: concurrency (camera loop + interaction loop), low-latency feedback
* **Multimodal ML integration**: CV + audio signal proxy + state fusion
* **Feature engineering**: valence/arousal mapping + rolling aggregation + thresholding
* **Human-centric AI**: user agency, interaction design, transparent decisions
* **LLM engineering**: structured prompting, safe context packaging, reproducible outputs
* **Debuggability**: optional debug print of LLM inputs + report logging for audit trails

---

## ⚙️ Setup

### 1) Clone

```bash
git clone https://github.com/mbakos95/Emotion-Aware-Study-Companion.git
cd Emotion-Aware-Study-Companion
```

### 2) Virtual environment (recommended)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Set OpenAI API key

**Windows (PowerShell)**

```powershell
setx OPENAI_API_KEY "YOUR_KEY"
```

**macOS/Linux**

```bash
export OPENAI_API_KEY="YOUR_KEY"
```

---

## ▶️ Run

```bash
python main.py
```

Controls:

* **ENTER** → press-to-talk
* **Q** → quit camera window

---

## 🧠 Notes & limitations

* Facial affect estimation is probabilistic and sensitive to lighting and face visibility.
* Voice fatigue is a **proxy** (voice activity/energy) and **not** a medical signal.
* This is a research/demo system for study support, **not** a diagnostic tool.

---

## 🗺️ Future roadmap

* Per-user calibration (adaptive baselines for voice/fatigue thresholds)
* Reliability gating (“no face detected”, “low audio quality”, confidence-based fusion)
* Lightweight UI (Streamlit) + session dashboard
* Offline/local LLM option for privacy-preserving deployments
* More robust fusion (modality weights, uncertainty estimates)

---

## 👨‍💻 Author

**Christos Zampakos**
Master’s in Artificial Intelligence & Deep Learning 
GitHub: [mbakos95](https://github.com/mbakos95)


