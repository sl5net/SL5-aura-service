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
import logging  # ADDED: For logging
import platform
import threading

# --- Configuration ---

if platform.system() == "Windows":
    TMP_DIR = Path("C:/tmp")
    NOTIFY_SEND_PATH = None # Deaktiviert notify-send
else:
    TMP_DIR = Path("/tmp")

OUTPUT_FILE = TMP_DIR / "tts_output.txt"

# ERSETZE DIE ALTEN PFADE:
TRIGGER_FILE = TMP_DIR / "vosk_trigger"
# TRIGGER_FILE = Path("/tmp/vosk_trigger")

# HEARTBEAT_FILE = "/tmp/dictation_service.heartbeat"

HEARTBEAT_FILE = TMP_DIR / "dictation_service.heartbeat"

# PIDFILE = "/tmp/dictation_service.pid"
PIDFILE = TMP_DIR / "dictation_service.pid"


CRITICAL_THRESHOLD_MB = 1024
SCRIPT_DIR = Path(__file__).resolve().parent
LOG_FILE = Path("vosk_dictation.log")
NOTIFY_SEND_PATH = "/usr/bin/notify-send"
XDOTOOL_PATH = "/usr/bin/xdotool"
SAMPLE_RATE = 16000
# LANGUAGETOOL_URL = "http://localhost:8082/v2/check"

LANGUAGETOOL_BASE_URL = "http://localhost:8082"
LANGUAGETOOL_URL = f"{LANGUAGETOOL_BASE_URL}/v2/check"

LANGUAGETOOL_JAR_PATH = f"{SCRIPT_DIR}/LanguageTool-6.6/languagetool-server.jar"

languagetool_process = None

#Jetzt wird alles funktionieren

# --- Logging Setup (Must be first) ---
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
    if "-de-" in name:
        return "de-DE"
    elif "-en-" in name:
        return "en-US"
    elif "-fr-" in name:
        return "fr-FR"
    return "de-DE"






def start_languagetool_server():
    global languagetool_process
    if not Path(LANGUAGETOOL_JAR_PATH).exists():
        logger.fatal(f"LanguageTool JAR not found at {LANGUAGETOOL_JAR_PATH}")
        return False
    port = LANGUAGETOOL_URL.split(':')[-1].split('/')[0]
    logger.info("Starting LanguageTool Server...")

    command = [
        "java", "-jar", LANGUAGETOOL_JAR_PATH,
        "--port", port,
        "--allow-origin", "*"
    ]

    logger.info(f"LANGUAGETOOL_JAR_PATH: {LANGUAGETOOL_JAR_PATH}")
    logger.info(f"Command list: {command!r}")

    try:
        languagetool_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        logger.fatal(f"Failed to start LanguageTool Server process: {e}")
        languagetool_process = None
        return False

    logger.info("Waiting for LanguageTool Server to be responsive...")
    for _ in range(20):
        try:
            # ping_url = LANGUAGETOOL_URL.replace("/check", "/v2/languages")
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
            if stdout:
                logger.error(f"LanguageTool STDOUT:\n{stdout}")
            if stderr:
                logger.error(f"LanguageTool STDERR:\n{stderr}")
                # --- HERE IS THE TARGETED ERROR DETECTION ---
                if "ExceptionInInitializerError" in stderr and "common_words.txt" in stderr:
                    print("\n" + "="*60)
                    print("ERROR: LanguageTool failed to initialize correctly.")
                    print("This is a known issue on the first installation.")
                    print("\nPLEASE PERFORM THE FOLLOWING WORKAROUND:")
                    print(f"1. Delete the folder: '{SCRIPT_DIR / 'LanguageTool-6.6'}'")

                    notify("1. Delete the folder:", f"'{SCRIPT_DIR / 'LanguageTool-6.6'}'", "normal", icon="dialog-error")

                    print("2. Run the setup script again.")

                    notify("1. Delete the folder", "2. Run the setup script again.", "normal", icon="dialog-error")


                    print("="*60 + "\n")
            return False











        time.sleep(1)

    logger.fatal("LanguageTool Server did not become responsive.")
    stop_languagetool_server()
    if languagetool_process:
        stdout, stderr = languagetool_process.communicate()
        if stdout:
            logger.error(f"LanguageTool STDOUT on timeout:\n{stdout}")
        if stderr:
            logger.error(f"LanguageTool STDERR on timeout:\n{stderr}")
    else:
        logger.error("LanguageTool process was not started, cannot get output.")
    return False



