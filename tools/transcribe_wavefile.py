# Source: transcribe_wavefile.py
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

# --- Configuration ---
SCRIPT_DIR = Path(__file__).resolve().parent
LOG_FILE = Path("/tmp/vosk_transcription.log")
NOTIFY_SEND_PATH = "/usr/bin/notify-send"
# The sample rate your Vosk model expects. Most models use 16000.
EXPECTED_SAMPLE_RATE = 16000
EXPECTED_CHANNELS = 1

# --- Argument Processing with Defaults ---
MODEL_NAME_DEFAULT = "../models/vosk-model-de-0.21"
parser = argparse.ArgumentParser(description="Transcribe a .WAV audio file using Vosk. Automatically converts format if needed.")
parser.add_argument('wavefile', help="Path to the .WAV file to transcribe.")
parser.add_argument('--vosk_model', help=f"Name of the Vosk model folder. Defaults to '{MODEL_NAME_DEFAULT}'.")
args = parser.parse_args()

# --- Model Name Resolution ---
VOSK_MODEL_FILE_PATH =  SCRIPT_DIR / "config/model_name.txt"

vosk_model_from_file = ''
if os.path.exists(VOSK_MODEL_FILE_PATH):
    with open(VOSK_MODEL_FILE_PATH, 'r') as f:
        vosk_model_from_file = f.read().strip()

MODEL_NAME = args.vosk_model or vosk_model_from_file or MODEL_NAME_DEFAULT
MODEL_PATH = SCRIPT_DIR / "../models" / MODEL_NAME


# --- Punctuation Normalization (reused from your script) ---
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
    except (subprocess.CalledProcessError, FileNotFoundError) as e1:
        basic_cmd = [NOTIFY_SEND_PATH, summary, body]
        try:
            subprocess.run(basic_cmd, check=True, capture_output=True, text=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e2:
            error_message = (
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - NOTIFICATION FAILED\n"
                f"  Summary: {summary}\n  Body: {body}\n  Full command error: {e1}\n  Basic command error: {e2}\n"
                "------------------------------------------\n"
            )
            print(error_message, file=sys.stderr)
            with open(LOG_FILE, "a") as f: f.write(error_message)

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

    # --- Input File Validation ---
    original_wave_path = Path(args.wavefile)
    if not original_wave_path.is_file():
        msg = f"ERROR: Input file not found at '{original_wave_path}'"
        print(msg, file=sys.stderr)
        notify("Vosk Transcription Error", msg, "critical", "dialog-error")
        sys.exit(1)

    # --- Model Validation ---
    if not MODEL_PATH.exists():
        msg = f"FATAL ERROR: Model not found at '{MODEL_PATH}'"
        print(msg, file=sys.stderr)
        notify("Vosk Model Error", msg, "critical", "dialog-error")
        sys.exit(1)

    # --- Load Model ---
    print(f"Loading model '{MODEL_NAME}'... This may take a moment.")
    try:
        model = vosk.Model(str(MODEL_PATH))
        print("✅ Model loaded successfully.")
    except Exception as e:
        msg = f"FATAL ERROR: Could not load model '{MODEL_NAME}'.\n{e}"
        print(msg, file=sys.stderr)
        notify("Vosk Model Error", msg, "critical", "dialog-error")
        sys.exit(1)

    temp_file_path = None
    path_to_process = original_wave_path
    try:
        # --- Check Audio Format and Convert if Necessary ---
        with wave.open(str(original_wave_path), "rb") as wf:
            rate = wf.getframerate()
            channels = wf.getnchannels()
            if rate != EXPECTED_SAMPLE_RATE or channels != EXPECTED_CHANNELS:
                print(f"Info: Audio format mismatch ({channels}ch @ {rate}Hz). "
                      f"Required: {EXPECTED_CHANNELS}ch @ {EXPECTED_SAMPLE_RATE}Hz.")
                print("Attempting conversion with ffmpeg...")
                notify("Vosk File Conversion", "Converting audio to required format...", "low", "media-record")

                # Create a temporary file for the converted audio
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_f:
                    temp_file_path = tmp_f.name

                ffmpeg_cmd = [
                    "ffmpeg", "-hide_banner", "-loglevel", "error",
                    "-i", str(original_wave_path),
                    "-ar", str(EXPECTED_SAMPLE_RATE),
                    "-ac", str(EXPECTED_CHANNELS),
                    "-y", # Overwrite output file if it exists
                    temp_file_path
                ]
                subprocess.run(ffmpeg_cmd, check=True)
                path_to_process = Path(temp_file_path)
                print(f"Conversion successful. Using temporary file: {path_to_process}")

        # --- Transcribe File ---
        with wave.open(str(path_to_process), "rb") as wf:
            print(f"Transcribing '{path_to_process.name}'...")
            notify("Vosk Transcription", f"Processing '{original_wave_path.name}'...", "low", "media-record")

            recognizer = vosk.KaldiRecognizer(model, wf.getframerate())
            recognizer.SetWords(True)

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                recognizer.AcceptWaveform(data)

            result = json.loads(recognizer.FinalResult())
            raw_text = result.get('text', '')

            if raw_text:
                final_text = normalize_punctuation(raw_text)
                pyperclip.copy(final_text)
                print("\n--- Transcription ---")
                print(final_text)
                print("---------------------")
                notify("Transcription Complete", "Text copied to clipboard.", "normal", "edit-paste")
            else:
                print("No text recognized in the audio file.")
                notify("Transcription Complete", "No text was recognized.", "normal", "dialog-warning")

    except Exception as e:
        msg = f"An error occurred during transcription: {e}"
        print(msg, file=sys.stderr)
        notify("Vosk Runtime Error", msg, "critical", "dialog-error")
        sys.exit(1)
    finally:
        # --- Cleanup ---
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Cleaned up temporary file: {temp_file_path}")

if __name__ == "__main__":
    main()
