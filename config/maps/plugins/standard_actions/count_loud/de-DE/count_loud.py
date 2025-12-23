# config/maps/plugins/standard_actions/count_loud/de-DE/count_loud.py
# import sys
from pathlib import Path
import subprocess
from scripts.py.func.audio_manager import speak_fallback

RULES_FILE_PATH = Path(__file__).parent / 'FUZZY_MAP_pre.py'
def speak(text):
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        subprocess.run(['espeak', '-v', 'de', text], check=True)
    except Exception as e:
        print(f"STDOUT (TTS-Fallback): {text} , {e}")

# standard_actions/count_loud/de-DE/count_loud.py:14
#Tests
def on_file_load():
    # This must be defined to show up in the attributes list
    for i in range(10):
        speak_fallback(f"in DE: {i}",'de-DE')

def on_plugin_load():
    for i in range(4):
        speak_fallback(f"in DE: {i}",'de-DE')

def on_reload():
    for i in range(2):
        speak_fallback(f"in DE: {i}",'de-DE')

def on_folder_change(current_dir=None):
    for i in range(1):
        speak_fallback(f"in DE: {i}",'de-DE')

#TestDoch malnochmaltschüss JeffTipp

# def execute(match_data):
#
#     speak("Hallo Berg")
#
# def __main__():
#         speak("Hallo Baum")
#
#
#
# if __name__ == '__main__':
#     __main__()

#TestTestTest