def stop_languagetool_server():
    global languagetool_process
    if languagetool_process and languagetool_process.poll() is None:
        logger.info("Shutting down LanguageTool Server...")
        languagetool_process.terminate()
        try:
            languagetool_process.wait(timeout=5)
            logger.info("LanguageTool Server terminated.")
        except subprocess.TimeoutExpired:
            logger.warning("LanguageTool Server did not respond, killing process...")
            languagetool_process.kill()
        languagetool_process = None

def cleanup():
    logger.info("Cleaning up and exiting.")
    stop_languagetool_server()
    for f in [HEARTBEAT_FILE, PIDFILE, TRIGGER_FILE]:
        try:
            Path(f).unlink(missing_ok=True)
        except OSError as e:
            logger.warning(f"Could not remove {f}: {e}")

atexit.register(cleanup)
with open(PIDFILE, 'w') as f:
    f.write(str(os.getpid()))

MODEL_NAME_DEFAULT = "vosk-model-de-0.21"
parser = argparse.ArgumentParser(description="A real-time dictation service using Vosk.")
parser.add_argument('--vosk_model', help=f"Name of the Vosk model folder. Defaults to '{MODEL_NAME_DEFAULT}'.")
# parser.add_argument('--target-window', required=True, help="The window ID to send keystrokes to.")


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
    data = {
        'language': LT_LANGUAGE,
        'text': text,
        'maxSuggestions': 1
    }
    # if LT_LANGUAGE == "de-DE":
    #    data['enabledRules'] = ['DE_CASE']
    try:
        response = requests.post(LANGUAGETOOL_URL, data,
            timeout=10
        )
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

def check_memory_critical(threshold_mb: int) -> tuple[bool, float]:
    mem = psutil.virtual_memory()
    return mem.available / (1024 * 1024) < threshold_mb, mem.available / (1024 * 1024)

# PUNCTUATION_MAP = json.loads(f"{SCRIPT_DIR}/config/languagetool_server/PUNCTUATION_MAP.json")
from config.languagetool_server.PUNCTUATION_MAP import PUNCTUATION_MAP


# From GitHub  From GitHub  From GitHub

def normalize_punctuation(text: str) -> str:
    pattern = r'\b(' + '|'.join(re.escape(k) for k in sorted(PUNCTUATION_MAP, key=len, reverse=True)) + r')\b'
    return re.sub(pattern, lambda m: PUNCTUATION_MAP[m.group(1).lower()], text, flags=re.IGNORECASE)

# >>> THE NEW, PLATFORM-AWARE NOTIFY FUNCTION <<<
def notify(summary, body="", urgency="low", icon=None, duration=3000):
    """Sends a desktop notification, using the appropriate method for the OS."""
    logger.info(f"DEBUG: Attempting to notify: '{summary}'")

    if platform.system() == "Windows":
        try:
            # For Windows, we write to a file watched by an AHK script.
            # This avoids adding new dependencies and uses our existing toolchain.
            notify_file = TMP_DIR / "notification.txt"

            # Sanitize inputs to prevent issues with the separator
            clean_summary = summary.replace("|", "/")
            clean_body = body.replace("|", "/")

            # Create content in "Title|Body" format
            content = f"{clean_summary}|{clean_body}"
            notify_file.write_text(content, encoding='utf-8')
        except Exception as e:
            logger.error(f"Windows notification via file failed for '{summary}': {e}")

    else: # Linux logic
        if not NOTIFY_SEND_PATH or not Path(NOTIFY_SEND_PATH).exists():
            return # Silently fail if notify-send is not available
        try:
            command = [NOTIFY_SEND_PATH, "-u", urgency, summary, body, "-t", str(duration)]
            if icon:
                command.extend(["-i", icon])
            subprocess.run(command, check=True, capture_output=True, text=True, timeout=5)
        except Exception as e:
            logger.error(f"Linux notification failed for '{summary}': {e}")



def transcribe_audio_with_feedback(recognizer):
    q = queue.Queue()
    def audio_callback(indata, frames, time, status):
        if status: logger.warning(f"Audio status: {status}")
        q.put(bytes(indata))

    recognizer.SetWords(True)
    notify("Vosk is Listening...", "Speak now. It will stop on silence.", "normal", icon="microphone-sensitivity-high-symbolic")
    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
            SILENCE_TIMEOUT = 0.6
            last_audio_time = time.time()
            while time.time() - last_audio_time < SILENCE_TIMEOUT:
                try:
                    data = q.get(timeout=0.5)
                    last_audio_time = time.time()
                    if recognizer.AcceptWaveform(data):
                        break
                except queue.Empty:
                    pass
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        notify("Vosk Error", f"Transcription error: {e}", icon="dialog-error")
        return ""
    finally:
        return json.loads(recognizer.FinalResult()).get('text', '')


