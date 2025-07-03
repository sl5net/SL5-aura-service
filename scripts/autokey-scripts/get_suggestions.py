import subprocess
import time
from pathlib import Path
import os

SCRIPT_DIR = Path(__file__).resolve().parent


readmeBuckup = """
xdotool key --clearmodifiers ctrl+Left ctrl+shift+Right && sleep 0.1 && xdotool key --clearmodifiers ctrl+c && sleep 0.1 && {scriptDir}/.venv/bin/python {scriptDir}/vosk-tts/bin/python ~/projects/py/STT/get_suggestions.py
command = 'xdotool click 2 && sleep 0.1 && xdotool key --clearmodifiers "ctrl+c" && sleep 0.1 && {scriptDir}/vosk-tts/bin/python ~/projects/py/STT/get_suggestions.py'
system . exec_command (command)
Mond
"""

keyboard.send_keys('<ctrl>+<left>')
keyboard.send_keys('<ctrl>+<shift>+<right>')
keyboard.send_keys('<ctrl>+c')
time.sleep(0.2)
keyboard.send_keys('<right>')

home_dir = Path.home()

command = f"{home_dir}/projects/py/STT/.venv/bin/python {home_dir}/projects/py/STT/get_suggestions.py"
# clipboard.fill_clipboard(command)
# {SCRIPT_DIR}/.venv/bin/python {SCRIPT_DIR}/get_suggestions.py
# maus     Has Huns UAS Hulas Huts /home/seeh/.config/autokey/data/stt/autokey-scripts/.venv/bin/python /home/seeh/.config/autokey/data/stt/autokey-scripts/get_suggestions.py
system.exec_command (command)

# Haus ( aus | hass | hatz | hausse | ass )






