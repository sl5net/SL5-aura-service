# config/maps/plugins/standard_actions/count_loud/de-DE/count_loud.py
import sys
from pathlib import Path
import subprocess

RULES_FILE_PATH = Path(__file__).parent / 'FUZZY_MAP_pre.py'
def speak(text):
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        subprocess.run(['espeak', '-v', 'de', text], check=True)
    except Exception:
        print(f"STDOUT (TTS-Fallback): {text}")

# standard_actions/count_loud/de-DE/count_loud.py:14
def on_file_load():
    # This must be defined to show up in the attributes list
    speak("started 1")

def on_plugin_load():
    speak("einmal nur 20")


#

# def on_reload():
#     speak("System reloaded 1")
#
#     #Mal ausprobieren
#
# def on_folder_change(current_dir=None):
#     speak("Hallo Sonne 4") #desTestTestTestTestjkhlTestsdfsdf
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

#TestTestTest