# --- Main Application Start ---
logger.info("--- Vosk dictation_service starting ---")
TRIGGER_FILE.unlink(missing_ok=True)

if not start_languagetool_server():
    notify("Vosk Startup Error", f"LanguageTool Server failed to start (LOG_FILE:{LOG_FILE}).", "critical")
    sys.exit(1)

if not MODEL_PATH.exists():
    notify("Vosk Startup Error", f"Model not found: {MODEL_PATH}", "critical")
    sys.exit(1)

logger.info(f"Loading model '{MODEL_NAME}'...")
try:
    model = vosk.Model(str(MODEL_PATH))
    message = f"{MODEL_NAME} loaded. Waiting for trigger."
    logger.info(message)
    notify("Vosk Ready", message, icon="media-record")
except Exception as e:
    notify("Vosk Error", f"Could not load model {MODEL_NAME}: {e}", "critical")
    sys.exit(1)

last_check_time = time.time()
recording_time = 0
CHECK_INTERVAL_SECONDS = 5


def process_and_output_text(text, output_path):
    """Processes the recognized text, corrects it, and writes it to the output file."""
    global recording_time
    logger.info(f"Transcribed: '{text}'")
    processed_text = normalize_punctuation(text)
    processed_text = correct_text(processed_text)

    # `recording_time` most be global
    global recording_time
    if re.match(r"^\w", processed_text) and time.time() - recording_time < 20:
        processed_text = ' ' + processed_text
    recording_time = time.time()

    Path(output_path).write_text(processed_text)
    notify("Transkribiert", duration=1000)


# In: dictation_service.py

# In dictation_service.py

def process_dictation_trigger(recognized_text):
    try:
        logger.info(f"THREAD: Received text to process: '{recognized_text}'") # NEU
        if recognized_text:
            timestamp = int(time.time() * 1000)
            unique_output_file = TMP_DIR / f"tts_output_{timestamp}.txt"
            logger.info(f"THREAD: Attempting to write to: {unique_output_file}") # NEU

            process_and_output_text(recognized_text, unique_output_file)
        else:
            logger.info("THREAD: Received empty text. Nothing to write.") # NEU
            notify("Vosk: No Input", "No text was recognized.", "normal")

    except Exception as e:
        logger.error(f"FATAL: Error in processing thread: {e}", exc_info=True)
        notify("Processing Error!", f"Thread failed: {e}", "critical")
    finally:
        logger.info("--- Background processing finished. ---")






















try:
    if platform.system() == "Linux":
        from inotify_simple import INotify, flags
        inotify = INotify()
        inotify.add_watch(TMP_DIR, flags.CREATE)
        logger.info("418: Listening for triggers via inotify...")
        while True:
            proc = subprocess.run(
                ['inotifywait', '-q', '-e', 'create', '--format', '%f', str(TMP_DIR)],
                capture_output=True, text=True
            )

            # Prüfen, ob die erstellte Datei unser Trigger ist
            if proc.stdout.strip() == TRIGGER_FILE.name:
                logger.info("TRIGGER DETECTED!")
                TRIGGER_FILE.unlink(missing_ok=True) # Trigger aufräumen

                # Die bekannte Logik von hier an...
                recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
                text_to_process = transcribe_audio_with_feedback(recognizer)
                thread = threading.Thread(target=process_dictation_trigger, args=(text_to_process,))
                thread.start()


            time.sleep(0.02)
            Path(HEARTBEAT_FILE).write_text(str(int(time.time())))
    else:
        # Windows-Logik mit Threading (konsistent)
        logger.info("Listening for triggers via file polling...")
        while True:
            if TRIGGER_FILE.exists():
                TRIGGER_FILE.unlink(missing_ok=True)
                recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
                text_to_process = transcribe_audio_with_feedback(recognizer)
                thread = threading.Thread(target=process_dictation_trigger, args=(text_to_process, OUTPUT_FILE))
                thread.start()
            time.sleep(0.02)
            Path(HEARTBEAT_FILE).write_text(str(int(time.time())))

except Exception as e:
    logger.error("FATAL ERROR in main loop:", exc_info=True)
    notify("Vosk Service CRASHED", f"Error: {e}", "critical")

except KeyboardInterrupt:
    logger.info("\nService interrupted by user.")
finally:
    cleanup()
    notify("Vosk Service", "Service has been shut down.", "normal", icon="process-stop-symbolic")


