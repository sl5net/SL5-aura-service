# /de-DE/run_doc_search.py
import os
import subprocess
import time
from pathlib import Path

from scripts.py.func.get_project_root import get_aura_project_root


def execute(match_data):
    SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()


    search_script = SL5NET_AURA_PROJECT_ROOT / "scripts" / "search_rules" / "search_rules.sh"
    env = os.environ.copy()
    env.setdefault("DISPLAY", ":0")
    env.setdefault("DBUS_SESSION_BUS_ADDRESS", "unix:path=/run/user/1000/bus")
    docs_dir = "docs"
    current_lang = Path(__file__).parent.name.split("-")[0]
    file_filter = f"*-{current_lang}lang.md"

    from scripts.py.func.config.dynamic_settings import settings

    sleep_sec = 0
    if settings.DEV_MODE:
        sleep_sec = 5

    cmd = [
        'konsole', '-e', 'bash', '-c',
        f'SEARCH_FILES_FILTER="{file_filter}" bash "{search_script}" "{docs_dir}"; sleep {sleep_sec}'
    ]
    subprocess.Popen(cmd, start_new_session=True, env=env)
    print("Suche wird im Terminal geoeffnet…")
    time.sleep(0.060)

    raise Exception('no text after replacement')



if __name__ == "__main__":
    execute()
# python3 ./config/maps/plugins/   /de-DE/run_doc_search.py
