from scripts.py.func.get_project_root import get_aura_project_root
import subprocess
import time

def execute(match_data):
    # TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
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

    # Start-Session entkoppeln, damit das Fenster unabhängig von Aura bleibt
    subprocess.Popen(cmd, start_new_session=True)


    print("Suche wird im Terminal geöffnet…")
    time.sleep(0.060)
    raise Exception('no text after replacement')
