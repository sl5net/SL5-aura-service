# scripts/py/welcome_wizard/de-DE/start.py
import subprocess
import platform
from pathlib import Path

def run(project_root):
    d = project_root / "scripts" / "search_rules"
    search_script = d / "search_rules.bat" if platform.system() == "Windows" else d / "search_rules.sh"
    koan_dir = project_root / "config" / "maps" / "koans_deutsch"

    if not search_script.exists():
        return

    welcome_msg = (
        "=== WILLKOMMEN BEI AURA ===\\n\\n"
        "Ich habe dir die interaktiven Uebungen (Koans) geoeffnet.\\n"
        "Suche dir eine Aufgabe aus und druecke ENTER um sie in Kate zu oeffnen.\\n"
    )

    if platform.system() == "Windows":
        # Wir übergeben das Koan-Verzeichnis an die .bat
        # Windows handles background processes differently, usually no fix needed
        subprocess.Popen(['cmd', '/c', 'start', str(search_script), str(koan_dir)], start_new_session=True)
    else:
        cmd = [
            'konsole', '-e', 'bash', '-c',
            f'echo -e "{welcome_msg}"; sleep 2; bash {search_script} {koan_dir}; exec bash'
        ]
        # FIX: Wir fügen '; exec bash' am Ende hinzu.
        # Das ersetzt den Prozess am Ende durch eine echte, offene Shell.
        subprocess.Popen(cmd, start_new_session=True)
        # Auszug aus scripts/py/welcome_wizard/de-DE/start.py (Windows Sektion)
