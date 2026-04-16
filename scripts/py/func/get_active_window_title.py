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


def get_active_window_kde():
    # This command directly asks KWin for the title of the active window
    # cmd = "qdbus6 org.kde.KWin /KWin org.kde.KWin.activeWindow"
    # If this only provides an ID, this one is better for the text:
    cmd_title = "qdbus6 org.kde.KWin /KWin org.kde.KWin.supportInformation"

    try:
        res = subprocess.check_output(cmd_title, shell=True, text=True)
        for line in res.splitlines():
            if "Active window title:" in line:
                return line.split(":")[1].strip()
    except Exception as e:
        print(f'29: {e}')
        return "NO_WINDOW_TITLE_30"

def get_active_window_title_atspi_fallback():
    """
    Retrieves the title of the currently active window using the
    AT-SPI (Accessibility) Bus. This is the most reliable method for
    Linux / Plasma 6 (Wayland).

    Prerequisites for Linux:
    1. System packages: sudo pacman -S orca at-spi2-core
    2. Environment: export QT_ACCESSIBILITY=1
    3. KDE Settings: Enable Screen Reader in Accessibility settings.

    something else maybe important if you have problems:
    python -m venv .venv --system-site-packages

    source .venv/bin/activate.fish

    don't forget:
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


    sudo pacman -S orca at-spi2-core. Das ist korrekt, aber unter Arch/CachyOS ist es oft zwingend erforderlich, das Paket python-gobject systemweit zu haben, damit die gi-Bindings (GObject Introspection) überhaupt mit den System-Bibliotheken kommunizieren können.

    Ergänze python-gobject in der pacman Zeile. Ohne dieses Paket schlägt import gi in manchen Venvs fehl, wenn diese mit --system-site-packages erstellt wurden.

    kwriteconfig6 --file kaccessrc --group ScreenReader --key Enabled true

    echo "export QT_ACCESSIBILITY=1" >> ~/.bashrc
    echo "set -gx QT_ACCESSIBILITY 1" >> ~/.config/fish/config.fish


    Systemeinstellungen > Eingabehilfen > Eingabehilfen


    orca -s
    > disable language

    Test:
    dbus-send --print-reply --dest=org.a11y.Bus /org/a11y/bus org.a11y.Bus.GetAddress


    """
    try:
        try:
            import gi
        except ImportError:
            if os.environ.get("XDG_SESSION_TYPE") == "wayland" or os.environ.get("WAYLAND_DISPLAY"):
                print("pip install PyGObject ")
                print("pip install PyGObject ")
                raise RuntimeError(
                    "PyGObject is required on Wayland sessions (e.g. to get actual Window-Title (s, 26.2.'26). Install it with: "
                    "pip install PyGObject"
                )

        gi.require_version('Atspi', '2.0')
        from gi.repository import Atspi
    except (ImportError, ValueError) as e:
        print(f"Required library 'gi' (PyGObject) or Atspi 2.0 not found: {e}")
        return "Error: AT-SPI dependencies missing"

    # Initialize the Atspi Registry (0 = success)
    # if Atspi.init() != 0:
    #     return f"89: Error: Could not initialize Atspi {Atspi}"


    # --- SCHRITT 2: Einmalige Initialisierung (hasattr Trick) ---
    # We check whether we have already attached a “note” to this function.
    # 'hasattr' checks: "Do I have the variable 'initialized' yet?"
    if not hasattr(get_active_window_title_atspi_fallback, "initialized"):
        if Atspi.init() == 0:
            # We stick the note "initialized = True" to the function
            get_active_window_title_atspi_fallback.initialized = True
        else:
            get_active_window_title_atspi_fallback.initialized = False
            return None





    # Get the root desktop object
    desktop = Atspi.get_desktop(0)
    if not desktop:
        return "Error: Could not access desktop via AT-SPI"

    # Iterate through all applications on the Accessibility Bus
    for i in range(desktop.get_child_count()):
        app = desktop.get_child_at_index(i)
        if not app:
            continue

        # Each app can have multiple windows
        for j in range(app.get_child_count()):
            window = app.get_child_at_index(j)
            if not window:
                continue

            # Check the states of the window
            try:
                state_set = window.get_state_set()
                states = state_set.get_states()

                # We are looking for the window that is either ACTIVE or FOCUSED
                # Atspi.StateType.ACTIVE (2) or Atspi.StateType.FOCUSED (4)
                if Atspi.StateType.ACTIVE in states or Atspi.StateType.FOCUSED in states:
                    return f"App: {app.get_name()} | Title: {window.get_name()}"
            except Exception:
                continue

    return "No active window found"



