# scripts/py/welcome_wizard/de-DE/start.py
import subprocess
import platform

def run(project_root):
    d = project_root / "scripts" / "search_rules"
    search_script = d / "search_rules.bat" if platform.system() == "Windows" else d / "search_rules.sh"
    koan_dir = project_root / "config" / "maps" / "koans_deutsch"

    if not search_script.exists():
        return

    welcome_msg_20260402 = ( # noqa: F841
        "=== WILLKOMMEN BEI AURA ===\\n\\n"
        "Ich habe dir die interaktiven Uebungen (Koans) geoeffnet.\\n"
        "Suche dir eine Aufgabe aus und druecke ENTER um sie in Kate zu oeffnen.\\n"
    )

    welcome_msg = (
        "=== WILLKOMMEN BEI AURA 🔭 ===\\n\\n"
        "Aura ist dein Teleskop fuer den PC: Steuerung aus der Ferne!\\n\\n"
        "TIPP: Sag 'Teleskop' waehrend der Aufnahme, um die\\n"
        "Pausen-Funktion (SUSPENDED) ein- oder auszuschalten.\\n\\n"
        "Ich oeffne dir jetzt die Uebungen (Koans)..."
    )


    if platform.system() == "Windows":
        # Wir übergeben das Koan-Verzeichnis an die .bat
        # Windows handles background processes differently, usually no fix needed
        subprocess.Popen(['cmd', '/c', 'start', str(search_script), str(koan_dir)], start_new_session=True)

    else:
        import os
        env = os.environ.copy()
        env.setdefault("DISPLAY", ":0")
        env.setdefault("DBUS_SESSION_BUS_ADDRESS", "unix:path=/run/user/1000/bus")

        from scripts.py.func.config.dynamic_settings import DynamicSettings
        settings = DynamicSettings()

        sleep_sec = 0
        if settings.DEV_MODE:
            sleep_sec = 5

        cmd = [
            'konsole', '-e', 'bash', '-c',
            f'echo -e "{welcome_msg}"; sleep 2; bash {search_script} {koan_dir}; sleep {sleep_sec}'
        ]
        subprocess.Popen(cmd, start_new_session=True, env=env)
