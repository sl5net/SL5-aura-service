# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# /de-DE/run_doc_search.py

import os
import re
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

    match_obj = match_data['regex_match_obj']

    dirpath_spoken = match_obj.group('dirpath').strip()

    # Collection: consecration

    docs_dir = None
    print('_________________________')
    print(f'dirpath_spoken: {dirpath_spoken}')
    assign_re = re.compile(r'^(?:Config\w*|config\w*|configuration|consecration)$', re.IGNORECASE)
    m = assign_re.match(dirpath_spoken)
    if m:
        docs_dir = 'config'
        file_filter = "*.py"
    else:
        assign_re = re.compile(r'^(?:Document\w*|document\w*)$', re.IGNORECASE)
        if m:
            docs_dir = '~/Documents'
            file_filter = "*.md"

    # ~/Documents


    docs_dir = dirpath_spoken

    docs_dir = 'config'
    print(f'hardcoded docs_dir: {docs_dir} , dirpath: {dirpath_spoken}')

    current_lang = Path(__file__).parent.name.split("-")[0]
    file_filter = f"*-{current_lang}lang.md"

    if docs_dir == 'config':
        file_filter = "settings*.py"
    else:
        file_filter = "*.py"
# red confederationAura shy ConfigurationsDora search configurationOver such a good vibrationsO search configuration


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
# python3 ./config/maps/plugins/ /de-DE/run_doc_search.py

