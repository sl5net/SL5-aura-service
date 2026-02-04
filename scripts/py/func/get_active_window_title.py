# scripts/py/func/get_active_window_title.py
import sys
import os
import subprocess
import shutil
import json
import tempfile
from pathlib import Path
# --- GLOBALER CACHE (Memory) ---
_X11_ENV_CACHE = None

# --- DATEI CACHE (Disk - überlebt Reloads) ---
X11_CACHE_FILE = Path(tempfile.gettempdir()) / "sl5_aura" / "sl5_aura_x11_env.json"

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

        # --- LINUX ---
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
