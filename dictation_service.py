# Datei: ~/projects/py/STT/dictation_service.py
import vosk
import sys
import sounddevice as sd
import queue
import json
import pyperclip
import subprocess
import time
from pathlib import Path
import argparse
import os
import re
import psutil # pip install psutil
import atexit


HEARTBEAT_FILE = "/tmp/dictation_service.heartbeat"
PIDFILE = "/tmp/dictation_service.pid"
def cleanup():
    """Remove the heartbeat and PID files on exit."""
    print("Cleaning up and exiting.")
    if os.path.exists(HEARTBEAT_FILE):
        os.remove(HEARTBEAT_FILE)
    if os.path.exists(PIDFILE):
        os.remove(PIDFILE)
# Register the cleanup function to run on normal exit or termination
atexit.register(cleanup)
# Write the PID file once at the start
with open(PIDFILE, 'w') as f:
    f.write(str(os.getpid()))

# --- Configuration ---
# Set the critical threshold for available memory in Megabytes (MB).
CRITICAL_THRESHOLD_MB = 1024  # 1 GB
SCRIPT_DIR = Path(__file__).resolve().parent
TRIGGER_FILE = Path("/tmp/vosk_trigger")
LOG_FILE = Path("/tmp/vosk_dictation.log")
NOTIFY_SEND_PATH = "/usr/bin/notify-send"
XDOTOOL_PATH = "/usr/bin/xdotool"
SAMPLE_RATE = 16000

# --- Argument processing with default value ---
MODEL_NAME_DEFAULT = "vosk-model-de-0.21"
parser = argparse.ArgumentParser(description="A real-time dictation service using Vosk.")
parser.add_argument('--vosk_model', help=f"Name of the Vosk model folder. Defaults to '{MODEL_NAME_DEFAULT}'.")
args = parser.parse_args()

# --- Model Name Resolution ---
VOSK_MODEL_FILEread = ''
VOSK_MODEL_FILE = "/tmp/vosk_model"
if os.path.exists(VOSK_MODEL_FILE):
    with open(VOSK_MODEL_FILE, 'r') as f:
        VOSK_MODEL_FILEread = f.read()
MODEL_NAME = args.vosk_model or VOSK_MODEL_FILEread or MODEL_NAME_DEFAULT
MODEL_PATH = SCRIPT_DIR / MODEL_NAME

# MODEL_NAME = args.vosk_model if args.vosk_model else MODEL_NAME_DEFAULT


def check_memory_critical(threshold_mb: int) -> tuple[bool, float]:
    """
    Checks if the available system memory is below a given threshold.

    This function uses 'psutil' to get cross-platform memory information.
    It checks 'available' memory, which is a more realistic measure than 'free' memory.

    Args:
        threshold_mb: The critical memory threshold in Megabytes.

    Returns:
        A tuple containing:
        - bool: True if memory is critical, False otherwise.
        - float: The currently available memory in Megabytes.

    its fast. maybe take 5 milliseconds
    """
    # Get memory statistics
    mem = psutil.virtual_memory()

    # Convert available memory from Bytes to Megabytes
    available_mb = mem.available / (1024 * 1024)

    # Check if available memory is below the threshold
    is_critical = available_mb < threshold_mb

    return is_critical, available_mb


PUNCTUATION_MAP = {
    # German
    'punkt': '.',
    'komma': ',',
    'fragezeichen': '?',
    'ausrufezeichen': '!',
    'doppelpunkt': ':',
    'semikolon': ';',
    'strichpunkt': ';', # Synonym for Semicolon

    # English
    'period': '.',
    'full stop': '.',
    'dot': '.',
    'comma': ',',

    'question mark': '?',
    'christian monk': '?', # ists not exacpt but help somtimes

    'exclamation mark': '!',
    'exclamation point': '!',
    'colon': ':',
    'semicolon': ';',
}

# ? huge please stop.!

def normalize_punctuation(text: str) -> str:
    """
    Replaces spoken punctuation (e.g., "question mark") with its symbol (e.g., "?").
    This function is case-insensitive and handles multiple languages via the map.
    It correctly handles word boundaries to avoid partial replacements.
    """
    # Create a single regex pattern from the dictionary keys.
    # The `|` acts as an "OR". We sort keys by length descending
    # to match longer phrases first (e.g., "question mark" before "mark").
    # \b ensures we match whole words only.
    pattern = r'\b(' + '|'.join(re.escape(key) for key in sorted(PUNCTUATION_MAP.keys(), key=len, reverse=True)) + r')\b'

    # The replacement function looks up the matched word (in lowercase) in our map.
    def replace(match):
        return PUNCTUATION_MAP[match.group(1).lower()]

    # Use re.sub with the IGNORECASE flag to perform the replacement.
    # The `(?i)` flag inline is an alternative to re.IGNORECASE
    return re.sub(pattern, replace, text, flags=re.IGNORECASE)



