import sys
import time
import shutil
import threading
from pathlib import Path

from scripts.py.func.audio_manager import speak_fallback


import os
import platform
# scripts/py/func/checks/auto_zip_startup_test.py
readme = '' # noqa: F841
readme += """
für löschen siehe:
tools/del_all_self_test_zip_tmp_folders.py
"""
try:
    from scripts.py.func import map_reloader
except ImportError:
    map_reloader = None

# Config
TEST_DIR_NAME = "self_test_zip_tmp"
TEST_DIR_Zip_NAME = f"{TEST_DIR_NAME}.zip"

EXPECTED_ZIP_NAME = "locked_folder.zip"

root = Path("config/maps/plugins")
# TEST_ROOTS = [p / TEST_DIR_NAME for p in sorted(root.iterdir()) if p.is_dir()]


import random

# Config oben in der Datei
SMOKE_TEST_PROBABILITY = 0.1  # 40% Chance bei jedem Start


def iter_non_hidden_dirs(start: Path):
    for p in start.iterdir():
        if (not p.name.startswith('.')
                and not p.name.startswith('_')
                and not p.name.startswith('s')
                and p.is_dir()):
            yield p
            yield from iter_non_hidden_dirs(p)

# Alle gefundenen Verzeichnisse nehmen und TEST_DIR_NAME anhängen

# Achtung! Es werden bei jdem Durhclauf wieder viel mehr!
# TEST_ROOTS = [ (d / TEST_DIR_NAME).resolve() for d in iter_non_hidden_dirs(root) ]



# Optional: nur existierende Pfade behalten
# TEST_ROOTS = [p for p in TEST_ROOTS if p.exists()]

# print(TEST_ROOTS)

if True:
    TEST_ROOTS = [
        # following are true at the moment 17.2.'26 16:38 Tue
        # Path("config/maps/plugins/wannweil/de-DE") / TEST_DIR_NAME,
        # Path("config/maps/_privat") / TEST_DIR_NAME,
        # Path("config/maps/_privat/_subdira") / TEST_DIR_NAME,

        # following are not testest at the moment 17.2.'26 16:38 Tue

        Path("config/maps/plugins/git/de-DE") / TEST_DIR_NAME,
        # Path("config/maps/plugins/git") / TEST_DIR_NAME,
        Path("config/maps/plugins") / TEST_DIR_NAME,
        Path("config/maps") / TEST_DIR_NAME,

        # Path("config/maps/plugins/web-radio-funk/de-DE") / TEST_DIR_NAME,
        # Path("config/maps/plugins/web-radio-funk") / TEST_DIR_NAME,
        #
        # Path("config/maps/plugins/sandbox/de-DE") / TEST_DIR_NAME,
        # Path("config/maps/plugins/sandbox") / TEST_DIR_NAME,
        #
        # Path("config/maps/plugins/wannweil") / TEST_DIR_NAME,

        # Path("config/maps") / TEST_DIR_NAME,

    ]
# Alle direkte Unterverzeichnisse nehmen und jeweils TEST_DIR_NAME anhängen

MAX_WAIT_SECONDS = 120  # Increased time for 6 folders!

if platform.system() == "Windows":
    TMP_DIR = Path("C:/tmp")
    NOTIFY_SEND_PATH = None
else:
    TMP_DIR = Path("/tmp")
core_logic_self_test_is_running_FILE = TMP_DIR / "sl5_aura" / "core_logic_self_test_FILE_is_running"

# easier to debug when empties it at the start
# aura_log = Path('log/aura_engine.log')
# aura_log.unlink(missing_ok=True) ## seems problematic

SUCCESS = None

creation_time_first_zip = 0
creation_time_last_zip = 0


def timeout_auto_zip(waited_sec, MAX_WAIT_SECONDS, logger):
    if waited_sec > MAX_WAIT_SECONDS:
        logger.error(f"Auto-Zip: Timeout! ⏰ {waited_sec:.1f}s > {MAX_WAIT_SECONDS}s")

        # DIAGNOSE
        flag_exists = core_logic_self_test_is_running_FILE.exists()
        logger.error(f"Auto-Zip: 🔍 Flag existiert noch: {flag_exists}")
        logger.error(f"Auto-Zip: 🔍 Flag-Pfad: {core_logic_self_test_is_running_FILE}")

        missing, found = _get_missing_zips(logger, silent=False)
        logger.error(f"Auto-Zip: 🔍 Fehlende Zips ({len(missing)}): {missing}")
        logger.error(f"Auto-Zip: 🔍 Gefundene Zips ({len(found)}): {found}")

        for root in TEST_ROOTS:
            logger.error(f"Auto-Zip: 🔍 Root exists={root.exists()}: {root}")

        speak_fallback(f"Auto-Zip Timeout nach {int(waited_sec)} Sekunden", 'de-DE')
        global SUCCESS
        SUCCESS = False
        return True
    return False

