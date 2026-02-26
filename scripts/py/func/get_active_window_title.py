# scripts/py/func/get_active_window_title.py
import sys
import os
import subprocess
import shutil
import json
import tempfile
from pathlib import Path

from scripts.py.func.checks.auto_zip_startup_test import readme

# --- GLOBALER CACHE (Memory) ---
_X11_ENV_CACHE = None

# --- DATEI CACHE (Disk - überlebt Reloads) ---
X11_CACHE_FILE = Path(tempfile.gettempdir()) / "sl5_aura" / "sl5_aura_x11_env.json"

# Source - https://stackoverflow.com/a/79895679
# Posted by HybridMoments
# Retrieved 2026-02-26, License - CC BY-SA 4.0

import subprocess
import time


def get_active_window_title_atspi():

    readme = """
    Konsole:


    pip install PyGObject
    
    maybe use when this is not working:
    
    python -m venv .venv --system-site-packages

    
    nano ~/.bashrc 
    nano ~/.config/fish/config.fish
        
    
    att to 
    Bash: export QT_ACCESSIBILITY=1
    Fish: set -gx QT_ACCESSIBILITY 1
    
    sudo pacman -S at-spi2-core qt6-declarative
    or shorter (maybe better)
    sudo pacman -S orca at-spi2-core
    
    kwriteconfig6 --file kaccessrc --group ScreenReader --key Enabled true
    
    echo "export QT_ACCESSIBILITY=1" >> ~/.bashrc
    echo "set -gx QT_ACCESSIBILITY 1" >> ~/.config/fish/config.fish
    
    
    Systemeinstellungen > Eingabehilfen > Eingabehilfen
    
    
    orca -s
    > disable language
    
    Test:
    dbus-send --print-reply --dest=org.a11y.Bus /org/a11y/bus org.a11y.Bus.GetAddress
    
    
    """

    # Wir laden die Atspi (Assistive Technology Service Provider Interface) Library

    import gi

    try:
        gi.require_version('Atspi', '2.0')
        from gi.repository import Atspi
    except Exception as e:
        print(f"Fehler: GObject-Introspection für Atspi fehlt. ({e})")
        exit(1)

    # Initialisiere Atspi Registry
    # 0 bedeutet Erfolg
    if Atspi.init() != 0:
        return "Atspi konnte nicht initialisiert werden."

    # Wir holen uns das "Desktop"-Objekt (die Wurzel aller Fenster)
    desktop = Atspi.get_desktop(0)

    # Wir gehen alle Anwendungen durch, die sich am A11Y-Bus angemeldet haben
    for i in range(desktop.get_child_count()):
        app = desktop.get_child_at_index(i)
        if not app:
            continue

        # Jede App kann mehrere Fenster haben
        for j in range(app.get_child_count()):
            window = app.get_child_at_index(j)
            if not window:
                continue

            # Wir prüfen den Status des Fensters
            state_set = window.get_state_set()
            states = state_set.get_states()

            # Die entscheidenden Zustände sind ACTIVE (Fenster aktiv)
            # oder FOCUSED (Eingabefokus)
            # Atspi.StateType.ACTIVE (2) oder Atspi.StateType.FOCUSED (4)
            if Atspi.StateType.ACTIVE in states or Atspi.StateType.FOCUSED in states:
                # Wir geben den Namen des Objekts zurück (das ist der Fenstertitel)
                return f"App: {app.get_name()} | Titel: {window.get_name()}"

    return "Kein aktives Fenster über AT-SPI gefunden."




def get_active_window_plasma6():
    script = "print(workspace.activeWindow.caption);"

    load_cmd = [
        "dbus-send", "--print-reply", "--dest=org.kde.KWin",
        "/Scripting", "org.kde.kwin.Scripting.loadScript",
        f"string:{script}"
    ]

    try:
        result = subprocess.run(load_cmd, capture_output=True, text=True, check=True)
        script_path = result.stdout.split('object path "')[1].split('"')[0]

        start_time = time.time()
        subprocess.run(["dbus-send", "--dest=org.kde.KWin", script_path, "org.kde.kwin.Script.run"], check=True)

        log_cmd = ["journalctl", "_COMM=kwin_wayland", "-o", "cat", f"--since=@{int(start_time)}"]
        logs = subprocess.run(log_cmd, capture_output=True, text=True).stdout

        subprocess.run(["dbus-send", "--dest=org.kde.KWin", script_path, "org.kde.kwin.Script.stop"])

        for line in logs.strip().split('\n'):
            if line.startswith("js:"):
                return line.replace("js: ", "").strip()
    except Exception as e:
        return f"Error: {e}"


# print(f"Active Window: {get_active_window_plasma6()}")


