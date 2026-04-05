import subprocess
import os
import time
from pathlib import Path












def execute(match_data):
    tmp_dir = Path("/tmp")
    PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())


    SEARCH_SCRIPT = PROJECT_ROOT / "scripts" / "search_rules" / "search_rules.sh"

    env = os.environ.copy()
    env.setdefault("DISPLAY", ":0")
    env.setdefault("DBUS_SESSION_BUS_ADDRESS", "unix:path=/run/user/1000/bus")

    cmd = [
        'konsole', '-e', 'bash', '-c',
        f'bash "{SEARCH_SCRIPT}"; sleep 5'
    ]
    subprocess.Popen(cmd, start_new_session=True, env=env)
    print("Suche wird im Terminal geoeffnet...")
    time.sleep(0.060)
    exit(1)

if __name__ == "__main__":
    execute()
