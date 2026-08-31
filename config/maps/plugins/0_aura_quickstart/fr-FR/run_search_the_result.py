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
import subprocess
import time


def execute(match_data):
    import os as o
    from pathlib import Path as p
    with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())

    search_script = SL5NET_AURA_PROJECT_ROOT / "scripts" / "search_rules" / "search_rules.sh"
    env = os.environ.copy()
    env.setdefault("DISPLAY", ":0")
    env.setdefault("DBUS_SESSION_BUS_ADDRESS", "unix:path=/run/user/1000/bus")

    # match_obj = match_data['regex_match_obj']


    text_after_replacement = match_data['text_after_replacement']
    docs_dir = text_after_replacement
    if docs_dir == 'config':
        file_filter = "settings*.py"
    elif docs_dir == '~/dokumente' or docs_dir == '~/Dokumente':
        docs_dir = '~/Dokumente'
        file_filter = "*.pdf|*.png|*.jpg"
    elif docs_dir == 'log':
        file_filter = "*.log"
    # elif docs_dir == '~/documents' :

    # docs_dir = '~/Documents'

    # fichier_filter = "*.md"

    else:
        file_filter = "*.py|*.txt|*.md"
        print(f'exit docs_dir = {docs_dir} 2026-0407-1220')
        # exit(1)Sortie vers les moteursGrand-père backEra suffixes

    #
    # Les stupides documents du Jura Hourra, je te cherche pour venir. Dora, je t'attends pour venir

    # current_lang = Chemin(__file__).parent.name.split("-")[0]

    # file_filter = f"*-{current_lang}lang.md"

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
    execute('')
# python3 ./config/maps/plugins/ /de-DE/run_doc_search.py