def get_linux_x11_env():
    """
    Ermittelt das Environment (DISPLAY, XAUTHORITY).
    Mit Timeout-Schutz gegen hängende Reads in /proc.
    """
    global _X11_ENV_CACHE

    # 1. Memory Cache
    if _X11_ENV_CACHE: return _X11_ENV_CACHE

    # 2. File Cache
    if X11_CACHE_FILE.exists():
        try:
            with open(X11_CACHE_FILE, "r") as f:
                cached_env = json.load(f)
            if os.path.exists(cached_env.get('XAUTHORITY', '')):
                _X11_ENV_CACHE = cached_env
                return cached_env
        except Exception as e:
            print(f'34 {e}')
            pass

    target_env = os.environ.copy()
    found_auth = False

    # A: Check existing
    if 'DISPLAY' in target_env and 'XAUTHORITY' in target_env:
        if os.path.exists(target_env['XAUTHORITY']):
            found_auth = True

    # B: Sniffer (/proc) - Jetzt robuster
    if not found_auth:
        try:
            # Limitieren auf max 50 Versuche, damit wir nicht ewig in /proc hängen
            pids = [p for p in os.listdir('/proc') if p.isdigit()]
            # Sortieren, neuere PIDs zuerst (wahrscheinlicher GUI apps)
            pids.sort(key=lambda x: int(x), reverse=True)

            for pid in pids[:100]: # Nur die neuesten 100 Prozesse scannen
                try:
                    # Timeout simulieren durch schnelles Lesen (non-blocking ist in Python schwer bei files)
                    # Wir lesen einfach und fangen jeden Fehler ab
                    env_path = f'/proc/{pid}/environ'
                    if not os.access(env_path, os.R_OK): continue

                    with open(env_path, 'rb') as f:
                        env_data = f.read(8192) # Max 8KB lesen, reicht für Env
                except Exception as e:
                    print(f'78 {e}')
                    continue

                try:
                    proc_env = {}
                    for item in env_data.split(b'\0'):
                        if b'=' in item:
                            parts = item.decode('utf-8', errors='ignore').split('=', 1)
                            if len(parts) == 2: proc_env[parts[0]] = parts[1]

                    if 'DISPLAY' in proc_env and 'XAUTHORITY' in proc_env:
                        if os.path.exists(proc_env['XAUTHORITY']):
                            target_env['DISPLAY'] = proc_env['DISPLAY']
                            target_env['XAUTHORITY'] = proc_env['XAUTHORITY']
                            found_auth = True
                            break
                except Exception as e:
                    print(f'78 {e}')
                    continue


        except Exception as e:
            print(f'201 {e}')
            pass

    # C: Fallback
    if not found_auth:
        possible_auths = [
            Path.home() / ".Xauthority",
            Path(f"/run/user/{os.getuid()}/gdm/Xauthority"),
            Path("/var/run/sddm")
        ]
        try: possible_auths.extend(list(Path("/var/run/sddm").glob("*")))
        except Exception as e:
            print(f'111 {e}')
            pass

        for p in possible_auths:
            if p.exists() and p.is_file():
                target_env['XAUTHORITY'] = str(p)
                target_env['DISPLAY'] = ':0'
                found_auth = True
                break

    # Save Cache SECURELY
    if found_auth:
        _X11_ENV_CACHE = target_env
        try:
            cache_data = {'DISPLAY': target_env.get('DISPLAY'), 'XAUTHORITY': target_env.get('XAUTHORITY')}

            # Erst öffnen/erstellen
            with open(X11_CACHE_FILE, "w") as f:
                # DANN Rechte einschränken (nur Owner darf lesen/schreiben)
                try:
                    Path(X11_CACHE_FILE).chmod(0o600)
                    os.chmod(X11_CACHE_FILE, 0o600)
                except Exception as e:
                    print(f'Failed to chmod {X11_CACHE_FILE}: {e}')
                    pass

                json.dump(cache_data, f)
        except Exception as e:
            print(f'111 {e}')
            pass

    return target_env


