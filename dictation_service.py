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
import vosk

# --- Konfiguration ---
SCRIPT_DIR = Path(__file__).resolve().parent
MODEL_NAME = "vosk-model-de-0.21"
MODEL_NAME = "vosk-model-small-en-us-0.15"
MODEL_PATH = SCRIPT_DIR / MODEL_NAME
TRIGGER_FILE = Path("/tmp/vosk_trigger") # Unsere "Signal"-Datei

NOTIFY_SEND_PATH = "/usr/bin/notify-send"
XDOTOOL_PATH = "/usr/bin/xdotool"
SAMPLE_RATE = 16000

# --- Hilfsfunktionen ---
def notify(summary, body=""):
    try:
        subprocess.run([NOTIFY_SEND_PATH, summary, body, "-t", "2000"], check=True)
    except Exception:
        print(f"NOTIFY: {summary} - {body}")

def transcribe_audio():
    q = queue.Queue()
    def audio_callback(indata, frames, time, status):
        q.put(bytes(indata))

    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000,
                               dtype='int16', channels=1, callback=audio_callback):
            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    break
        result = json.loads(recognizer.Result())
        return result.get('text', '')
    except Exception as e:
        print(f"Fehler bei der Transkription: {e}")
        return ""

# --- Hauptlogik des Dienstes ---
print("--- Vosk Diktier-Dienst ---")
if not MODEL_PATH.exists():
    print(f"FATALER FEHLER: Modell nicht gefunden unter {MODEL_PATH}")
    sys.exit(1)

print(f"Lade Modell '{MODEL_NAME}'... Dies kann einige Sekunden dauern.")
try:
    model = vosk.Model(str(MODEL_PATH))
    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
    print("Modell erfolgreich geladen. Dienst wartet auf Signal.")
    notify("Vosk Dienst Bereit", "Hotkey ist nun aktiv.")
except Exception as e:
    print(f"FATALER FEHLER: Modell konnte nicht geladen werden. {e}")
    sys.exit(1)

# Der Haupt-Loop: Warten auf die Trigger-Datei
while True:
    try:
        if TRIGGER_FILE.exists():
            print("Signal erkannt! Starte Transkription.")
            notify("Vosk Hört zu...", "Jetzt sprechen.")
            TRIGGER_FILE.unlink() # Signal sofort entfernen

            recognized_text = transcribe_audio()

            if recognized_text:
                print(f"Transkribiert: '{recognized_text}'")
                subprocess.run([XDOTOOL_PATH, "type", "--clearmodifiers", recognized_text])
                pyperclip.copy(recognized_text)
            else:
                notify("Vosk Diktat", "Kein Text erkannt.")

        time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nDienst durch Benutzer beendet.")
        break
    except Exception as e:
        print(f"Fehler im Haupt-Loop: {e}")
        notify("Vosk Dienst Fehler", str(e))
