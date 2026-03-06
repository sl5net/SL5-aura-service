# scripts/py/func/checks/trigger_aura_maintenance.py
import threading
import random
import time
import shutil

from pathlib import Path

import subprocess
import sys

# scripts/py/func/checks/trigger_aura_maintenance.py:12
REPO_ROOT = Path(__file__).resolve().parents[4]
TEST_ROOTS = [
    Path("config/maps/plugins/git/de-DE/self_test_zip_tmp"),
    Path("config/maps/plugins/self_test_zip_tmp"),
    Path("config/maps/self_test_zip_tmp"),
]
EXPECTED_ZIP_NAME = "locked_folder.zip"
LAST_CHECK_FILE = Path("/tmp/sl5_aura/last_smoke_zip_check")

# radio_script = REPO_ROOT / "config/maps/plugins/z_fallback_llm/de-DE/radio_deep_dive.py"
radio_script = REPO_ROOT / "config/maps/plugins/z_fallback_llm/de-DE/radio_deep_dive.py"
translator_script = REPO_ROOT / "tools" / "translate_md.py"


MAINTENANCE_TIMER = None

def trigger_aura_maintenance(logger):
    # from scripts.py.func.audio_manager import speak_fallback
    """Triggered by Aura. Starts maintenance tasks after 4s of silence."""
    global MAINTENANCE_TIMER
    if MAINTENANCE_TIMER:
        MAINTENANCE_TIMER.cancel()
    logger.info("Maintenance: Timer scheduled (4s silence)...")
    # speak_fallback("Maintenance: Timer scheduled (4s silence)...", 'de-DE')

    MAINTENANCE_TIMER = threading.Timer(4.0, _execute_maintenance_tasks, args=[logger])
    MAINTENANCE_TIMER.daemon = True
    MAINTENANCE_TIMER.start()


def _execute_maintenance_tasks(logger):
    from scripts.py.func.audio_manager import speak_inclusive_fallback
    logger.info("!!! Maintenance Task Started !!!")

    """Zentraler Manager für Hintergrund-Aufgaben."""
    try:
        # 1. Throttling: Nur alle 10 Minuten einen Test machen
        now = time.time()
        if LAST_CHECK_FILE.exists():
            try:
                last_time = float(LAST_CHECK_FILE.read_text())
                if now - last_time < 60 * 2:
                    return
            except Exception:
                pass

        # 2. RADIO-AURA CACHE GENERIERUNG
        logger.info(f"Maintenance: Checking Path: {radio_script}")

        if radio_script.exists():
            # Wir nutzen subprocess, um die venv-Umgebung und das if-main-Handling sauber zu trennen

            result = subprocess.run([sys.executable, str(radio_script)], capture_output=True, text=True, check=False)

            output = result.stdout.strip()
            logger.info(f"Radio Generator Output: {output}")

            if "All documents are up to date" in output:
                logger.info("Maintenance: Radio Cache is already current.")
                # speak_fallback("Maintenance: Radio Cache is already current.", 'de-DE')

            else:
                logger.info("Maintenance: Radio-Aura Cache wurde aktualisiert.")
                # speak_fallback("Maintenance: Radio-Aura Cache wurde aktualisiert", 'de-DE')

            # subprocess.run([sys.executable, str(radio_script)], check=False)
            logger.info("Maintenance: Radio-Aura Cache fertig.")
            # speak_fallback("Maintenance: Radio-Aura Cache fertig.", 'de-DE')

        else:
            logger.error(f"Maintenance: PATH NOT FOUND: {radio_script}")

        # 2.b MARKDOWN TRANSLATOR (i18n Sync)
        if translator_script.exists():
            logger.info(f"Maintenance: Starting Markdown Translator: {translator_script}")

            # Startet den Translator. Da dieser bereits existierende Dateien überspringt,
            # ist der Aufruf effizient.
            res_trans = subprocess.run([sys.executable, str(translator_script)], capture_output=True, text=True,
                                       check=False)

            if res_trans.stdout:
                logger.info(f"Translator Output: {res_trans.stdout.strip()}")
            if res_trans.stderr:
                logger.warning(f"Translator Warnings: {res_trans.stderr.strip()}")

            logger.info("Maintenance: Markdown Translation Sync fertig.")
        else:
            logger.error(f"Maintenance: TRANSLATOR PATH NOT FOUND: {translator_script}")


        # 3. SMOKE-ZIP TEST
        root = random.choice(TEST_ROOTS)
        folder_nickname = root.parent.name if root.parent.name != "self_test_zip_tmp" else "Root"
        logger.info(f"Maintenance: Starting Smoke-Zip Test for: {root}")

        if _setup_scenario(root, logger):
            # 4. Warten und Prüfen (Aura zippt im Vorbeigehen)
            success = False
            start_wait = time.time()
            expected_zip = root / EXPECTED_ZIP_NAME

            # Wir geben Aura 30 Sekunden Zeit
            while time.time() - start_wait < 30:
                if expected_zip.exists():
                    success = True
                    break
                time.sleep(1.0)

            if success:
                msg = f"Auto-Zip erfolgreich für {folder_nickname}"
                logger.info(f"Auto-Zip: ✅ Smoke Test ERFOLGREICH für {root}")
                # speak_fallback(msg, 'de-DE')
            else:
                msg = 'Smoke Test Timeout '
                logger.warning(f"Auto-Zip: ❌ {msg} für {root}")
                msg = f"Auto-Zip {msg} in {folder_nickname}"

                # speak_fallback(msg, 'de-DE')

            # 5. Aufräumen
            _cleanup(root, logger)
        else:
            logger.error(f"Auto-Zip: Setup fehlgeschlagen für {root}")
            speak_inclusive_fallback("Fehler beim Setup des Zip Tests", 'de-DE')

    except Exception as e:
        logger.error(f"Auto-Zip: 💥 Fehler im Smoke Test: {e}")
        speak_inclusive_fallback("Kritischer Fehler im Auto-Zip Test", 'de-DE')


def _setup_scenario(root, logger):
    """Erstellt eine realistische Map-Struktur für den Test."""
    try:
        # Sicherheitscheck: Parent muss existieren (sonst ist Aura nicht korrekt installiert)
        if not root.parent.exists():
            logger.error(f"Auto-Zip: Parent Pfad existiert nicht: {root.parent}")
            return False

        # 1. Container erstellen
        root.mkdir(parents=True, exist_ok=True)
        (root / "__init__.py").write_text("# Container Init")

        # 2. Den Ziel-Ordner erstellen (der gezippt werden soll)
        locked = root / "_locked_folder"
        locked.mkdir(parents=True, exist_ok=True)

        # 3. Notwendige Dateien für die Erkennung durch Aura
        (locked / "__init__.py").write_text("# module init\n")

        # Eine nicht-leere .py Datei (wichtig für den Reloader/Packer)
        content = "def on_reload():\n    pass\n\n# Auto-Generated Test File\n"
        (locked / "FUZZY_MAP_pre.py").write_text(content)

        # Sprachebene für tiefes Scannen
        de_dir = locked / "de-DE"
        de_dir.mkdir(parents=True, exist_ok=True)
        (de_dir / "__init__.py").write_text("# lang init")

        return True
    except Exception as e:
        logger.error(f"Auto-Zip: Scenario Setup failed: {e}")
        return False


def _cleanup(root, logger):
    """Löscht den Test-Container nach Abschluss."""
    if root.exists():
        try:
            shutil.rmtree(root)
            logger.info(f"Auto-Zip: Cleaned up {root}")
        except Exception as e:
            logger.error(f"Maintenance Fehler: {e}")
