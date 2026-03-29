import subprocess
import os
from pathlib import Path

def run(project_root):
    # Pfad zum Such-Skript
    search_script = project_root / "scripts" / "search_rules" / "search_rules.sh"

    if not search_script.exists():
        return

    # Nachricht für die Oma
    welcome_msg = "=== AURA WILLKOMMEN ===\\n\\nAura ist aktiv. Druecke deinen Hotkey zum Sprechen.\\n\\nIch oeffne jetzt die Suche fuer dich..."

    # Wir starten konsole. '--hold' lässt das Fenster offen.
    # Wir führen erst das Echo aus und dann das Such-Skript.
    cmd = [
        'konsole', '--hold', '-e', 'bash', '-c',
        f'echo -e "{welcome_msg}"; sleep 2; bash {search_script}'
    ]

    subprocess.Popen(cmd, start_new_session=True)
