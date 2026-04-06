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

    match_obj = match_data['regex_match_obj']

    dirpath = match_obj.group('dirpath').strip()

    # Sammlung: konsekration
    print('_________________________')
    print(f'dirpath: {dirpath}')




    docs_dir = dirpath

    docs_dir = 'config'
    print(f'hardcoded docs_dir: {docs_dir} , dirpath: {dirpath}')
    #

    current_lang = Path(__file__).parent.name.split("-")[0]
    file_filter = f"*-{current_lang}lang.md"

    if docs_dir == 'config':
        file_filter = "settings*.py"
    else:
        file_filter = "*.py"
#roter KonföderationAura schüchtern KonfigurationenDora suche KonfigurationOver such a good vibrationsO suche Konfiguration


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