# def timeout_auto_zip(waited_sec, MAX_WAIT_SECONDS, logger):
#     if waited_sec > MAX_WAIT_SECONDS:
#         logger.error(f"Auto-Zip: Timeout! ⏰ {waited_sec}sec > {int(MAX_WAIT_SECONDS)}sec")
#         speak_fallback(f"Auto-Zip: Timeout! Zeit abgelaufen {int(waited_sec)}sec > {int(MAX_WAIT_SECONDS)}sec",
#                        'de-DE')
#         global SUCCESS
#         SUCCESS = False
#         return True
#     return False


def run_auto_zip_sanity_check(logger):
    start_time = time.time()

    speak_fallback(f"Auto-Zip: ⏰ start 123", 'de-DE')
    logger.info("Auto-Zip: 126: 🧪 🚀 START: Sanity Check - multiple roots")

    def _test_logic():
        print("Auto-Zip: _test_logic LÄUFT", flush=True)

        # 1. SETUP - Testordner erstellen
        try:
            _create_test_scenarios(logger)
        except Exception as e:
            logger.error(f"Auto-Zip: 💀 Setup Error: {e}")
            return  # kein sys.exit() im Thread!

        # sleep(30) ENTFERNEN - wir warten jetzt gezielt auf das Flag

        # 2. POLLING LOOP
        core_logic_self_test_was_running = False
        core_logic_self_test_not_running_anymore = False
        global SUCCESS
        waited_sec_int_old = 0

        logger.info(f"Auto-Zip: 162: Warte auf Flag-File: {core_logic_self_test_is_running_FILE}")

        while True:
            waited_sec = time.time() - start_time

            # Timeout immer zuerst prüfen
            if timeout_auto_zip(waited_sec, MAX_WAIT_SECONDS, logger):
                break

            # Schnellcheck: Zips schon alle da? (Service war sehr schnell)
            missing_list, found_zips = _get_missing_zips(logger)
            if not missing_list and found_zips:
                logger.info("Auto-Zip: ✨ Alle Zips schon da - Service war sehr schnell!")
                SUCCESS = True
                break

            # Phase 1: Warten bis Flag EXISTS (= erster Durchlauf fertig, Modelle geladen)
            if not core_logic_self_test_was_running:
                if core_logic_self_test_is_running_FILE.exists():
                    core_logic_self_test_was_running = True
                    logger.info(f"Auto-Zip: ✅ Flag gesetzt - Self-Tests laufen ({waited_sec:.1f}s)")
                    speak_fallback("Auto-Zip: Self-Test läuft", "de-DE")
                else:
                    if int(waited_sec / 5) > int(waited_sec_int_old / 5):
                        logger.info(f"Auto-Zip: 187 ⏳ Warte auf Flag... {int(waited_sec)}s / {MAX_WAIT_SECONDS}s")
                    waited_sec_int_old = waited_sec
                    time.sleep(0.5)
                    continue

            # Phase 2: Warten bis Flag WEG (= alle Self-Tests fertig)
            # if not core_logic_self_test_not_running_anymore:
            #     if not core_logic_self_test_is_running_FILE.exists():
            #         core_logic_self_test_not_running_anymore = True
            #         logger.info(f"Auto-Zip: ✅ Flag weg - Self-Tests fertig ({waited_sec:.1f}s)")
            #         speak_fallback("Auto-Zip: Self-Tests fertig, prüfe Zips", "de-DE")
            #     else:
            #         if int(waited_sec / 5) > int(waited_sec_int_old / 5):
            #             logger.info(f"Auto-Zip: 200: ⏳ Warte auf Flag-Ende... {int(waited_sec)}s")
            #         waited_sec_int_old = waited_sec
            #         time.sleep(0.5)
            #         continue

            # Phase 3: Zips prüfen
            missing_list, _ = _get_missing_zips(logger)
            if not missing_list:
                SUCCESS = True
                break

            logger.debug(f"Auto-Zip: ⏳ Noch {len(missing_list)} Zips fehlend... {waited_sec:.1f}s")
            time.sleep(0.1)

    t = threading.Thread(target=_test_logic, daemon=False)
    t.start()
    t.join()  # ← blockiert bis _test_logic fertig ist
    logger.info("Auto-Zip: 🧵 Test Thread fertig.")

    # 4. RESULT

    print("Auto-Zip: Thread fertig oder Timeout", flush=True)

