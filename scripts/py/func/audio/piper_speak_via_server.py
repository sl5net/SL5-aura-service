import requests
import sys

import threading


from ..config.dynamic_settings import DynamicSettings
settings = DynamicSettings()
from scripts.py.func.config.dynamic_settings import DynamicSettings

import time

_speech_lock = threading.Lock()

PIPER_SERVER_HOST = '127.0.0.1'
PIPER_SERVER_PORT = 5002
PIPER_SERVER_URL = f"https://{PIPER_SERVER_HOST}:{PIPER_SERVER_PORT}/speak"

from pathlib import Path


def piper_speak_via_server(text: str) -> bool:
    """Returns True only if Piper server is reachable, then speaks async."""
    try:
        requests.get(f"https://{PIPER_SERVER_HOST}:{PIPER_SERVER_PORT}/",
                     verify=False, timeout=1)  # nosec B501
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return False  # Piper nicht erreichbar → espeak Fallback greift

    speak(text, voice="de-de", pitch=50, blocking=False, use_espeak=False)
    return True

# scripts/py/func/audio/piper_speak_via_server.py:22
def speak(text, voice="de-de", pitch=50, blocking=False, use_espeak=False):
    if not text or not globals().get('SPEECH_ENABLED', True):
        return None

    def _do_speak(use_espeak2):
        try:
            with open('/tmp/speak_server_input.txt', 'w') as f:
                f.write(text)
            requests.post(PIPER_SERVER_URL, verify=False, timeout=60)  # nosec B501 - localhost only

            time.sleep(.1)

            p = Path("/tmp/speak_server_input.txt")
            try:
                p.unlink()
                print(f"Deleted: {p}")
            except FileNotFoundError:
                print(f"File not found: {p}")
            except PermissionError:
                print(f"Permission denied: {p}")
            except OSError as e:
                print(f"Error deleting {p}: {e}")

            return
        except requests.exceptions.ConnectionError:
            print("Piper Error !! Piper Server not running — Fallback to espeak")
        except Exception as e:
            print(f"Piper Error 2026-0306-2339: {e}", file=sys.stderr)
            return False

    t = threading.Thread(target=_do_speak, args=(use_espeak,))
    t.start()

    if blocking:
        t.join()

    return t  # statt Prozess jetzt Thread zurückgeben
