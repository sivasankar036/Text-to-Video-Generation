"""
AI-Based Text-to-Video Generation System v2.0
==============================================
Author  : Sivasankar Bharidu
Project : Final Year B.Tech Project
Stack   : Python | Groq (LLaMA 3) | Pexels API | gTTS | MoviePy

KEY IMPROVEMENT IN v2:
  Each image now matches its sentence.
  AI extracts a keyword from EACH sentence → fetches matching image.
  This makes visuals perfectly synced with narration.

INSTALL:
  pip install groq gtts moviepy requests pillow
"""

import os
import time
import requests
from pathlib import Path

from groq import Groq
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# ─── CONFIGURATION ───────────────────────────────────────────────────────────
GROQ_API_KEY   = os.getenv("GROQ_API_KEY",  "YOUR_GROQ_KEY_HERE")
PEXELS_API_KEY = os.getenv("PEXELS_KEY",    "YOUR_PEXELS_KEY_HERE")
OUTPUT_VIDEO   = "output_video.mp4"
TEMP_AUDIO     = "temp_audio.mp3"
IMG_FOLDER     = "temp_images"


# ─── CLASS: ScriptGenerator ──────────────────────────────────────────────────
class ScriptGenerator:
    """
    Generates a video narration script using Groq LLaMA-3.
    Also splits the script into clean sentences for image syncing.

    Interview explanation:
    "I ask the AI to write the script as numbered sentences.
    This makes splitting easy and each sentence maps to one image."
    """

    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model  = "llama-3.3-70b-versatile"

    def generate(self, topic: str) -> list:
        """
        Generates script and returns it as a list of sentences.

        Returns:
            sentences (list): each item is one narration sentence
        """
        prompt = (
            f"Write a 8-sentence narration script about: '{topic}'. "
            f"Format: write EXACTLY 8 sentences numbered 1 to 8. "
            f"Each sentence should be about a different visual aspect. "
            f"Plain text only. No hashtags or emojis."
        )

        print(f"  → Calling Groq LLaMA-3...")
        response = self.client.chat.completions.create(
            model       = self.model,
            messages    = [{"role": "user", "content": prompt}],
            temperature = 0.7,
            max_tokens  = 400
        )

        raw = response.choices[0].message.content.strip()

        # Parse numbered sentences: "1. text" → ["text", ...]
        sentences = []
        for line in raw.split("\n"):
            line = line.strip()
            if not line:
                continue
            # Remove numbering like "1." "1)" "1:"
            if line and line[0].isdigit():
                # Remove "1. " or "1) " prefix
                parts = line.split(" ", 1)
                if len(parts) == 2:
                    sentences.append(parts[1].strip())
                else:
                    sentences.append(line)
            else:
                sentences.append(line)

        # Fallback: split by period if parsing failed
        if len(sentences) < 3:
            sentences = [s.strip() for s in raw.split(".") if len(s.strip()) > 10]

        print(f"  ✓ Script ready — {len(sentences)} sentences")
        return sentences


# ─── CLASS: KeywordExtractor ─────────────────────────────────────────────────
class KeywordExtractor:
    """
    Extracts a 2-3 word visual search keyword from each sentence.

    Interview explanation:
    "This is the core improvement. Instead of one keyword for all
    images, I ask the AI to read each sentence and return the best
    2-3 words that describe what image should appear on screen."

    Example:
      Sentence : "Pilgrims climb the steep steps of Tirumala hill"
      Keyword  : "pilgrims climbing steps"
    """

    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model  = "llama-3.3-70b-versatile"

    def extract(self, sentence: str) -> str:
        prompt = (
            f"Return ONLY 2-3 words that best describe the visual "
            f"scene for this sentence. No explanation, just words.\n"
            f"Sentence: {sentence}"
        )
        try:
            resp = self.client.chat.completions.create(
                model       = self.model,
                messages    = [{"role": "user", "content": prompt}],
                temperature = 0.2,
                max_tokens  = 15
            )
            kw = resp.choices[0].message.content.strip()
            kw = kw.replace('"', '').replace("'", "").strip()
            return kw if kw else " ".join(sentence.split()[:3])
        except Exception:
            return " ".join(sentence.split()[:3])


# ─── CLASS: ImageFetcher ─────────────────────────────────────────────────────
class ImageFetcher:
    """
    Downloads ONE perfectly matched image per sentence from Pexels.

    Interview explanation:
    "For each sentence I get a keyword from the AI, then search
    Pexels with that keyword. So if the script says 'pilgrims
    climbing Tirumala', Pexels returns a photo of pilgrims on
    hills — not a generic temple photo."
    """

    PEXELS_URL = "https://api.pexels.com/v1/search"

    def __init__(self, api_key: str, groq_key: str):
        self.headers   = {"Authorization": api_key}
        self.extractor = KeywordExtractor(groq_key)
        Path(IMG_FOLDER).mkdir(exist_ok=True)

    def _download_one(self, keyword: str, index: int) -> str:
        """Downloads best Pexels image for keyword. Returns filepath."""
        for query in [keyword, keyword.split()[0]]:
            try:
                r = requests.get(
                    self.PEXELS_URL,
                    headers=self.headers,
                    params={"query": query, "per_page": 3, "orientation": "landscape"},
                    timeout=10
                )
                photos = r.json().get("photos", [])
                if photos:
                    url  = photos[0]["src"]["large"]
                    path = f"{IMG_FOLDER}/img_{index}.jpg"
                    with open(path, "wb") as f:
                        f.write(requests.get(url, timeout=10).content)
                    return path
            except Exception:
                continue
        return None

    def fetch_per_sentence(self, sentences: list) -> list:
        """
        Fetches one matched image per sentence.

        Returns:
            list of (sentence, image_path) pairs
        """
        print(f"  → Matching images to {len(sentences)} sentences...")
        pairs = []

        for i, sentence in enumerate(sentences):
            # Extract visual keyword using AI
            keyword = self.extractor.extract(sentence)
            print(f"  [{i+1}/{len(sentences)}] \"{sentence[:45]}...\"")
            print(f"            🔍 Searching: \"{keyword}\"")

            # Download matching image
            path = self._download_one(keyword, i)

            if path:
                pairs.append((sentence, path))
                print(f"            ✓ Image saved")
            else:
                print(f"            ✗ Skipped — no result")

            time.sleep(0.4)  # avoid rate limit

        if not pairs:
            raise ValueError("No images fetched. Check Pexels API key.")

        return pairs


