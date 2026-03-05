# scripts/py/func/checks/run_auto_zip_random_quick_check.py
import threading
import random
import time
import shutil

from pathlib import Path

from scripts.py.func.audio_manager import speak_fallback

# --- KONFIGURATION (unabhängig) ---
TEST_ROOTS = [
    Path("config/maps/plugins/git/de-DE/self_test_zip_tmp"),
    Path("config/maps/plugins/self_test_zip_tmp"),
    Path("config/maps/self_test_zip_tmp"),
]
EXPECTED_ZIP_NAME = "locked_folder.zip"
LAST_CHECK_FILE = Path("/tmp/sl5_aura/last_smoke_zip_check")
ZIP_TEST_TIMER = None


def trigger_background_zip_check(logger):
    """Wird von Aura aufgerufen. Startet den Test nach 4 Sek. Stille."""
    global ZIP_TEST_TIMER
    if ZIP_TEST_TIMER:
        ZIP_TEST_TIMER.cancel()

    # Timer für 4 Sekunden Stille
    ZIP_TEST_TIMER = threading.Timer(4.0, _execute_smoke_test, args=[logger])
    ZIP_TEST_TIMER.daemon = True
    ZIP_TEST_TIMER.start()

    # Optionale Ansage, dass der Test in Warteschlange ist (kann man auch weglassen)
    # speak_fallback("Zip Test geplant", 'de-DE')


def _execute_smoke_test(logger):
    """Die eigentliche Test-Logik (läuft im Hintergrund-Thread)."""
    try:
        # 1. Throttling: Nur alle 10 Minuten einen Test machen
        now = time.time()
        if LAST_CHECK_FILE.exists():
            try:
                last_time = float(LAST_CHECK_FILE.read_text())
                if now - last_time < 600:  # 10 Min
                    return
            except Exception:
                pass

        LAST_CHECK_FILE.parent.mkdir(parents=True, exist_ok=True)
        LAST_CHECK_FILE.write_text(str(now))

        # 2. Zufälligen Pfad auswählen
        root = random.choice(TEST_ROOTS)
        folder_nickname = root.parent.name if root.parent.name != "self_test_zip_tmp" else "Root"

        logger.info(f"Auto-Zip: 🎲 Random Smoke Test startet für: {root}")
        speak_fallback(f"Auto-Zip Test startet in Ordner {folder_nickname}", 'de-DE')

        # 3. Test-Ordner erstellen
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
                speak_fallback(msg, 'de-DE')
            else:
                msg = f"Auto-Zip Zeitüberschreitung in {folder_nickname}"
                logger.warning(f"Auto-Zip: ❌ Smoke Test Timeout für {root}")
                speak_fallback(msg, 'de-DE')

            # 5. Aufräumen
            _cleanup(root, logger)
        else:
            logger.error(f"Auto-Zip: Setup fehlgeschlagen für {root}")
            speak_fallback("Fehler beim Setup des Zip Tests", 'de-DE')

    except Exception as e:
        logger.error(f"Auto-Zip: 💥 Fehler im Smoke Test: {e}")
        speak_fallback("Kritischer Fehler im Auto-Zip Test", 'de-DE')


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
            logger.error(f"Auto-Zip: Cleanup failed for {root}: {e}")
