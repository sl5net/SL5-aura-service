# Source: transcribe_audiofile.py
import vosk
import sys
import json
import pyperclip
import subprocess
import time
from pathlib import Path
import argparse
import os
import re
import wave
import tempfile
import shutil
from slugify import slugify
import datetime

# --- Prerequisite Check ---
try:
    from slugify import slugify
except ImportError:
    print("ERROR: python-slugify is not installed. Please run: pip install python-slugify", file=sys.stderr)
    sys.exit(1)


# --- Configuration ---
SCRIPT_DIR = Path(__file__).resolve().parent
LOG_FILE = Path("/tmp/vosk_transcription.log")
NOTIFY_SEND_PATH = "/usr/bin/notify-send"
# The format Vosk requires
EXPECTED_SAMPLE_RATE = 16000
EXPECTED_CHANNELS = 1

# --- Argument Processing with Defaults ---
MODEL_NAME_DEFAULT = "vosk-model-de-0.21"
parser = argparse.ArgumentParser(description="Transcribe an audio file (MP3, WAV, etc.) using Vosk.")
parser.add_argument('audiofile', help="Path to the audio file to transcribe.")
parser.add_argument('--vosk_model', help=f"Name of the Vosk model folder. Defaults to '{MODEL_NAME_DEFAULT}'.")
args = parser.parse_args()

# --- Model Name Resolution ---
VOSK_MODEL_FILE_PATH = "/tmp/vosk_model"
vosk_model_from_file = ''
if os.path.exists(VOSK_MODEL_FILE_PATH):
    with open(VOSK_MODEL_FILE_PATH, 'r') as f:
        vosk_model_from_file = f.read().strip()

MODEL_NAME = args.vosk_model or vosk_model_from_file or MODEL_NAME_DEFAULT
MODEL_PATH = SCRIPT_DIR / MODEL_NAME

MY_STOPWORDS = ['der', 'die', 'das', 'ist', 'ein', 'eine', 'einer', 'mit', 'und', 'a', 'is', 'with', 'the', 'of', 'in']

def create_slug_from_text(text: str, min_word_len: int = 4) -> str:
    """
    Creates a clean, descriptive slug from text.
    Requires python-slugify version 5.0.0 or newer for 'stopwords' support.
    """
    # 1. Use slugify to remove stopwords and create a basic slug.
    # The word_boundary=True is good practice to avoid partial word matching.
    try:
        initial_slug = slugify(text, stopwords=MY_STOPWORDS, max_length=80, word_boundary=True)
    except TypeError:
        # This is a fallback for older versions, though upgrading is recommended.
        print("Warning: Your 'python-slugify' is outdated. 'stopwords' are not being removed.", file=sys.stderr)
        initial_slug = slugify(text, max_length=80, word_boundary=True)

    # 2. Filter out any remaining short words.
    words = initial_slug.split('-')
    long_words = [w for w in words if len(w) >= min_word_len and w]

    # 3. Join them back and ensure the result is not empty.
    final_slug = '-'.join(long_words)
    return final_slug if final_slug else "transcription"


# --- Punctuation Normalization ---
PUNCTUATION_MAP = {
    # German
    'punkt': '.', 'komma': ',', 'fragezeichen': '?', 'ausrufezeichen': '!',
    'doppelpunkt': ':', 'semikolon': ';', 'strichpunkt': ';',
    # English
    'period': '.', 'full stop': '.', 'dot': '.', 'comma': ',',
    'question mark': '?', 'exclamation mark': '!', 'exclamation point': '!',
    'colon': ':', 'semicolon': ';',
}

def normalize_punctuation(text: str) -> str:
    """Replaces spoken punctuation with its symbol."""
    pattern = r'\b(' + '|'.join(re.escape(key) for key in sorted(PUNCTUATION_MAP.keys(), key=len, reverse=True)) + r')\b'
    def replace(match):
        return PUNCTUATION_MAP[match.group(1).lower()]
    return re.sub(pattern, replace, text, flags=re.IGNORECASE)


