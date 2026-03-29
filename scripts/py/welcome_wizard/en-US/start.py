# scripts/py/welcome_wizard/en-US/start.py
import subprocess
from pathlib import Path

def run(project_root):
    # Path to the search script
    search_script = project_root / "scripts" / "search_rules" / "search_rules.sh"

    if not search_script.exists():
        return

    # Welcome message for the user
    welcome_msg = "=== AURA WELCOME ===\\n\\nAura is active. Press your hotkey to speak.\\n\\nI am opening the search for you now..."

    # Start konsole (KDE/Manjaro). '--hold' keeps the window open.
    # We display the welcome message, wait 2 seconds, then launch the search tool.
    cmd = [
        'konsole', '--hold', '-e', 'bash', '-c',
        f'echo -e "{welcome_msg}"; sleep 2; bash {search_script}'
    ]

    try:
        subprocess.Popen(cmd, start_new_session=True)
    except Exception as e:
        print(f"Error starting the English Wizard: {e}")

