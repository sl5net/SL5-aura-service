import platform
import subprocess
import time
from pathlib import Path

def execute(match_data):

    # TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
    # PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
    # PROJECT_ROOT = Path(PROJECT_ROOT_FILE.read_text(encoding="utf-8"))

    PROJECT_ROOT = Path("/tmp/sl5_aura/sl5net_aura_project_root")

    SEARCH_SCRIPT = PROJECT_ROOT / "scripts" / "search_rules" / "search_rules.sh"

    cmd = [
        'konsole', '-e', 'bash', '-c',
        f'bash "{SEARCH_SCRIPT}"; exec bash'
    ]

    # Start-Session entkoppeln, damit das Fenster unabhängig von Aura bleibt
    subprocess.Popen(cmd, start_new_session=True)


    print("Suche wird im Terminal geöffnet...")
    time.sleep(0.060)
    exit(1)