def get_active_window_title_safe():
    """
    Gibt den Titel des aktiven Fensters zurück (lowercase).
    Funktioniert auf Windows und Linux (auch als Service/Root).
    """
    try:
        # --- WINDOWS ---
        if sys.platform == 'win32':

            active_win_title_file_path = r"c:\tmp\activeWinTitle.txt"
            with open(active_win_title_file_path) as f:
                active_win_title = f.read()
                return active_win_title

            import ctypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            if length == 0: return None
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            return buff.value.lower()


        # --- LINUX WAYLAND ---

        # --- LINUX WAYLAND (KDE Fix) ---
        # return get_active_window_plasma6()



        if os.environ.get('XDG_SESSION_TYPE') == 'wayland' or os.environ.get('WAYLAND_DISPLAY'):

            print(f'🔵🔵🔵{get_active_window_title_atspi()}🔵🔵🔵')
            exit(1)

            return get_active_window_title_atspi()

            try:
                # 1. Aktiven Fenster-Pfad über dbus-send holen (Standard-Tool)
                cmd_id = ["dbus-send", "--session", "--print-reply", "--dest=org.kde.KWin", "/KWin",
                          "org.kde.KWin.activeWindow"]
                out_id = subprocess.check_output(cmd_id, stderr=subprocess.DEVNULL).decode()
                # Extrahiert den Pfad (z.B. /Windows/W1)
                win_path = out_id.split('objpath "')[1].split('"')[0]

                # 2. Titel (caption) für diesen Pfad holen
                cmd_title = ["dbus-send", "--session", "--print-reply", "--dest=org.kde.KWin", win_path,
                             "org.freedesktop.DBus.Properties.Get", "string:org.kde.KWin.Window", "string:caption"]
                out_title = subprocess.check_output(cmd_title, stderr=subprocess.DEVNULL).decode()
                # Extrahiert den eigentlichen Titel
                res = out_title.split('variant       string "')[1].split('"')[0]

                if res: return res.lower()
            except Exception:
                pass
            return "wayland-unknown"  # Verhindert den Absturz durch xdotool!

        # is_wayland = os.environ.get('XDG_SESSION_TYPE') == 'wayland' or os.environ.get('WAYLAND_DISPLAY')

        # if is_wayland:
        #     try:
        #         # KDE Plasma 6
        #         if shutil.which("qdbus"):
        #             # Holt Pfad wie /Windows/W1
        #             win_path = subprocess.check_output(["qdbus", "org.kde.KWin", "/KWin", "activeWindow"],
        #                                                stderr=subprocess.DEVNULL).decode().strip()
        #             if win_path:
        #                 # Holt Titel
        #                 res = subprocess.check_output(["qdbus", "org.kde.KWin", win_path, "caption"],
        #                                               stderr=subprocess.DEVNULL).decode().strip()
        #                 if res: return res.lower()
        #     except:
        #         pass
        #     return None  # Verhindert den Absturz im X11-Teil (xdotool)

        # --- LINUX X11 ---
        if sys.platform.startswith('linux'):
            env = get_linux_x11_env()

            # Versuch 1: xdotool
            res = None
            if shutil.which("xdotool"):
                try:
                    res = subprocess.check_output(
                        ["xdotool", "getwindowfocus", "getwindowname"],
                        stderr=subprocess.DEVNULL, env=env
                    )
                    # return res.decode("utf-8", errors='ignore').strip().lower()
                    return res.decode('cp1252', errors='replace').strip().lower()
                except Exception as e:
                    print(f'145 {e}')
                    pass

            # Versuch 2: xprop
            if shutil.which("xprop"):
                try:
                    active_id = subprocess.check_output(
                        ["xprop", "-root", "_NET_ACTIVE_WINDOW"],
                        stderr=subprocess.DEVNULL, env=env
                    ).decode().split()[-1]

                    res = subprocess.check_output(
                        ["xprop", "-id", active_id, "WM_NAME"],
                        stderr=subprocess.DEVNULL, env=env
                    )
                    return res.decode("utf-8").split('=', 1)[-1].strip().strip('"').lower()
                except Exception as e:
                    print(f'201 {e}')
                    pass

            # 3. Wenn es fehlschlägt: Cache könnte veraltet sein! # neue 17.1.'26 01:21 Sat Passiert vielleicht beim ein und ausloggen (nicht beim reboot)
            if res is None:
                # Wir löschen den globalen Cache und die Datei
                global _X11_ENV_CACHE
                _X11_ENV_CACHE = None
                if X11_CACHE_FILE.exists():
                    try: os.remove(X11_CACHE_FILE)
                    except Exception as e:
                        print(f'111 {e}')
                        pass

            # Wir holen das Environment FRISCH (neuer Scan)
            env = get_linux_x11_env()
            # Zweiter Versuch
            # res = try_get_title(env)

        # return res

    except Exception as e:
        # scripts/py/func/get_active_window_title.py:206
        print(f'178 {e}')
        pass

    return None


# --- CLIPBOARD FUNKTIONEN ---

def get_clipboard_text_linux():
    if not sys.platform.startswith('linux'): return ""
    env = get_linux_x11_env()

    if shutil.which("xclip"):
        try:
            return subprocess.check_output(["xclip", "-selection", "clipboard", "-o"], stderr=subprocess.DEVNULL, env=env).decode("utf-8")
        except Exception as e:
            print(f'194 {e}')
        pass

    elif shutil.which("xsel"):
        try:
            return subprocess.check_output(["xsel", "-b", "-o"], stderr=subprocess.DEVNULL, env=env).decode("utf-8")
        except Exception as e:
            print(f'201 {e}')
            pass

    return ""

def set_clipboard_text_linux(text):
    if not sys.platform.startswith('linux'): return
    env = get_linux_x11_env()

    if shutil.which("xclip"):
        try:
            p = subprocess.Popen(["xclip", "-selection", "clipboard", "-i"], stdin=subprocess.PIPE, env=env)
            p.communicate(input=text.encode('utf-8'))
        except Exception as e:
            print(f'215 {e}')
            pass
    elif shutil.which("xsel"):
        try:
            p = subprocess.Popen(["xsel", "-b", "-i"], stdin=subprocess.PIPE, env=env)
            p.communicate(input=text.encode('utf-8'))
        except Exception as e:
            print(f'220 {e}')
            pass
