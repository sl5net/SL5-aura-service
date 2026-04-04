import platform
import subprocess
import os
import time
import glob
import shutil
from pathlib import Path

def execute(match_data=None):
    # 1. Projekt-Root finden (Deine bewährte Methode)
    is_windows = platform.system() == "Windows"
    tmp_dir = Path("C:/tmp") if is_windows else Path("/tmp")
    root_file = tmp_dir / "sl5_aura" / "sl5net_aura_project_root"

    if not root_file.exists():
        return
    project_root = Path(root_file.read_text(encoding="utf-8").strip())


    # 2. Such-Skript und Terminal-Befehl wählen
    if is_windows:
        search_script = project_root / "scripts" / "search_rules" / "search_rules.bat"
        # Auf Windows schließt cmd automatisch nach Beenden der bat
        terminal_cmd = ['cmd.exe', '/c', 'start', '/wait', str(search_script)]
        env = os.environ.copy()

    else:
        # search_script = project_root / "scripts" / "search_rules" / "search_rules.sh"
        search_script = project_root / "scripts" / "search_rules" / "search_rules.sh"

        # Terminal-Detektor
        terminal = None
        for t in ['konsole', 'gnome-terminal', 'xfce4-terminal', 'xterm']:
            if shutil.which(t):
                terminal = t
                break

        if not terminal: return

        # Umgebung für Linux-Grafik (Xauth-Fix)
        env = os.environ.copy()
        uid = os.getuid()
        xauth_candidates = glob.glob(f"/run/user/{uid}/xauth_*")
        env["XAUTHORITY"] = xauth_candidates[0] if xauth_candidates else os.path.expanduser("~/.Xauthority")
        if "DISPLAY" not in env: env["DISPLAY"] = ":0"

        # CLEAN FIX: Wir rufen NUR das Such-Skript auf.
        # Ohne 'exec bash' schließt sich das Fenster sofort nach dem Skript.
        # terminal_cmd = [terminal, '-e', 'bash', str(search_script)]

        terminal_cmd = [
            'systemd-run', '--user', '--collect', '--quiet', '--description=AuraSearch',
            terminal, '-e', 'bash', '-c', f'bash "{search_script}";'
        ]



    # 1. Locale erzwingen (behebt den ANSI_X3.4 Fehler)
    env["LANG"] = "de_DE.UTF-8"
    env["LC_ALL"] = "de_DE.UTF-8"

    # 2. DBus-Adresse sicherstellen (verhindert den Portal-Error)
    if "DBUS_SESSION_BUS_ADDRESS" not in env:
        # Standardpfad für den Session-Bus
        uid = os.getuid()
        env["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{uid}/bus"

    # 3. Starten
    #

    subprocess.Popen(terminal_cmd, start_new_session=True, env=env, cwd=str(project_root))

    # 4. Deine Aura-Pflicht-Sequenz (Sleep + Exit)
    print("Suche gestartet. Session wird beendet...")
    time.sleep(0.060)
    if match_data is not None:
        exit(1)

if __name__ == "__main__":
    execute()
