# File: ~/projects/py/STT/dictation_service.py
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
import psutil
import atexit
import requests
import threading
import signal
from inotify_simple import INotify, flags

# --- Configuration ---
CRITICAL_THRESHOLD_MB = 1024
SCRIPT_DIR = Path(__file__).resolve().parent
TRIGGER_FILE = Path("/tmp/vosk_trigger")

try:
    TRIGGER_FILE.unlink()
except FileNotFoundError:
    pass # It might already be gone, which is fine

LOG_FILE = Path("/tmp/vosk_dictation.log")
HEARTBEAT_FILE = "/tmp/dictation_service.heartbeat"
PIDFILE = "/tmp/dictation_service.pid"
NOTIFY_SEND_PATH = "/usr/bin/notify-send"
XDOTOOL_PATH = "/usr/bin/xdotool"
SAMPLE_RATE = 16000

# --- LanguageTool Configuration ---
LANGUAGETOOL_URL = "http://localhost:8082/v2/check" # Standard-Port für LT ist 8081
LANGUAGETOOL_JAR_PATH = "/home/seeh/Downloads/LanguageTool-6.5/languagetool-server.jar"
# LANGUAGETOOL_JAR_PATH = "/home/seeh/Downloads/LanguageTool-6.5/languagetool.jar"

languagetool_process = None

# File: ~/projects/py/STT/dictation_service.py

def start_languagetool_server():
    global languagetool_process
    if not Path(LANGUAGETOOL_JAR_PATH).exists():
        print(f"FATAL: LanguageTool JAR not found at {LANGUAGETOOL_JAR_PATH}")
        return False

    port = LANGUAGETOOL_URL.split(':')[-1].split('/')[0]
    fasttext_model_path = str(Path(LANGUAGETOOL_JAR_PATH).parent / "lid.176.bin")

    command = ["java", "-cp", LANGUAGETOOL_JAR_PATH, "org.languagetool.server.HTTPServer", "--port", port, "--allow-origin", "*"]

    # Only add the fastText parameter if the model file actually exists
    if Path(fasttext_model_path).exists():
        command.extend(["--fasttext-model", fasttext_model_path])
        print("Starting LanguageTool Server with fastText...")
    else:
        print("Starting LanguageTool Server (fastText model not found, performance may be reduced)...")

    try:
        dev_null = open(os.devnull, 'w')
        languagetool_process = subprocess.Popen(command, stdout=dev_null, stderr=dev_null)
    except Exception as e:
        print(f"FATAL: Failed to start LanguageTool Server process: {e}")
        return False

    print("Waiting for LanguageTool Server to be responsive...")
    for _ in range(15):
        try:
            ping_url = LANGUAGETOOL_URL.replace("/check", "/languages")
            response = requests.get(ping_url, timeout=1)
            if response.status_code == 200:
                print("LanguageTool Server is online.")
                return True
        except requests.exceptions.RequestException:
            pass
        print(".", end="", flush=True)
        time.sleep(1)

    print("\nFATAL: LanguageTool Server did not become responsive after startup.")
    stop_languagetool_server()
    return False




def stop_languagetool_server():
    """Stops the LanguageTool server process if it's running."""
    global languagetool_process
    if languagetool_process and languagetool_process.poll() is None:
        print("Fahre LanguageTool Server herunter...")
        languagetool_process.terminate()
        try:
            languagetool_process.wait(timeout=5)
            print("LanguageTool Server sauber beendet.")
        except subprocess.TimeoutExpired:
            print("LanguageTool Server reagiert nicht auf terminate, sende kill...")
            languagetool_process.kill()
        languagetool_process = None

# --- Cleanup & PID Management ---
def cleanup():
    """Remove heartbeat/PID files and stop the LT server on exit."""
    print("Räume auf und beende das Skript.")
    stop_languagetool_server()
    if os.path.exists(HEARTBEAT_FILE):
        os.remove(HEARTBEAT_FILE)
    if os.path.exists(PIDFILE):
        os.remove(PIDFILE)

atexit.register(cleanup)

with open(PIDFILE, 'w') as f:
    f.write(str(os.getpid()))

