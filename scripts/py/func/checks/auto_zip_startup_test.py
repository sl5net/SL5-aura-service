import sys
import time
import shutil
import threading
from pathlib import Path

from scripts.py.func.audio_manager import speak_fallback


import os
import platform



# scripts/py/func/checks/auto_zip_startup_test.py:9

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
TEST_DIR_Zip_NAME = f"_{TEST_DIR_NAME}.zip"

root = Path("config/maps/plugins")
# TEST_ROOTS = [p / TEST_DIR_NAME for p in sorted(root.iterdir()) if p.is_dir()]


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
        Path("config/maps/_privat") / TEST_DIR_NAME,
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


MAX_WAIT_SECONDS = 570  # Increased time for 6 folders!


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
        logger.error(f"Auto-Zip: Timeout! ⏰ {waited_sec}sec > {int(MAX_WAIT_SECONDS)}sec")
        speak_fallback(f"Auto-Zip: Timeout! Zeit abgelaufen {int(waited_sec)}sec > {int(MAX_WAIT_SECONDS)}sec",
                       'de-DE')
        global SUCCESS
        SUCCESS = False
        return True
    return False


def run_auto_zip_sanity_check(logger):
    start_time = time.time()

    def _test_logic():
        time.sleep(1)
        logger.info("Auto-Zip: 🧪 🚀 START: Sanity Check - multiple roots")
        # speak_fallback("START: Auto-Zip Test", 'de-DE')

        # 1. CLEANUP & SETUP
        try:
            _create_test_scenarios(logger)

            # 2. FORCE RELOAD
            # if map_reloader:
            #     logger.info("Auto-Zip: ⚡ Forcing Map Reload...")
            #     if hasattr(map_reloader, 'auto_reload_modified_maps'):
            #         # Pass True to force execution
            #         map_reloader.auto_reload_modified_maps(logger, True)
            #     elif hasattr(map_reloader, 'load_maps'):
            #         map_reloader.load_maps(logger)
            #     else:
            #         logger.warning("Auto-Zip: ⚠️ Method not found.")
            # else:
            #     logger.error("Auto-Zip: ❌ map_reloader missing.")

        except Exception as e:
            logger.error(f"Auto-Zip: 💀 Setup Error: {e}")

            sys.exit(1)

            return


        time.sleep(20) # the selftest probably needs much more than 30 seconds, so we can wait per default


        # 3. POLLING LOOP

        core_logic_self_test_was_running = False
        core_logic_self_test_not_running_anymore = None
        global SUCCESS

        logger.info(f"Auto-Zip: ⏰ start zeit -> {start_time}")
        speak_fallback(f"Auto-Zip: ⏰ start", 'de-DE')
        global SUCCESS

        while True:
            # global core_logic_self_test_is_running_FILE
            waited_sec = time.time() - start_time

            if not core_logic_self_test_was_running:
                logger.info(f"Auto-Zip: Waiting core_logic_self_test_was_running ... {waited_sec:.1f}s")
                if core_logic_self_test_is_running_FILE.exists():
                    core_logic_self_test_was_running = True
                else:
                    if timeout_auto_zip(waited_sec, MAX_WAIT_SECONDS, logger):
                        break
                    time.sleep(0.5)
                    continue

            if not core_logic_self_test_not_running_anymore:
                logger.info(f"Auto-Zip: Waiting core_logic_self_test_not_running_anymore ... {waited_sec:.1f}s")
                if not core_logic_self_test_is_running_FILE.exists():
                    core_logic_self_test_not_running_anymore = True
                else:
                    if timeout_auto_zip(waited_sec, MAX_WAIT_SECONDS, logger):
                        break
                    time.sleep(0.05)
                    continue

            if timeout_auto_zip(waited_sec, MAX_WAIT_SECONDS, logger):
                break

            # Check ALL roots
            missing_list, _ = _get_missing_zips(logger)
            if not missing_list:
                # LIST IS EMPTY = SUCCESS
                SUCCESS = True
                break
            # else:
            #     logger.info(f'Auto-Zip: 126: missing_list = {missing_list}')

            if timeout_auto_zip(waited_sec, MAX_WAIT_SECONDS, logger):
                break

            logger.debug(f"Auto-Zip: Waiting... ({len(missing_list)} remaining) {waited_sec:.1f}s")
            time.sleep(0.01)

        if SUCCESS is None:
            logger.error(f"Auto-Zip: SUCCESS is None {waited_sec:.1f}s.")
            speak_fallback("Auto-Zip: Error: SUCCESS is None . Das sollte nicht passieren", 'de-DE')
            # _cleanup(logger)
        elif SUCCESS:

            readme ='' # noqa: F841
            readme += r""" 
show modification times for all .zip files (recursive)
Sorted by newest first, with cleaner timestamp (no nanoseconds):
            
find . -type f -name '*.zip' -print0 \
| while IFS= read -r -d '' f; do
  printf '%s %s\n' "$(date -d "@$(stat -c %Y "$f")" '+%F %T')" "$f"
done \
| sort -r
           
            """

            # logger.info(f"Auto-Zip: ⏱️ Time from first ZIP to Finish: {zip_lag:.2f}s")

            # speak_fallback(f"Auto-Zip: Success in  {int(zip_lag)} Sekunden", 'de-DE')


            """
            19:52:25,729 - INFO     - Auto-Zip: Created creation time first_zip: 1771440710.7s
            19:52:25,729 - INFO     - Auto-Zip: 🎉 🟢 ALL Checks PASSED in 39.1s.
            """

            # logger.info(f"Auto-Zip: 🎉 🟢 ALL Checks PASSED in {waited_sec:.1f}s.")
            # speak_fallback(f"Auto-Zip: Success in  {int(waited_sec)} Sekunden", 'de-DE')

            finish_time = time.time()
            logger.info(f"Auto-Zip: 🎉 🟢 ALL Checks PASSED in {waited_sec:.1f}s.")

            # --- STATISTIK BERECHNUNG ---
            # global creation_time_first_zip, creation_time_last_zip
            if creation_time_first_zip and creation_time_last_zip:
                # 1. Wie lange hat das Zippen wirklich gedauert? (Von erster bis letzter Datei)
                zipping_duration = creation_time_last_zip - creation_time_first_zip
                zipping_duration = max(0.0, zipping_duration)  # Keine negativen Zahlen

                # 2. Wie lange hat der Test nach dem letzten Zip noch gewartet?
                test_lag = finish_time - creation_time_last_zip
                test_lag = max(0.0, test_lag)

                logger.info(f"Auto-Zip: 📊 Stats (this stats is without the  time for the create_test_scenarios setup!!!):")
                logger.info(f"Auto-Zip:   - Zipping Duration (Real Work): {zipping_duration:.2f}s")
                logger.info(f"Auto-Zip:   - Zipping per .Zip (Real Work): {(zipping_duration/len(TEST_ROOTS)):.2f}s")
                logger.info(f"Auto-Zip:   - Test/Lock-File Lag:           {test_lag:.2f}s")
                logger.info(f"Auto-Zip:   - Total Time:                   {waited_sec:.2f}s")

                # speak_fallback(f"Auto-Zip: Zipping took {round((zipping_duration)} seconds", 'de-DE')
                speak_fallback(f"Zip Dauer {round(zipping_duration)} Sekunden", 'de-DE')
                # speak_fallback(f"Zip Dauer je Datei {round(zipping_duration/len(TEST_ROOTS))} Sekunden", 'de-DE')


            core_logic_self_test_is_running_FILE.unlink(missing_ok=True)

            _cleanup(logger)
        elif not SUCCESS:
            logger.error("Auto-Zip: 💀 FAILED.")
            for roots in TEST_ROOTS:
                os.path.getctime(roots)

                logger.info(f"Auto-Zip: -searching: {roots}/{TEST_DIR_Zip_NAME}")
            missing, found_zips = _get_missing_zips(logger, silent=False)
            for missing_zip in missing:
                logger.error(f"Auto-Zip: ❌ Missing: {missing_zip}")
            for found_zip in found_zips:
                logger.info(f"Auto-Zip: ✅ found z: {found_zip}")
            speak_fallback("Auto-Zip: Failed", 'de-DE')

            core_logic_self_test_is_running_FILE.unlink(missing_ok=True)



            sys.exit(1)





    # 4. RESULT

    t = threading.Thread(target=_test_logic, daemon=True)
    t.start()
    logger.info("Auto-Zip: 🧵 Test Thread started.")

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
        expected_zip = root / "locked_folder.zip"

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
    _cleanup(logger)
    for root in TEST_ROOTS:
        try:
            root.mkdir(parents=True, exist_ok=True)
            (root / "__init__.py").write_text("# Line 98")
            (root / "README_AUTOZIP.py").write_text("# Line 99")

            locked = root / "_locked_folder" # Zip will be then root / "locked_folder.zip"
            locked.mkdir(parents=True, exist_ok=True)
            (locked / "__init__.py").write_text("# Line 101")
            (locked / "README_AUTOZIP.py").write_text("# Line 102")

            de = locked / "de-DE"
            de.mkdir(parents=True, exist_ok=True)
            (de / "__init__.py").write_text("# Line 106")
            (de / "FUZZY_MAP_pre.py").write_text("# Line 108")

            (root / ".password").write_text("pwd")
        except Exception as e:
            logger.error(f"Error creating scenario in {root}: {e}")


# Source - https://stackoverflow.com/a/39501288
# Posted by Mark Amery, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-18, License - CC BY-SA 4.0





def _cleanup(logger):
    for root333 in TEST_ROOTS:
        if root.exists():
            try:
                shutil.rmtree(root333)
                logger.info(f"Auto-Zip: Cleaned: {root333}")
            except Exception as e:
                logger.info(f"Auto-Zip: NOT Cleaned: {root333} Exception:{e}")

                pass