# Oder noch einfacher — ohne Thread, da du sowieso blockieren willst:
# def run_auto_zip_sanity_check(logger):
#     start_time = time.time()
#     speak_fallback("Auto-Zip: ⏰ start", 'de-DE')
#     logger.info("Auto-Zip: 🚀 START")
#     _test_logic_direct(logger, start_time)  # ← direkt aufrufen, kein Thread



    # t = threading.Thread(target=_test_logic, daemon=True)
    # t.start()
    # logger.info("Auto-Zip: 🧵 Test Thread started.")

    # else:
    #     # wenn map_reloader.auto_reload_modified_maps ist nicht-blockierend, dann:
    #     reload_event = threading.Event()
    #
    #     def reload_and_signal(logger):
    #         map_reloader.auto_reload_modified_maps(logger, True)
    #         reload_event.set()
    #
    #     t = threading.Thread(target=_test_logic(), daemon=True)
    #     t.start()
    #     # warte auf reload_event mit Timeout bevor du Polling beginnst
    #     reload_event.wait(timeout=10)
    #     logger.info("🧵 Auto-Zipsdfg Test Thread started.")
    # time.sleep(1)
    # waited_sec = time.time() - start_time


def _get_missing_zips(logger, silent=True):
    """Returns a list of roots that do NOT have the zip yet."""
    missing = []
    found_zips = []
    for root in TEST_ROOTS:
        # Check for locked_folder.zip OR _locked_folder.zip
        # Adjust logic if you expect specific names
        expected_zip = root / EXPECTED_ZIP_NAME

        if not expected_zip.exists():
            missing.append(str(expected_zip))
        else:
            found_zips.append(str(expected_zip))

            # its interesting to check how long it takes to create al zips. idk how to check the beginning of the zip creations but here we can check when te first zip was created: (s, 18.2.'26 19:40 Wed)
            global creation_time_first_zip

            # p = Path(expected_zip)
            ctime = expected_zip.stat().st_mtime

            if not creation_time_first_zip:
                creation_time_first_zip = ctime
            else:
                global creation_time_last_zip
                if not creation_time_last_zip or ctime > creation_time_last_zip:
                    creation_time_last_zip = ctime


    return missing, found_zips


def _create_test_scenarios(logger):
    logger.info(f"Auto-Zip: _create_test_scenarios START, roots={TEST_ROOTS}")
    for root202603040230 in TEST_ROOTS:
        logger.info(f"Auto-Zip: checking parent: {root202603040230.parent} exists={root202603040230.parent.exists()}")

    if not core_logic_self_test_is_running_FILE.exists():
        _cleanup(logger)
    else:
        logger.info("Auto-Zip: 🛡️ Skipping initial cleanup - another test seems to be running.")

    for root in TEST_ROOTS:

        if not root.parent.exists():
            logger.error(f"Auto-Zip: ❌ exit! Parent-no exist: {root.parent} ==> exiting")

            m = "Auto-Zip: ❌ Abbruch! Parent-Ordner fehlt: {root.parent}"
            speak_fallback(f"{m}", 'de-DE')

            sys.exit(1)

        try:
            root.mkdir(parents=True, exist_ok=True)
            (root / "__init__.py").write_text("# Line 98")
            (root / "README_AUTOZIP.py").write_text("# Line 99")
            (root / "FUZZY_MAP_pre.py").write_text("# Line 108")

            locked = root / "_locked_folder" # Zip will be then root / "locked_folder.zip"

            logger.info(f"Auto-Zip: mkdir: {locked}")

            locked.mkdir(parents=True, exist_ok=True)
            (locked / "__init__.py").write_text("# Line 101")
            (locked / "README_AUTOZIP.py").write_text("# Line 102")

            de = locked / "de-DE"

            logger.info(f"Auto-Zip: mkdir: {de}")

            de.mkdir(parents=True, exist_ok=True)
            (de / "__init__.py").write_text("# Line 106")
            (de / "FUZZY_MAP_pre.py").write_text("# Line 108")

            (root / ".password").write_text("pwd")
        except Exception as e:
            m = f"Auto-Zip: Error creating scenario in {root}: {e}"
            logger.error(m)
            speak_fallback(m, 'de-DE')
            sys.exit(1)


import random


def run_auto_zip_random_quick_check(logger):
    # 1. Auswahl treffen
    selected_root = random.choice(TEST_ROOTS)
    logger.info(f"Auto-Zip: 🎲 Random Smoke Test - picking: {selected_root}")

    # 2. Den Rest des Scripts nur für diesen EINEN Root ausführen
    # Wir überschreiben global TEST_ROOTS für diesen Lauf
    global TEST_ROOTS
    original_roots = TEST_ROOTS
    TEST_ROOTS = [selected_root]

    try:
        # Hier rufst du deine normale run_auto_zip_sanity_check Logik auf
        run_auto_zip_sanity_check(logger)
    finally:
        # Optional: TEST_ROOTS wieder zurücksetzen (falls nötig)
        # TEST_ROOTS = original_roots
        pass



def _cleanup(logger):
    for root333 in TEST_ROOTS:
        if root333.exists():
            try:
                shutil.rmtree(root333)
                logger.info(f"Auto-Zip: Cleaned: {root333}")
            except Exception as e:
                logger.info(f"Auto-Zip: NOT Cleaned: {root333} Exception:{e}")
                pass
