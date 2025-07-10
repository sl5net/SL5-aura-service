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
import logging
import platform
import threading

# --- Configuration ---
suspicious_events = []
SUSPICIOUS_TIME_WINDOW = 90
SUSPICIOUS_THRESHOLD = 3

if platform.system() == "Windows":
    TMP_DIR = Path("C:/tmp")
    NOTIFY_SEND_PATH = None
else:
    TMP_DIR = Path("/tmp")

OUTPUT_FILE = TMP_DIR / "tts_output.txt"
TRIGGER_FILE = TMP_DIR / "vosk_trigger"
HEARTBEAT_FILE = TMP_DIR / "dictation_service.heartbeat"
PIDFILE = TMP_DIR / "dictation_service.pid"
SCRIPT_DIR = Path(__file__).resolve().parent
LOG_FILE = Path("vosk_dictation.log")
NOTIFY_SEND_PATH = "/usr/bin/notify-send"
XDOTOOL_PATH = "/usr/bin/xdotool"
SAMPLE_RATE = 16000
LANGUAGETOOL_BASE_URL = "http://localhost:8082"
LANGUAGETOOL_URL = f"{LANGUAGETOOL_BASE_URL}/v2/check"
LANGUAGETOOL_JAR_PATH = f"{SCRIPT_DIR}/LanguageTool-6.6/languagetool-server.jar"
languagetool_process = None

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)-8s - %(message)s',
    handlers=[
        logging.FileHandler(f'{SCRIPT_DIR}/vosk_dictation.log', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()

# --- Wrapper Script Check ---
if os.environ.get("DICTATION_SERVICE_STARTED_CORRECTLY") != "true":
    logger.fatal("FATAL: This script must be started using the 'activate-venv_and_run-server.sh' wrapper.")
    sys.exit(1)

def guess_lt_language_from_model(model_name):
    name = model_name.lower()
    if "-de-" in name: return "de-DE"
    elif "-en-" in name: return "en-US"
    elif "-fr-" in name: return "fr-FR"
    return "de-DE"

def start_languagetool_server():
    global languagetool_process
    if not Path(LANGUAGETOOL_JAR_PATH).exists():
        logger.fatal(f"LanguageTool JAR not found at {LANGUAGETOOL_JAR_PATH}")
        return False
    port = LANGUAGETOOL_URL.split(':')[-1].split('/')[0]
    logger.info("Starting LanguageTool Server...")
    command = ["java", "-jar", LANGUAGETOOL_JAR_PATH, "--port", port, "--allow-origin", "*"]
    try:
        languagetool_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        logger.fatal(f"Failed to start LanguageTool Server process: {e}")
        return False
    logger.info("Waiting for LanguageTool Server to be responsive...")
    for _ in range(20):
        try:
            ping_url = f"{LANGUAGETOOL_BASE_URL}/v2/languages"
            response = requests.get(ping_url, timeout=1.5)
            if response.status_code == 200:
                logger.info("LanguageTool Server is online.")
                return True
        except requests.exceptions.RequestException:
            pass
        if languagetool_process and languagetool_process.poll() is not None:
            logger.fatal("LanguageTool process terminated unexpectedly.")
            stdout, stderr = languagetool_process.communicate()
            if stderr: logger.error(f"LanguageTool STDERR:\n{stderr}")
            return False
        time.sleep(1)
    logger.fatal("LanguageTool Server did not become responsive.")
    stop_languagetool_server()
    return False

def stop_languagetool_server():
    global languagetool_process
    if languagetool_process and languagetool_process.poll() is None:
        logger.info("Shutting down LanguageTool Server...")
        languagetool_process.terminate()
        try:
            languagetool_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            languagetool_process.kill()
        languagetool_process = None

def cleanup():
    logger.info("Cleaning up and exiting.")
    stop_languagetool_server()
    for f in [HEARTBEAT_FILE, PIDFILE, TRIGGER_FILE]:
        f.unlink(missing_ok=True)

atexit.register(cleanup)
with open(PIDFILE, 'w') as f:
    f.write(str(os.getpid()))

# --- Argument Parsing und Model-Setup ---
MODEL_NAME_DEFAULT = "vosk-model-de-0.21"
parser = argparse.ArgumentParser(description="A real-time dictation service using Vosk.")
parser.add_argument('--vosk_model', help=f"Name of the Vosk model folder. Defaults to '{MODEL_NAME_DEFAULT}'.")
parser.add_argument('--test-text', help="Bypass microphone and use this text for testing.")
args = parser.parse_args()
VOSK_MODEL_FILE = SCRIPT_DIR / "config/model_name.txt"
vosk_model_from_file = Path(VOSK_MODEL_FILE).read_text().strip() if Path(VOSK_MODEL_FILE).exists() else ""
MODEL_NAME = args.vosk_model or vosk_model_from_file or MODEL_NAME_DEFAULT
MODEL_PATH = SCRIPT_DIR / "models" / MODEL_NAME
LT_LANGUAGE = guess_lt_language_from_model(MODEL_NAME)

def correct_text(text: str) -> str:
    if not text.strip(): return text
    logger.info(f"  -> Input to LT:  '{text}'")
    data = {'language': LT_LANGUAGE, 'text': text, 'maxSuggestions': 1}
    try:
        response = requests.post(LANGUAGETOOL_URL, data, timeout=10)
        response.raise_for_status()
        matches = response.json().get('matches', [])
        if not matches:
            logger.info("  <- Output from LT: (No changes)")
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
        logger.info(f"  <- Output from LT: '{corrected_text}'")
        return corrected_text
    except requests.exceptions.RequestException as e:
        logger.error(f"  <- ERROR: LanguageTool request failed: {e}")
        return text

from config.languagetool_server.PUNCTUATION_MAP import PUNCTUATION_MAP
def normalize_punctuation(text: str) -> str:
    pattern = r'\b(' + '|'.join(re.escape(k) for k in sorted(PUNCTUATION_MAP, key=len, reverse=True)) + r')\b'
    return re.sub(pattern, lambda m: PUNCTUATION_MAP[m.group(1).lower()], text, flags=re.IGNORECASE)

def notify(summary, body="", urgency="low", icon=None, duration=3000):
    logger.info(f"DEBUG: Attempting to notify: '{summary}'")
    if platform.system() == "Windows":
        # ... Windows logic ...
        pass
    else:
        if not NOTIFY_SEND_PATH or not Path(NOTIFY_SEND_PATH).exists(): return
        try:
            command = [NOTIFY_SEND_PATH, "-u", urgency, summary, body, "-t", str(duration)]
            if icon: command.extend(["-i", icon])
            subprocess.run(command, check=True, capture_output=True, text=True, timeout=5)
        except Exception as e:
            logger.error(f"Linux notification failed for '{summary}': {e}")

def transcribe_audio_with_feedback(recognizer,LT_LANGUAGE):
    q = queue.Queue()
    def audio_callback(indata, frames, time, status):
        if status: logger.warning(f"Audio status: {status}")
        q.put(bytes(indata))
    recognizer.SetWords(True)
    notify(f"Vosk is Listening {LT_LANGUAGE} ...", "Speak now. It will stop on silence.", "normal", icon="microphone-sensitivity-high-symbolic")
    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
            SILENCE_TIMEOUT = 0.4
            last_audio_time = time.time()
            while time.time() - last_audio_time < SILENCE_TIMEOUT:
                try:
                    data = q.get(timeout=0.3)
                    last_audio_time = time.time()
                    if recognizer.AcceptWaveform(data):
                        break
                except queue.Empty:
                    pass
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return ""
    finally:
        return json.loads(recognizer.FinalResult()).get('text', '')

# --- Model Loading und Server-Start ---
logger.info("--- Vosk dictation_service starting ---")
TRIGGER_FILE.unlink(missing_ok=True)
if not start_languagetool_server():
    notify("Vosk Startup Error", "LanguageTool Server failed to start.", "critical")
    sys.exit(1)
if not MODEL_PATH.exists():
    notify("Vosk Startup Error", f"Model not found: {MODEL_PATH}", "critical")
    sys.exit(1)
try:
    model = vosk.Model(str(MODEL_PATH))
    logger.info(f"{MODEL_NAME} loaded. Waiting for trigger.")
    notify("Vosk Ready", f"{MODEL_NAME} loaded.", icon="media-record")
except Exception as e:
    notify("Vosk Error", f"Could not load model {MODEL_NAME}: {e}", "critical")
    sys.exit(1)

# --- Kernlogik für die Verarbeitung (läuft im Thread) ---
recording_time = 0
def process_text_in_background(raw_text):
    global recording_time
    try:
        if not raw_text:
            return
        logger.info(f"THREAD: Starting processing for: '{raw_text}'")
        processed_text = normalize_punctuation(raw_text)
        processed_text = correct_text(processed_text)
        if re.match(r"^\w", processed_text) and time.time() - recording_time < 20:
            processed_text = ' ' + processed_text
        recording_time = time.time()
        timestamp = int(time.time() * 1000)
        unique_output_file = TMP_DIR / f"tts_output_{timestamp}.txt"
        unique_output_file.write_text(processed_text)
        logger.info(f"THREAD: Successfully wrote to {unique_output_file}")
        notify("Transkribiert", duration=1000)
    except Exception as e:
        logger.error(f"FATAL: Error in processing thread: {e}", exc_info=True)
    finally:
        logger.info(f"--- Background processing for '{raw_text[:20]}...' finished. ---")

# --- Hauptschleife (Main Thread) ---
def main():
    global suspicious_events, LT_LANGUAGE
    active_threads = []

    try:
        if platform.system() == "Linux":
            logger.info(f"Listening for triggers via inotifywait on '{TMP_DIR}'. Waiting for '{TRIGGER_FILE.name}'.")
            while True:
                active_threads = [t for t in active_threads if t.is_alive()]
                try:
                    proc = subprocess.run(
                        ['inotifywait', '-q', '-e', 'create,close_write', '--format', '%f', str(TMP_DIR)],
                        capture_output=True, text=True, timeout=5
                    )
                    if proc.stdout.strip() == TRIGGER_FILE.name:
                        logger.info(f"TRIGGER DETECTED via inotifywait! Active threads: {len(active_threads)}")
                        TRIGGER_FILE.unlink(missing_ok=True)
                        recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
                        raw_text = transcribe_audio_with_feedback(recognizer, LT_LANGUAGE)
                        if not raw_text.strip() or len(raw_text.split()) < 1:
                            suspicious_events.append(time.time())
                        now = time.time()
                        suspicious_events = [t for t in suspicious_events if now - t < SUSPICIOUS_TIME_WINDOW]
                        if len(suspicious_events) >= SUSPICIOUS_THRESHOLD:
                            notify(
                                "Tipp: Aufnahme zu kurz?",
                                "Die Aufnahme stoppt sehr schnell. Erwäge, den SILENCE_TIMEOUT auf 0.8 oder 1.0 zu setzen.",
                                "normal"
                            )
                            suspicious_events = []
                        if raw_text.strip():
                            thread = threading.Thread(target=process_text_in_background, args=(raw_text,))
                            thread.start()
                            active_threads.append(thread)
                except subprocess.TimeoutExpired:
                    pass
                Path(HEARTBEAT_FILE).write_text(str(int(time.time())))
        else:
            # Polling
            logger.info("Listening for triggers via file polling...")
            while True:
                if TRIGGER_FILE.exists():
                    pass
                time.sleep(0.2)
                Path(HEARTBEAT_FILE).write_text(str(int(time.time())))

    except Exception as e:
        logger.error("FATAL ERROR in main loop:", exc_info=True)
    except KeyboardInterrupt:
        logger.info("\nService interrupted by user.")
    finally:
        logger.info("Waiting for all background threads to finish...")
        for t in active_threads:
            t.join()
        cleanup()
        notify("Vosk Service", "Service has been shut down.", "normal")

if __name__ == "__main__":
    main()