# --- Argumente & Modell-Pfad ---
MODEL_NAME_DEFAULT = "vosk-model-de-0.21"
parser = argparse.ArgumentParser(description="A real-time dictation service using Vosk.")
parser.add_argument('--vosk_model', help=f"Name of the Vosk model folder. Defaults to '{MODEL_NAME_DEFAULT}'.")
args = parser.parse_args()
VOSK_MODEL_FILEread = ''
VOSK_MODEL_FILE = "/tmp/vosk_model"
if os.path.exists(VOSK_MODEL_FILE):
    with open(VOSK_MODEL_FILE, 'r') as f:
        VOSK_MODEL_FILEread = f.read()
MODEL_NAME = args.vosk_model or VOSK_MODEL_FILEread or MODEL_NAME_DEFAULT
MODEL_PATH = SCRIPT_DIR / MODEL_NAME

def correct_text(text: str) -> str:
    if not text.strip():
        return text

    print(f"  -> Input to LT:  '{text}'")

    data = {
        'language': 'de-DE',
        'text': text,
        'level': 'picky',
        'enabledCategories': 'TYPOS,CASING,GRAMMAR'
    }

    try:
        response = requests.post(LANGUAGETOOL_URL, data=data, timeout=10)
        response.raise_for_status()

        matches = response.json().get('matches', [])
        if not matches:
            print(f"  <- Output from LT: (No changes)")
            return text

        sorted_matches = sorted(matches, key=lambda m: m['offset'])
        new_text_parts, last_index = [], 0

        for match in sorted_matches:
            new_text_parts.append(text[last_index:match['offset']])
            if match['replacements']:
                new_text_parts.append(match['replacements'][0]['value'])
            last_index = match['offset'] + match['length']

        new_text_parts.append(text[last_index:])
        corrected_text = "".join(new_text_parts)

        print(f"  <- Output from LT: '{corrected_text}'")

        # This part is only reached if a correction was possible.
        # We compare with the original text to be sure a change was made.
        if corrected_text != text:
             print("=> CORRECTION successfully applied.")
        else:
             print("=> NO CORRECTION needed.")

        return corrected_text

    except requests.exceptions.RequestException as e:
        print(f"  <- ERROR: LanguageTool request failed: {e}")
        print("=> NO CORRECTION applied due to an error.")
        # CORRECTED: Return the original text here to exit the function.
        return text


def check_memory_critical(threshold_mb: int) -> tuple[bool, float]:
    mem = psutil.virtual_memory()
    available_mb = mem.available / (1024 * 1024)
    return available_mb < threshold_mb, available_mb

PUNCTUATION_MAP = {
    # German - Correct and Common Mishearings
    'punkt': '.',
    'pumpt': '.',
    'punk': '.',
    'komma': ',',
    'fragezeichen': '?',
    'ausrufezeichen': '!',
    'doppelpunkt': ':',
    'semikolon': ';',
    'strichpunkt': ';',

    # English (for completeness)
    'period': '.',
    'full stop': '.',
    'dot': '.',

    'comma': ',',
    'question mark': '?',
    'christian monk': '?',
    'exclamation mark': '!',
    'exclamation point': '!',
    'colon': ':',
    'semicolon': ';',
}
def normalize_punctuation(text: str) -> str:
    pattern = r'\b(' + '|'.join(re.escape(key) for key in sorted(PUNCTUATION_MAP.keys(), key=len, reverse=True)) + r')\b'
    def replace(match):
        return PUNCTUATION_MAP[match.group(1).lower()]
    return re.sub(pattern, replace, text, flags=re.IGNORECASE)

def notify(summary, body="", urgency="low", icon=None):
    full_cmd = [NOTIFY_SEND_PATH, "-r", "9999", "-u", urgency, summary, body, "-t", "2000"]
    if icon: full_cmd.extend(["-i", icon])
    try: subprocess.run(full_cmd, check=True, capture_output=True, text=True)
    except:
        try: subprocess.run([NOTIFY_SEND_PATH, summary, body], check=True, capture_output=True, text=True)
        except Exception as e: print(f"NOTIFICATION FAILED: {summary} - {e}")

# File: ~/projects/py/STT/dictation_service.py