# --- Hilfsfunktionen ---
def notify(summary, body="", urgency="low", icon=None):
    full_cmd = [NOTIFY_SEND_PATH, "-r", "9999", "-u", urgency, summary, body, "-t", "2000"]
    if icon:
        full_cmd.extend(["-i", icon])
    try:
        subprocess.run(full_cmd, check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e1:
        basic_cmd = [NOTIFY_SEND_PATH, summary, body]
        try:
            subprocess.run(basic_cmd, check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e2:
            error_message = (
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - NOTIFICATION FAILED\n"
                f"  Summary: {summary}\n  Body: {body}\n  Full command error: {e1}\n  Basic command error: {e2}\n"
                "------------------------------------------\n"
            )
            print(error_message)
            with open(LOG_FILE, "a") as f: f.write(error_message)


def transcribe_audio_with_feedback(recognizer):
    q = queue.Queue()
    def audio_callback(indata, frames, time, status):
        if status: print(status, file=sys.stderr)
        q.put(bytes(indata))

    recognizer.SetWords(True)
    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=4000,
                               dtype='int16', channels=1, callback=audio_callback):
            notify("Vosk Hört zu...", "Jetzt sprechen.", "normal", icon="microphone-sensitivity-high-symbolic")
            # notify("Vosk is Listening...", "Speak now.", "normal", icon="microphone-sensitivity-high-symbolic")

            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    return json.loads(recognizer.Result()).get('text', '')
                #else:
                #    partial_text = json.loads(recognizer.PartialResult()).get('partial', '')
                    # if partial_text: notify("...", partial_text, icon="microphone-sensitivity-medium-symbolic")
    except Exception as e:
        # error_msg = f"Fehler bei der Transkription: {e}"
        error_msg = f"Transcription error: {e}"
        print(error_msg); notify("Vosk Error", error_msg, icon="dialog-error"); return ""

# --- Hauptlogik des Dienstes ---
print("--- Vosk Diktier-Dienst ---")

if not MODEL_PATH.exists():
    msg = f"FATALER FEHLER: Modell nicht gefunden unter {MODEL_PATH}"
    print(msg); notify("Vosk Startfehler", msg, icon="dialog-error"); sys.exit(1)

print(f"Lade Modell '{MODEL_NAME}'... Dies kann einige Sekunden dauern.")
try:
    model = vosk.Model(str(MODEL_PATH))
    # print("Modell erfolgreich geladen. Dienst wartet auf Signal.")
    # notify("Vosk Dienst Bereit", f"Hotkey für '{MODEL_NAME}' ist nun aktiv.", icon="media-record")
    print("Model loaded successfully. Service is waiting for signal.")
    notify("Vosk Service Ready", f"Hotkey for '{MODEL_NAME}' is now active.", icon="media-record")

except Exception as e:
    msg = f"FATALER FEHLER: Modell konnte nicht geladen werden. {e}"
    print(msg); notify("Vosk Startfehler", msg, icon="dialog-error"); sys.exit(1)

is_recording = False

CHECK_INTERVAL_SECONDS = 3
last_check_time = time.time()
recording_time = 0

try:
    while True:
        try:
            current_time = time.time()

            if TRIGGER_FILE.exists() and not is_recording:
                is_recording = True
                is_recording_time = time.time()

                TRIGGER_FILE.unlink()
                print("Signal erkannt! Starte Transkription.")

                try:
                    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
                    recognized_text = transcribe_audio_with_feedback(recognizer)
                    if recognized_text:
                        print(f"Transkribiert: '{recognized_text}'")

                        recognized_text = normalize_punctuation(recognized_text)
                        if re.match(r"^\w", recognized_text, re.IGNORECASE):
                            # it starts with a word

                            # use  needing space at the beginning then win us recognition  the last in the last twenty secondswas in last twenty seconds ago
                            if current_time - recording_time < 20:
                                recognized_text = ' ' + recognized_text

                            recording_time = time.time()

                        pyperclip.copy(recognized_text)
                        subprocess.run([XDOTOOL_PATH, "type", "--clearmodifiers", recognized_text])
                        # notify("Vosk Diktat", f"Text eingefügt:\n'{recognized_text}'", "normal", icon="edit-paste")
                    else:
                        notify("Vosk Diktat", "Kein Text erkannt.", icon="dialog-warning")
                finally:
                    is_recording = False
                    notify("Vosk Diktat", "Not Recoding at the Moment.", icon="dialog-warning")

            elif TRIGGER_FILE.exists() and not is_recording:
                 TRIGGER_FILE.unlink()


            if current_time - last_check_time > CHECK_INTERVAL_SECONDS:
                # Run the memory check here
                last_check_time = current_time

                # Call memory is_critical (this check takes only about 5 milliseconds)
                is_critical, current_available_mb = check_memory_critical(CRITICAL_THRESHOLD_MB)
                # notify("Vosk Diktat", f"available memory MB:\n'{current_available_mb:.2f} MB'", "normal", icon="edit-paste")

                # Print a status message based on the result
                if is_critical:
                    print(f"CRITICAL: Available memory is {current_available_mb:.2f} MB, "
                        f"which is below the threshold of {CRITICAL_THRESHOLD_MB} MB.")
                    # Exit with a non-zero status code to indicate a problem
                    sys.exit(1)

            time.sleep(0.1)

            # Update the heartbeat file with the current timestamp
            with open(HEARTBEAT_FILE, 'w') as f:
                f.write(str(int(time.time())))


        except KeyboardInterrupt:
            print("\nDienst durch Benutzer beendet.")
            notify("Vosk Diktat", "Dienst durch Benutzer beendet.", icon="dialog-warning")
            break # Verlässt den while-Loop und geht zum finally-Block
        except Exception as e:
            error_msg = f"Fehler im Haupt-Loop: {e}"
            print(error_msg)
            notify("Vosk Dienst Fehler", error_msg, icon="dialog-error")
            is_recording = False
finally:
    print("Dienst wird heruntergefahren. Sende Abschluss-Benachrichtigung.")
    notify("Vosk Dienst", "Dienst wurde beendet.", "normal", icon="process-stop-symbolic")