# def get_active_window_plasma6():
#     script = "print(workspace.activeWindow.caption);"
#
#     load_cmd = [
#         "dbus-send", "--print-reply", "--dest=org.kde.KWin",
#         "/Scripting", "org.kde.kwin.Scripting.loadScript",
#         f"string:{script}"
#     ]
#
#     try:
#         result = subprocess.run(load_cmd, capture_output=True, text=True, check=True)
#         script_path = result.stdout.split('object path "')[1].split('"')[0]
#
#         start_time = time.time()
#         subprocess.run(["dbus-send", "--dest=org.kde.KWin", script_path, "org.kde.kwin.Script.run"], check=True)
#
#         log_cmd = ["journalctl", "_COMM=kwin_wayland", "-o", "cat", f"--since=@{int(start_time)}"]
#         logs = subprocess.run(log_cmd, capture_output=True, text=True).stdout
#
#         subprocess.run(["dbus-send", "--dest=org.kde.KWin", script_path, "org.kde.kwin.Script.stop"])
#
#         for line in logs.strip().split('\n'):
#             if line.startswith("js:"):
#                 return line.replace("js: ", "").strip()
#     except Exception as e:
#         return f"Error: {e}"


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
            # Limit to a maximum of 50 attempts so that we don't get stuck in /proc forever
            pids = [p for p in os.listdir('/proc') if p.isdigit()]
            # Sortieren, neuere PIDs zuerst (wahrscheinlicher GUI apps)
            pids.sort(key=lambda x: int(x), reverse=True)

            for pid in pids[:100]: # Nur die neuesten 100 Prozesse scannen
                try:
                    # Timeout simulieren durch schnelles Lesen (non-blocking ist in Python schwer bei files)
                    # We just read and catch every mistake
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
                # THEN restrict rights (only owner is allowed to read/write)
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


def get_active_window_title_kde_wayland_qdbus():
    """
    Versucht den aktiven Fenstertitel direkt über KDE KWin (DBus) abzufragen.
    Dies ist der zuverlässigste Weg unter Plasma 6 + Wayland.
    """
    try:
        # qdbus6 is the default command under Plasma 6
        # We query the support information which contains the current status
        result = subprocess.run(
            ["qdbus6", "org.kde.KWin", "/KWin", "org.kde.KWin.supportInformation"],
            capture_output=True, text=True, timeout=1
        )

        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "Active window title:" in line:
                    title = line.replace("Active window title:", "").strip()
                    if title:
                        return f"🔵(KWin) {title}"
    except (subprocess.SubprocessError, FileNotFoundError):
        # If qdbus6 is not installed or fails
        pass
    return None


