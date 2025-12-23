# config/maps/plugins/standard_actions/count_loud/de-DE/count_loud.py
#import sys
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
#
#
# def on_reload():
#     speak("System reloaded")
#
#     #Test
#
# def on_folder_change(current_dir=None):
#     speak("Hallo Sonne 9") #TestTestTestTestTest Test
#
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

# count_loud.py
# (Second line: count_loud.py)
# standard_actions/count_loud/count_loud.py:37
def on_folder_change_OFF(current_dir=None):
    for i in range(1):
        speak_fallback(f"out DE: {i}",'en-US')

#Nochmal ausprobierennochmal
#Tipp Test