def transcribe_audio_with_feedback(recognizer):
    """
    Transcribes audio with a built-in timeout to prevent getting stuck on silence.
    """
    q = queue.Queue()
    def audio_callback(indata, frames, time, status):
        if status: print(status, file=sys.stderr)
        q.put(bytes(indata))

    recognizer.SetWords(True)
    notify("Vosk is Listening...", "Speak now. It will stop on silence.", "normal", icon="microphone-sensitivity-high-symbolic")

    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
            # Timeout configuration
            SILENCE_TIMEOUT = 2.0  # seconds of silence to stop
            last_audio_time = time.time()

            while time.time() - last_audio_time < SILENCE_TIMEOUT:
                try:
                    # Wait for audio data, but with a timeout to check our condition
                    data = q.get(timeout=0.5)
                    last_audio_time = time.time() # Reset timer on receiving audio

                    if recognizer.AcceptWaveform(data):
                        # This happens on a natural pause, we can stop early
                        break
                except queue.Empty:
                    # No audio received in the last 0.5s, loop will check main timeout
                    pass
    except Exception as e:
        notify("Vosk Error", f"Transcription error: {e}", icon="dialog-error")
        return ""
    finally:
        # Important: Get the final recognized text after the loop
        return json.loads(recognizer.FinalResult()).get('text', '')



print("--- Vosk dictation_service ---")

if not start_languagetool_server():
    sys.exit(1)

if not MODEL_PATH.exists():
    notify("Vosk StartError", f"Modell not found: {MODEL_PATH}", icon="dialog-error")
    sys.exit(1)

print(f"load Modell '{MODEL_NAME}'...")
try:
    model = vosk.Model(str(MODEL_PATH))
    message = f"{MODEL_NAME} loaded. Waiting for Signal."
    print(message)
    notify("Vosk ready", message, icon="media-record")
except Exception as e:
    notify("Vosk error", f"Modell {MODEL_NAME} not loaded: {e}", icon="dialog-error")
    sys.exit(1)

is_recording = False
last_check_time = time.time()
recording_time = 0
CHECK_INTERVAL_SECONDS = 3

try:
    # Setup the file system watcher
    inotify = INotify()
    watch_flags = flags.CREATE | flags.IGNORED
    # We watch the /tmp directory for events related to our trigger file
    wd = inotify.add_watch('/tmp', watch_flags)

    print("Service is now listening for triggers via inotify...")

    # This loop will now block and wait for events, consuming no CPU.
    while True:
        # Check for events from the OS
        for event in inotify.read(timeout=1):

            # We are only interested in the creation of our specific trigger file
            if event.name == TRIGGER_FILE.name and event.mask & flags.CREATE:
                print("\n--- Trigger received via inotify! Starting processing. ---")

                # Immediately remove the trigger to prevent re-triggering
                try:
                    TRIGGER_FILE.unlink()
                except FileNotFoundError:
                    pass # It might already be gone, which is fine

                # --- The entire processing logic is now inside the event handler ---
                try:
                    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
                    recognized_text = transcribe_audio_with_feedback(recognizer) # This part is still blocking

                    if recognized_text:
                        print(f"Transcribed: '{recognized_text}'")

                        processed_text = normalize_punctuation(recognized_text)
                        processed_text = correct_text(processed_text)

                        if re.match(r"^\w", processed_text):
                            if time.time() - recording_time < 20:
                                processed_text = ' ' + processed_text
                            recording_time = time.time()

                        pyperclip.copy(processed_text)
                        subprocess.run([XDOTOOL_PATH, "type", "--clearmodifiers", processed_text])
                    else:
                        notify("Vosk Dictation", "No text recognized.", icon="dialog-warning")
                finally:
                    notify("Vosk Dictation", "Processing finished.", "low", icon="microphone-sensitivity-off-symbolic")
                    print("--- Processing finished. Waiting for next trigger. ---\n")

        # heartbeat/memory check runs every second
        # when no trigger event is happening.
        current_time = time.time()
        if current_time - last_check_time > CHECK_INTERVAL_SECONDS:
            last_check_time = current_time
            is_critical, _ = check_memory_critical(CRITICAL_THRESHOLD_MB)
            if is_critical:
                print(f"CRITICAL: Low memory detected. Shutting down.")
                sys.exit(1)
            with open(HEARTBEAT_FILE, 'w') as f:
                f.write(str(int(time.time())))


except KeyboardInterrupt:
    print("\nService interrupted by user.")

finally:
    cleanup()
    notify("Vosk Service", "Service has been shut down.", "normal", icon="process-stop-symbolic")