# --- Helper Functions ---
def notify(summary, body="", urgency="low", icon=None):
    """Sends a desktop notification."""
    full_cmd = [NOTIFY_SEND_PATH, "-r", "9998", "-u", urgency, summary, body, "-t", "4000"]
    if icon:
        full_cmd.extend(["-i", icon])
    try:
        subprocess.run(full_cmd, check=True, capture_output=True, text=True)
    except Exception:
        pass # Fail silently if notifications don't work

def check_ffmpeg():
    """Checks if ffmpeg is installed and in the system's PATH."""
    if not shutil.which("ffmpeg"):
        msg = ("FATAL ERROR: `ffmpeg` is not installed or not in your PATH.\n"
               "It is required for audio conversion.\n"
               "On Manjaro/Arch, install it with: sudo pacman -Syu ffmpeg")
        print(msg, file=sys.stderr)
        notify("Vosk Prerequisite Missing", "ffmpeg is not installed.", "critical", "dialog-error")
        sys.exit(1)


# --- Main Logic ---
def main():
    """Main function to run the transcription process."""
    check_ffmpeg()

    original_audio_path = Path(args.audiofile)
    if not original_audio_path.is_file():
        msg = f"ERROR: Input file not found at '{original_audio_path}'"
        print(msg, file=sys.stderr); notify("Vosk Error", msg, "critical", "dialog-error"); sys.exit(1)

    if not MODEL_PATH.exists():
        msg = f"FATAL ERROR: Model not found at '{MODEL_PATH}'"
        print(msg, file=sys.stderr); notify("Vosk Model Error", msg, "critical", "dialog-error"); sys.exit(1)

    print(f"Loading model '{MODEL_NAME}'..."); model = vosk.Model(str(MODEL_PATH)); print("Model loaded.")

    temp_wav_path = None
    try:
        print(f"Converting '{original_audio_path.name}' to temporary WAV...");
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_f: temp_wav_path = tmp_f.name
        ffmpeg_cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(original_audio_path),
                      "-ar", str(EXPECTED_SAMPLE_RATE), "-ac", str(EXPECTED_CHANNELS), "-y", temp_wav_path]
        subprocess.run(ffmpeg_cmd, check=True)
        print("Conversion successful.")

        with wave.open(temp_wav_path, "rb") as wf:
            print("Transcribing audio...");
            recognizer = vosk.KaldiRecognizer(model, wf.getframerate()); recognizer.SetWords(True)
            while True:
                data = wf.readframes(4000)
                if len(data) == 0: break
                recognizer.AcceptWaveform(data)

            result = json.loads(recognizer.FinalResult())
            raw_text = result.get('text', '')

            if raw_text:
                final_text = normalize_punctuation(raw_text)
                pyperclip.copy(final_text)
                print("\n--- Transcription ---")
                print(final_text)

                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
                slug = create_slug_from_text(final_text, min_word_len=4)
                output_filename_txt = SCRIPT_DIR / f"{timestamp}_{slug}.txt"

                with open(output_filename_txt, "w") as text_file:
                    text_file.write(final_text)
                print(f"\nSaved to: {output_filename_txt}")

                print("---------------------")
                notify("Transcription Complete", f"Saved to {output_filename_txt.name}", "normal", "edit-paste")
            else:
                print("No text recognized in the audio file.")
                notify("Transcription Complete", "No text was recognized.", "normal", "dialog-warning")

    except subprocess.CalledProcessError:
        msg = f"ffmpeg failed to convert '{original_audio_path.name}'. It may be corrupted or unsupported."
        print(msg, file=sys.stderr); notify("Vosk Conversion Error", msg, "critical", "dialog-error"); sys.exit(1)
    except Exception as e:
        msg = f"An error occurred during transcription: {e}"
        print(msg, file=sys.stderr); notify("Vosk Runtime Error", msg, "critical", "dialog-error"); sys.exit(1)
    finally:
        if temp_wav_path and os.path.exists(temp_wav_path):
            os.remove(temp_wav_path); print(f"Cleaned up temporary file.")

if __name__ == "__main__":
    main()
