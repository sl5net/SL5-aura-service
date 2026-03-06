import requests
import sys

import threading


from ..config.dynamic_settings import DynamicSettings
settings = DynamicSettings()
from scripts.py.func.config.dynamic_settings import DynamicSettings


_speech_lock = threading.Lock()

PIPER_SERVER_HOST = '127.0.0.1'
PIPER_SERVER_PORT = 5002
PIPER_SERVER_URL = f"https://{PIPER_SERVER_HOST}:{PIPER_SERVER_PORT}/speak"


def piper_speak_via_server(text: str) -> bool:
    return speak(text, voice="de-de", pitch=50, blocking=False, use_espeak=False)

def speak(text, voice="de-de", pitch=50, blocking=False, use_espeak=False):
    if not text or not globals().get('SPEECH_ENABLED', True):
        return None

    def _do_speak(use_espeak2):
        try:
            with open('/tmp/speak_server_input.txt', 'w') as f:
                f.write(text)
            requests.post(PIPER_SERVER_URL, verify=False, timeout=60)
            return
        except requests.exceptions.ConnectionError:
            print("Piper Error !! Piper Server nicht erreichbar — Fallback zu espeak")
        except Exception as e:
            print(f"Piper Error 2026-0306-2339: {e}", file=sys.stderr)
            return False

    t = threading.Thread(target=_do_speak, args=(use_espeak,))
    t.start()

    if blocking:
        t.join()

    return t  # statt Prozess jetzt Thread zurückgeben
