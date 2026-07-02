# config/maps/plugins/standard_actions/count_loud/de-DE/count_loud.py
#import sys
from pathlib import Path
import subprocess



RULES_FILE_PATH = Path(__file__).parent / 'FUZZY_MAP_pre.py'
def speak(text):
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        subprocess.run(['espeak', '-v', 'de', text], check=True)
    except Exception as e:
        print(f"STDOUT (TTS-Fallback): {text} , {e}")


def on_folder_change_OFF(current_dir=None):
    from scripts.py.func.audio_manager import speak_inclusive_fallback
    for i in range(1):
        speak_inclusive_fallback(f"out DE: {i}", 'en-US')

