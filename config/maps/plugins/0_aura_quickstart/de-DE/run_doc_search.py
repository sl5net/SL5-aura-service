# /de-DE/run_doc_search.py
import subprocess
import os
import time
from pathlib import Path


def execute(match_data):
    tmp_dir = Path("/tmp")
    PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())


    search_script = PROJECT_ROOT / "scripts" / "search_rules" / "search_rules.sh"
    env = os.environ.copy()
    env.setdefault("DISPLAY", ":0")
    env.setdefault("DBUS_SESSION_BUS_ADDRESS", "unix:path=/run/user/1000/bus")
    docs_dir = "docs"
    current_lang = Path(__file__).parent.name.split("-")[0]
    file_filter = f"*-{current_lang}lang.md"
    cmd = [
        'konsole', '-e', 'bash', '-c',
        f'SEARCH_FILES_FILTER="{file_filter}" bash "{search_script}" "{docs_dir}"; sleep 5'
    ]
    subprocess.Popen(cmd, start_new_session=True, env=env)
    print("Suche wird im Terminal geoeffnet...")
    time.sleep(0.060)
    exit(1)




if __name__ == "__main__":
    execute()
# python3 ./config/maps/plugins/   /de-DE/run_doc_search.py