def get_active_window_title_kde_native():
    """
    Fragt KWin (Plasma 6) direkt über qdbus6 ab.
    Das ist unter Wayland der stabilste Weg.
    """
    try:
        # We ask KWin for the support information
        # timeout=0.5 ensures that the script does not hang
        result = subprocess.run(
            ["qdbus6", "org.kde.KWin", "/KWin", "org.kde.KWin.supportInformation"],
            capture_output=True,
            text=True,
            timeout=0.5
        )

        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "Active window title:" in line:
                    title = line.replace("Active window title:", "").strip()
                    if title:
                        return f"🔵App: {title}"  # Wir geben nur den Titel zurück
    except Exception:
        pass  # Wenn qdbus6 nicht da ist, gehen wir zum Fallback
    return None


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
            if length == 0: return "NO_WINDOW_TITLE_374"
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            return buff.value.lower()


        # --- LINUX WAYLAND ---

        # --- LINUX WAYLAND (KDE Fix) ---
        # return get_active_window_plasma6()



        if os.environ.get('XDG_SESSION_TYPE') == 'wayland' or os.environ.get('WAYLAND_DISPLAY'):

            # print(f'🔵🔵🔵{get_active_window_title_atspi()}🔵🔵🔵')
            # exit(1)

            # 1. Priorität: Plasma 6 / Wayland (qdbus6)
            title = get_active_window_title_kde_native()

            # Versuch: KDE Native (Wayland optimiert)
            # 2nd priority: If the first way fails, take Atspi (but quietly)
            if not title:
                title = get_active_window_title_kde_wayland_qdbus()

            if not title:
                title = get_active_window_kde()

            # 2nd attempt: If KDE didn't deliver anything or there was an error, use Atspi
            if title is None or "Error" in title:
                title = get_active_window_title_atspi_fallback()

            return title
            

            # return get_active_window_title_atspi()

            # try:
            # 1. Get active window path via dbus-send (standard tool)
            #     cmd_id = ["dbus-send", "--session", "--print-reply", "--dest=org.kde.KWin", "/KWin",
            #               "org.kde.KWin.activeWindow"]
            #     out_id = subprocess.check_output(cmd_id, stderr=subprocess.DEVNULL).decode()
            #     # Extrahiert den Pfad (z.B. /Windows/W1)
            #     win_path = out_id.split('objpath "')[1].split('"')[0]
            #
            # 2. Get the title (caption) for this path
            #     cmd_title = ["dbus-send", "--session", "--print-reply", "--dest=org.kde.KWin", win_path,
            #                  "org.freedesktop.DBus.Properties.Get", "string:org.kde.KWin.Window", "string:caption"]
            #     out_title = subprocess.check_output(cmd_title, stderr=subprocess.DEVNULL).decode()
            #     # Extrahiert den eigentlichen Titel
            #     res = out_title.split('variant       string "')[1].split('"')[0]
            #
            #     if res: return res.lower()
            # except Exception:
            #     pass
            # return "wayland-unknown"  # Verhindert den Absturz durch xdotool!

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
        # scripts/py/func/get_active_window_title.py:345
        if sys.platform.startswith('linux'):
            env = get_linux_x11_env()

            # Versuch 1: xdotool
            res = None
            if shutil.which("xdotool"):
                try:
                    res = subprocess.check_output(
                        ["xdotool", "getwindowfocus", "getwindowname"],
                        stderr=subprocess.DEVNULL, env=env, timeout=1.5
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
                        stderr=subprocess.DEVNULL, env=env, timeout=1.5
                    ).decode().split()[-1]

                    res = subprocess.check_output(
                        ["xprop", "-id", active_id, "WM_NAME"],
                        stderr=subprocess.DEVNULL, env=env, timeout=1.5
                    )
                    return res.decode("utf-8").split('=', 1)[-1].strip().strip('"').lower()
                except Exception as e:
                    print(f'201 {e}')
                    pass

            # 3. If it fails: Cache might be out of date! # new 1/17/26 01:21 Sat Maybe happens when logging in and out (not when rebooting)
            if res is None:
                # We delete the global cache and file
                global _X11_ENV_CACHE
                _X11_ENV_CACHE = None
                if X11_CACHE_FILE.exists():
                    try: os.remove(X11_CACHE_FILE)
                    except Exception as e:
                        print(f'111 {e}')
                        pass

            # We get the environment FRESH (new scan)
            env = get_linux_x11_env()
            # Zweiter Versuch
            # res = try_get_title(env)

        # return res

    except Exception as e:
        # scripts/py/func/get_active_window_title.py:206
        print(f'178 {e}')
        pass

    return "NO_WINDOW_TITLE_511"


# --- CLIPBOARD FUNKTIONEN ---

def get_clipboard_text_linux():
    if not sys.platform.startswith('linux'): return ""
    env = get_linux_x11_env()

    if shutil.which("xclip"):
        try:
            return subprocess.check_output(["xclip", "-selection", "clipboard", "-o"], stderr=subprocess.DEVNULL, env=env, timeout=1.5).decode("utf-8")
        except Exception as e:
            print(f'194 {e}')
        pass

    elif shutil.which("xsel"):
        try:
            return subprocess.check_output(["xsel", "-b", "-o"], stderr=subprocess.DEVNULL, env=env, timeout=1.5).decode("utf-8")
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
