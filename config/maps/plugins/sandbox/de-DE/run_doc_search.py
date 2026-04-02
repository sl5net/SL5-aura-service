import platform
import subprocess
import os
import time
from pathlib import Path

def execute(match_data=None):
    # 1. Projekt-Root finden (Deine bewährte Methode)
    tmp_dir = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
    root_file = tmp_dir / "sl5_aura" / "sl5net_aura_project_root"
    project_root = Path(root_file.read_text(encoding="utf-8").strip())
    search_script = project_root / "scripts" / "search_rules" / "search_rules.sh"
    # docs_dir = project_root / "docs"
    docs_dir = "docs"

    # 2. Aktuelle Sprache ermitteln (z.B. "de")
    current_lang = Path(__file__).parent.name.split("-")[0]


    file_filter = f"*-{current_lang}lang.md"

    env = os.environ.copy()

    # 3. Der saubere Aufruf mit ZWEI Parametern:
    # $1 = Der Ordner (docs)
    # $2 = Die Sprache (de)
    terminal_cmd = [
        'konsole', '-e', 'bash', '-c',
        f'bash "{search_script}" "{docs_dir}" "{current_lang}";'
    ]


    # (Hier ggf. deine Xauthority-Logik einfügen)

    # 4. Befehl für das Terminal
    # Wir übergeben den Filter direkt an das Such-Skript
    terminal_cmd = [
        'konsole', '-e', 'bash', '-c',
        f'SEARCH_FILES_FILTER="{file_filter}" bash "{search_script}" "{docs_dir}";'
    ]

    # 1. Locale erzwingen (behebt den ANSI_X3.4 Fehler)
    env["LANG"] = "de_DE.UTF-8"
    env["LC_ALL"] = "de_DE.UTF-8"

    # 2. DBus-Adresse sicherstellen (verhindert den Portal-Error)
    if "DBUS_SESSION_BUS_ADDRESS" not in env:
        # Standardpfad für den Session-Bus
        uid = os.getuid()
        env["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{uid}/bus"


    subprocess.Popen(terminal_cmd, start_new_session=True, env=env)

    print(f"Aura Hilfe: Suche wird auf {current_lang} begrenzt.")
    time.sleep(0.060)
    exit(1)
