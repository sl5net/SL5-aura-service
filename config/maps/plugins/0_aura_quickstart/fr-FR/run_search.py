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

from scripts.py.func.get_project_root import get_aura_project_root
import subprocess
import time

def execute(match_data):
    # TMP_DIR = Chemin("C:/tmp") if platform.system() == "Windows" sinon Chemin("/tmp")

    # PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"

    # SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()


    SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()


    SEARCH_SCRIPT = SL5NET_AURA_PROJECT_ROOT / "scripts" / "search_rules" / "search_rules.sh"

    from scripts.py.func.config.dynamic_settings import settings

    sleep_sec = 0
    if settings.DEV_MODE:
        sleep_sec = 5

    cmd = [
        'konsole', '-e', 'bash', '-c',
        f'bash "{SEARCH_SCRIPT}"; sleep {sleep_sec}'
    ]

    # Découpler la session de démarrage pour que la fenêtre reste indépendante d'Aura

    subprocess.Popen(cmd, start_new_session=True)


    print("Suche wird im Terminal geöffnet…")
    time.sleep(0.060)
    raise Exception('no text after replacement')
