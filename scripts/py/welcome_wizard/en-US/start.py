# scripts/py/welcome_wizard/en-US/start.py
import subprocess
import platform

def run(project_root):
    d = project_root / "scripts" / "search_rules"
    search_script = d / "search_rules.bat" if platform.system() == "Windows" else d / "search_rules.sh"

    # Target: Interactive tutorials (Koans)
    # Adjust directory name if it's different in your repository
    koan_dir = project_root / "config" / "maps" / "koans_deutsch"

    if not search_script.exists():
        return

    welcome_msg_20260402 = (
        "=== WELCOME TO AURA ===\\n\\n"
        "I've opened the interactive tutorials (Koans) for you.\\n"
        "Pick a lesson and start exploring Aura!\\n"
    )

    welcome_msg = (
        "=== WELCOME TO AURA 🔭 ===\\n\\n"
        "Aura is your telescope for the PC: Control from a distance!\\n\\n"
        "TIP: Say 'Teleskop' during recording to toggle the\\n"
        "pause function (SUSPENDED) on or off.\\n\\n"
        "Opening interactive tutorials (Koans) now..."
    )


    if platform.system() == "Windows":
        subprocess.Popen(['cmd', '/c', 'start', str(search_script), str(koan_dir)], start_new_session=True)

    else:
        cmd = [
            'konsole', '--hold', '-e', 'bash', '-c',
            #f'echo -e "{welcome_msg}"; sleep 2; bash {search_script} {koan_dir}'
            f'echo -e "{welcome_msg}"; sleep 2; bash {search_script} {koan_dir}; exec bash'
        ]
        subprocess.Popen(cmd, start_new_session=True)
