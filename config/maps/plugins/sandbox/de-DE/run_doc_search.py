# config/maps/plugins/sandbox/de-DE/run_doc_search.py
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
    # docs_dir = "./docs"
    docs_dir = "docs"
    # 2. Aktuelle Sprache ermitteln (z.B. "de")
    current_lang = Path(__file__).parent.name.split("-")[0]


    # config/maps/plugins/sandbox/de-DE/run_doc_search.py
    file_filter = f"*-{current_lang}lang.md"

    env = os.environ.copy()

    # 4. Befehl für das Terminal
    # Wir übergeben den Filter direkt an das Such-Skript
    # terminal_cmd = [
    #     'konsole', '-e', 'bash', '-c',
    #     f'SEARCH_FILES_FILTER="{file_filter}" bash "{search_script}" "{docs_dir}";'
    # ]
    # Eure DokumentationAura Dokumentation

    # Ersetze die alte terminal_cmd Zeile durch diese hier:
    terminal_cmd = [
        'systemd-run', '--user', '--collect', '--quiet',
        'konsole', '-e', 'bash', '-c',
        f'SEARCH_FILES_FILTER="{file_filter}" bash "{search_script}" "{docs_dir}" || sleep 5 ;'
    ]

    # 1. Locale erzwingen (behebt den ANSI_X3.4 Fehler)
    env["LANG"] = "de_DE.UTF-8"
    env["LC_ALL"] = "de_DE.UTF-8"

    # 2. DBus-Adresse sicherstellen (verhindert den Portal-Error)
    if "DBUS_SESSION_BUS_ADDRESS" not in env:
        # Standardpfad für den Session-Bus
        uid = os.getuid()
        env["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{uid}/bus"

    #
    # import glob
    # env = os.environ.copy()
    # xauth = glob.glob(f"/run/user/{os.getuid()}/xauth_*")
    # if xauth: env["XAUTHORITY"] = xauth[0]

    subprocess.Popen(terminal_cmd, start_new_session=True, env=env, cwd=str(project_root))
    #
    # subprocess.Popen(terminal_cmd, start_new_session=True, env=env)

    print(f"Aura Hilfe: Suche wird auf {current_lang} begrenzt.")
    time.sleep(0.060)
    exit(1)

if __name__ == "__main__":
    execute()
# python3 ./config/maps/plugins/sandbox/de-DE/run_doc_search.py
# Suche DokumentationAura Drucker bietet Schutz