# config/maps/plugins/standard_actions/count_loud/de-DE/count_loud.py
# import sys
from pathlib import Path
import subprocess

RULES_FILE_PATH = Path(__file__).parent / 'FUZZY_MAP_pre.py'
def speak(text):
    from scripts.py.func.audio_manager import speak_inclusive_fallback
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        subprocess.run(['espeak', '-v', 'de', text], check=True)
    except Exception as e:
        print(f"STDOUT (TTS-Fallback): {text} , {e}")

def on_file_load():
    from scripts.py.func.audio_manager import speak_inclusive_fallback
    # This must be defined to show up in the attributes list
    for i in range(10):
        speak_inclusive_fallback(f"in DE: {i}", 'de-DE')

def on_plugin_load():
    from scripts.py.func.audio_manager import speak_inclusive_fallback
    for i in range(4):
        speak_inclusive_fallback(f"in DE: {i}", 'de-DE')

def on_reload():
    from scripts.py.func.audio_manager import speak_inclusive_fallback
    for i in range(2):
        speak_inclusive_fallback(f"in DE: {i}", 'de-DE')

def on_folder_change(current_dir=None):
    from scripts.py.func.audio_manager import speak_inclusive_fallback
    for i in range(1):
        speak_inclusive_fallback(f"in DE: {i}", 'de-DE')

