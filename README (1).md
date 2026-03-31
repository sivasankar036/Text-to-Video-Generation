# 🎬 AI-Based Text-to-Video Generation System

> **Final Year B.Tech Project** | Team Size: 4 | Role: **Team Leader**  
> B.Tech Computer Science (AI/ML) — Sivasankar Bharidu — 2025

An automated Python pipeline that converts any text topic into a complete narrated video — using Groq LLaMA-3 AI, Pexels images, Google TTS, and MoviePy. No manual editing required.

---

## 🔥 How It Works

```
Topic Input  →  "Story of Tirumala Venkateswara Temple"
      ↓
[Stage 1]  Groq LLaMA-3 AI  →  Generates 8-sentence narration script
      ↓
[Stage 2]  Google TTS (gTTS)  →  Converts full script to MP3 audio
      ↓
[Stage 3]  KeywordExtractor (AI)  →  Extracts visual keyword per sentence
      ↓
[Stage 4]  Pexels API  →  Downloads 1 matched image per sentence
      ↓
[Stage 5]  MoviePy  →  Assembles all images + audio into MP4 video
      ↓
Output  →  output_video.mp4
```

---

## ✨ Key Features

- **Sentence-level image sync** — each image matches exactly what is being narrated
- **Free APIs only** — Groq, Pexels, gTTS — zero cost, no credit card
- **OOP architecture** — 5 classes, Single Responsibility Principle
- **Facade design pattern** — simple one-line interface hiding 4 subsystems
- Works for **any topic** — history, science, travel, culture, education

---

## 🛠 Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| AI Script Generation | Groq LLaMA-3.3-70B | Generate narration script |
| Text to Speech | Google TTS (gTTS) | Convert script to audio |
| Visual Keyword AI | Groq LLaMA-3.3-70B | Extract keyword per sentence |
| Image Search | Pexels API | Fetch matched images |
| Video Assembly | MoviePy | Combine images + audio |
| Language | Python 3.10+ | Core implementation |

---

## 🏗 Project Architecture

```
TextToVideoApp  (Facade Design Pattern)
│
├── ScriptGenerator     — Calls Groq LLaMA-3 to generate 8-sentence script
│
├── AudioGenerator      — Uses gTTS to convert script to MP3 audio
│
├── KeywordExtractor    — Calls AI to get visual keyword per sentence
│
├── ImageFetcher        — Searches Pexels for 1 matching image per sentence
│
└── VideoAssembler      — Uses MoviePy to assemble images + audio into MP4
```

---

## 📦 Installation

```bash
# Step 1: Clone the repository
git clone https://github.com/sivasankar036/text-to-video-ai.git
cd text-to-video-ai

# Step 2: Install all dependencies
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Get your **FREE** API keys:
- **Groq API Key** → [console.groq.com](https://console.groq.com) (free, no credit card)
- **Pexels API Key** → [pexels.com/api](https://www.pexels.com/api/) (free, instant approval)

Open `text_to_video.py` and replace lines 39-40:
```python
GROQ_API_KEY   = "YOUR_GROQ_KEY_HERE"     # paste your Groq key here
PEXELS_API_KEY = "YOUR_PEXELS_KEY_HERE"   # paste your Pexels key here
```

---

## ▶️ Run the Project

```bash
python text_to_video.py
```

Change the topic at the bottom of the file:
```python
TOPIC = "Story of Tirumala Venkateswara Temple"
# Change to any topic you want!
```

---

## 📋 Sample Output

```
=======================================================
  TEXT-TO-VIDEO PIPELINE v2.0
  Topic: Story of Tirumala Venkateswara Temple
=======================================================

[1/4] Generating Script...
  → Calling Groq LLaMA-3...
  ✓ Script ready — 8 sentences

[2/4] Generating Audio...
  → Converting 8 sentences to speech...
  ✓ Audio saved: temp_audio.mp3

[3/4] Fetching Sentence-Matched Images...
  [1/8] "Lord Venkateswara stands atop the seven sacred hills..."
            🔍 Searching: "Venkateswara temple hills"
            ✓ Image saved
  [2/8] "Millions of pilgrims climb the steps every year..."
            🔍 Searching: "pilgrims climbing steps"
            ✓ Image saved
  ...

[4/4] Assembling Video...
  → Total duration: 45.2s | Per image: 5.6s
  → Rendering video...
  ✓ Video saved: output_video.mp4

=======================================================
  PIPELINE COMPLETE!
  Video: output_video.mp4
=======================================================
```

---

## 🧠 OOP Concepts Used

| Concept | Implementation |
|---|---|
| **Class** | ScriptGenerator, ImageFetcher, AudioGenerator, VideoAssembler, TextToVideoApp |
| **Encapsulation** | Each class hides its internal API calls |
| **Abstraction** | app.run(topic) hides complexity of 4 subsystems |
| **Single Responsibility** | Each class does exactly one job |
| **Facade Pattern** | TextToVideoApp provides simple interface |

---

## 👨‍💻 Author

**Sivasankar Bharidu**  
B.Tech Computer Science Engineering (AI/ML Specialization) — 2025  
Annamacharya Institute of Technology & Sciences, Tirupati  
CGPA: 8.88 / 10

- GitHub: [github.com/sivasankar036](https://github.com/sivasankar036)
- Email: sivasankar102030@gmail.com
- LinkedIn: [linkedin.com/in/siva-sankar36](https://linkedin.com/in/siva-sankar36)

---

## 📄 Research Publication

This project is supported by a published research paper:  
**"AI-Driven Animation System: Revolutionizing the Animation Creation Process Through Artificial Intelligence"**  
JETIR — UGC Approved | ISSN: 2349-5162 | Impact Factor: 7.95  
[jetir.org/view?paper=JETIR2504260](https://jetir.org/view?paper=JETIR2504260)