# ─── CLASS: AudioGenerator ───────────────────────────────────────────────────
class AudioGenerator:
    """
    Converts full script text to MP3 using Google TTS (free).

    Interview explanation:
    "gTTS is Google Text-to-Speech. I join all sentences into
    one paragraph and convert to audio. This gives natural
    speech flow compared to generating audio per sentence."
    """

    def generate(self, sentences: list, filename: str = TEMP_AUDIO) -> str:
        full_text = " ".join(sentences)
        print(f"  → Converting {len(sentences)} sentences to speech...")
        tts = gTTS(text=full_text, lang="en", slow=False)
        tts.save(filename)
        print(f"  ✓ Audio saved: {filename}")
        return filename


# ─── CLASS: VideoAssembler ───────────────────────────────────────────────────
class VideoAssembler:
    """
    Assembles sentence-image pairs + audio into final MP4.

    Interview explanation:
    "I divide total audio duration equally across all images.
    Since each image matches its sentence, the visual and audio
    are now semantically synced — not just time synced."
    """

    def assemble(self, pairs: list, audio_path: str,
                 output: str = OUTPUT_VIDEO) -> str:
        """
        Args:
            pairs      : list of (sentence, image_path)
            audio_path : path to narration audio
            output     : output video filename
        """
        print(f"  → Assembling {len(pairs)} image-sentence pairs...")

        audio    = AudioFileClip(audio_path)
        duration = audio.duration
        per_clip = duration / len(pairs)

        print(f"  → Total duration: {duration:.1f}s | Per image: {per_clip:.1f}s")

        clips = []
        for sentence, img_path in pairs:
            clip = (
                ImageClip(img_path)
                .set_duration(per_clip)
                .set_fps(24)
            )
            clips.append(clip)

        video = concatenate_videoclips(clips, method="compose")
        final = video.set_audio(audio)

        print(f"  → Rendering video...")
        final.write_videofile(
            output,
            codec       = "libx264",
            audio_codec = "aac",
            fps         = 24,
            verbose     = False,
            logger      = None
        )
        print(f"  ✓ Video saved: {output}")
        return output


# ─── CLASS: TextToVideoApp ───────────────────────────────────────────────────
class TextToVideoApp:
    """
    Main application — orchestrates the full pipeline.

    Pipeline v2.0:
      topic
        → ScriptGenerator  (LLaMA-3 generates 8 sentences)
        → AudioGenerator   (gTTS converts sentences to MP3)
        → ImageFetcher     (AI keyword per sentence → Pexels image)
        → VideoAssembler   (images + audio → MP4)

    Interview explanation:
    "I used the Facade design pattern. TextToVideoApp is the
    facade — it provides one simple method run() that hides
    the complexity of 4 different modules working together."
    """

    def __init__(self):
        self.script_gen  = ScriptGenerator(GROQ_API_KEY)
        self.audio_gen   = AudioGenerator()
        self.img_fetch   = ImageFetcher(PEXELS_API_KEY, GROQ_API_KEY)
        self.video_asm   = VideoAssembler()

    def run(self, topic: str) -> str:
        print("\n" + "="*55)
        print("  TEXT-TO-VIDEO PIPELINE v2.0")
        print(f"  Topic: {topic}")
        print("="*55)

        # STEP 1: Generate 8-sentence script
        print("\n[1/4] Generating Script...")
        sentences = self.script_gen.generate(topic)
        print("\n  Script Preview:")
        for i, s in enumerate(sentences, 1):
            print(f"  {i}. {s}")

        # STEP 2: Generate audio from full script
        print("\n[2/4] Generating Audio...")
        audio_path = self.audio_gen.generate(sentences)

        # STEP 3: Fetch one matched image per sentence
        print("\n[3/4] Fetching Sentence-Matched Images...")
        pairs = self.img_fetch.fetch_per_sentence(sentences)

        # STEP 4: Assemble video
        print("\n[4/4] Assembling Video...")
        output = self.video_asm.assemble(pairs, audio_path)

        print("\n" + "="*55)
        print("  PIPELINE COMPLETE!")
        print(f"  Video: {output}")
        print(f"  Sentences: {len(sentences)} | Images: {len(pairs)}")
        print("="*55 + "\n")
        return output


# ─── MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    TOPIC = "Story of Tirumala Venkateswara Temple"
    app   = TextToVideoApp()
    video = app.run(TOPIC)
    print(f"Done! Open '{video}' to watch your video.")
