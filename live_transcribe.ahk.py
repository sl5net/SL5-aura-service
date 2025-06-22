# recomandet hotkey: CTRL+ALT+D

import subprocess
import time
from pathlib import Path

# --- config ---
service_name = "dictation_service.py"
trigger_file = Path("/tmp/vosk_trigger")

# Path
home_dir = Path.home()
project_dir = home_dir / "projects" / "py" / "STT"
python_executable = project_dir / "vosk-tts" / "bin" / "python"
service_script_path = project_dir / service_name

# --- Hauptlogik ---

# Wir benutzen 'pgrep', ein Standard-Linux-Tool, um nach laufenden Prozessen zu suchen.
# '-f' durchsucht die gesamte Befehlszeile nach dem Namen unseres Skripts.
check_command = ['pgrep', '-f', service_name]

# Wir führen den Befehl aus und fangen das Ergebnis ab.
result = subprocess.run(check_command, capture_output=True)

# PRÜFUNG: Ist der Dienst bereits gestartet?
# pgrep gibt den Exit-Code 0 zurück, wenn es einen Prozess findet.
if result.returncode != 0:
    system.exec_command("notify-send 'Vosk Service' 'Dienst wird gestartet... Bitte warten.' -t 4000")
    start_command = f"{python_executable} {service_script_path} &"
    system.exec_command(start_command)
    time.sleep(5)

system.exec_command(f'touch {trigger_file}')


exit(1)

system.exec_command('touch /tmp/vosk_trigger')

exit(1)

from pathlib import Path

home_dir = str(Path.home())
command_to_run = f'/home/seeh/projects/py/STT/vosk-tts/bin/python /home/seeh/projects/py/STT/dictate.py {home_dir}'
system.exec_command(command_to_run)

