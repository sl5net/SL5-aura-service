# scripts/py/func/map_reloader.py
from .config.regex_cache import clear_regex_cache
import importlib
import sys
import platform
import gc # Added for forced garbage collection
from pathlib import Path
import os
import time

from pyzipper import zipfile

from .config.dynamic_settings import DynamicSettings
settings = DynamicSettings()


from .log_memory_details import log4DEV
from .private_map_ex import _private_map_unpack
from .auto_fix_module import try_auto_fix_module
from .validate_map_structure import check_map_health
from .windows_apply_correction_with_sync import windows_apply_correction_with_sync
LAST_MODIFIED_TIMES = {}  # noqa: F824

KNOWN_MAP_Names = {'FUZZY_MAP_pre', 'FUZZY_MAP', 'PUNCTUATION_MAP'}
# KNOWN_MAP_ATTRIBUTES = {'FUZZY_MAP_pre', 'FUZZY_MAP', 'PUNCTUATION_MAP', 'on_reload', 'on_folder_change'}



def auto_reload_modified_maps(logger,run_mode_override):

    # its using:

    # may read: https://github.com/sl5net/SL5-aura-service/tree/master/docs/Feature_Spotlight/zip

    # importlib.reload(module): its changes the Memory of the Python-Interpreters (sys.modules).
    # iss also changes the:
    # LAST_MODIFIED_TIMES[...] = ...:

    # scripts/py/func/map_reloader.py:12

    # logger.info(f'31: run_mode_override: {run_mode_override}')

    from .process_text_in_background import clear_global_maps

    global LAST_MODIFIED_TIMES  # noqa: F824

    """
    Scans the map directories, detects changed files based on their
    modification time, and reloads only the necessary modules.
    """

    if getattr(settings, "DEV_MODE_memory", False):
        from .log_memory_details import log_memory_details
        log_memory_details("def start", logger)

    # logger.info("Starting map reload check.")

    # func/map_reloader.py:34
    try:
        # scripts/py/func/map_reloader.py:33
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        maps_base_dir = project_root / "config" / "maps"

        # Track if any maps were reloaded, to know if we need a final GC call
        reload_performed = False


        # run_mode_override # os.getenv('RUN_MODE')  # returns None or the value
        logger.info(f'run_mode_override: {run_mode_override} (other examples: API_SERVICE , ...)')

        # func/map_reloader.py:46
        for map_file_path in maps_base_dir.glob("**/*.py"):
            if map_file_path.name == "__init__.py":
                continue
            if map_file_path.name == "__init__":
                continue


            # Security Check: Prevent loading of private maps (starting with _) in API mode
            # This checks ANY part of the path relative to maps_base_dir
            # func/map_reloader.py:54: auto_reload_modified_maps(logger,run_mode_override)
            if run_mode_override == "API_SERVICE":
                try:
                    # Get path relative to /config/maps to check subfolders
                    relative_path = map_file_path.relative_to(maps_base_dir)

                    # Check if any folder in the structure starts with "_"
                    if any(part.startswith('_') for part in relative_path.parts):
                        logger.info(f"🔒 Security: Ignoring private map update: {relative_path}")
                        continue
                except ValueError:
                    continue  # Should not happen, but safe fallback

            # func/map_reloader.py:67
            map_file_key = str(map_file_path)

            # Using time.time() for current time, though os.path.getmtime is fine for file checks
            current_mtime = os.path.getmtime(map_file_key)
            last_mtime = LAST_MODIFIED_TIMES.get(map_file_key, 0)

            # CRITICAL CHECK: Reload if modified OR if it's a new file (last_mtime == 0)
            if last_mtime == 0:
                map_file_path_obj = Path(map_file_path)
                ensure_init_files(map_file_path_obj.parent, logger)
            # scripts/py/func/map_reloader.py:77
            if current_mtime > last_mtime:
                reload_performed = True

                _reload_start_time = time.time()  # NEU

                if last_mtime != 0:
                    if settings.DEV_MODE:
                        logger.info(f"🔄 Detected change in '{map_file_path}'. Reloading...")


                # scripts / py / func / map_reloader.py: 84

                relative_path = map_file_path.relative_to(project_root)
                module_name = str(relative_path.with_suffix('')).replace(os.path.sep, '.')

                log_all_map_reloaded = settings.DEV_MODE_all_processing

                # --- START OF COMPLETE MEMORY LEAK FIX & CLEANUP ---
                if module_name in sys.modules:
                    # 1. CLEAR CENTRAL REGISTRY (Breaks references to old ast.* objects)
                    # logger.info("🗑️ Calling clear_global_maps to release old function references.")
                    clear_global_maps(logger)

                    # 2. DELETE OLD MODULE (Breaks the global reference in Python's cache)
                    # logger.info(f"🗑️ Deleting old module reference for {module_name} from sys.modules.")
                    del sys.modules[module_name]

                    # 3. FORCE GARBAGE COLLECTION (only when actually reloading)
                    gc.collect()
                    clear_regex_cache()
                    if log_all_map_reloaded:
                        logger.info(" Forced garbage collection before re-import.")

                # --- END OF CLEANUP ---

                # log_all_changes = True
                log_all_changes = False

                try:
                    # -------------------------------------------------------
                    # In def auto_reload_modified_maps(logger,run_mode_override): -> scripts/py/func/map_reloader.py:127
                    # STANDARD TRIGGER LOGIC
                    # We try to import. If it is a .key file, this MUST fail.
                    # -------------------------------------------------------
                    module_to_reload = importlib.import_module(module_name)

                    # if not any(hasattr(module_to_reload, attr) for attr in KNOWN_MAP_ATTRIBUTES):
                    #     logger.debug(f"⏩ Skipping reload — no map structure found: {module_name}")
                    #     LAST_MODIFIED_TIMES[map_file_key] = current_mtime
                    #     continue

                    importlib.reload(module_to_reload)


                    # Lifecycle Hook (only for valid modules)
                    # scripts/py/func/map_reloader.py:117
                    if module_name is not None and hasattr(module_to_reload, 'on_reload') and callable(module_to_reload.on_reload):
                        try:
                            if log_all_map_reloaded or log_all_changes:
                                logger.info(f"🚀 Triggering on_reload() for '{module_name}'")
                            module_to_reload.on_reload()
                        except Exception as hook_error:
                            logger.info(f"❌ 🚨 Error in on_reload() for '{module_name}': {hook_error}")

                    LAST_MODIFIED_TIMES[map_file_key] = current_mtime

                    _reload_duration = time.time() - _reload_start_time  # NEU
                    if _reload_duration > 0.1:  # nur loggen wenn merklich langsam
                        logger.info(f"⌚ slow? 🐌 map reload: {module_name} took {_reload_duration:.2f}s")

                        if module_name not in KNOWN_MAP_Names:
                            logger.debug(f"lets do it conservative: if not {module_name} in KNOWN_MAP_Names and slo 🐌 ⏩ Skipping reload")
                            continue
                        # if not any(hasattr(module_to_reload, attr) for attr in KNOWN_MAP_ATTRIBUTES):
                        #     logger.debug(f"⏩ Skipping reload — no map structure found: {module_name}")
                        #     LAST_MODIFIED_TIMES[map_file_key] = current_mtime
                        #     continue

                        # continue
                        #

                    if log_all_map_reloaded or log_all_changes:
                        logger.info(f"✅ Successfully reloaded '{module_name} in  {_reload_duration:.2f}s'.")

                    # --- NEW CODE START ---
                    if log_all_map_reloaded or log_all_changes:
                        logger.info(f'before run: ↖️_trigger_upstream_hooks(📜...{str(map_file_path)[-25:]} ) ')
                    _trigger_upstream_hooks(map_file_path, project_root, logger)
                    # --- NEW CODE END ---

                    if module_to_reload is not None and hasattr(module_to_reload, 'FUZZY_MAP_pre'):
                        # def check_map_health(file_path, map_entries, logger):
                        check_map_health(file_path=map_file_path, module=module_to_reload, logger=logger)


                except (NameError, SyntaxError) as e:
                    logger.error(f"151:🚨 Error Import: {e}")
                    logger.error(f"151: {module_name}")
                    logger.error(f"151: {relative_path}")
                    was_fixed = try_auto_fix_module(relative_path, e, logger)
                    if was_fixed:
                        logger.info("🔧 Fix successful. Reload...")
                        try:
                            importlib.invalidate_caches()
                            module = importlib.import_module(module_name)
                            importlib.reload(module)
                            logger.info(f"✅ Reload successful: {module_name}")

                            if platform.system() == "Windows":
                                windows_apply_correction_with_sync()


                        except Exception as retry_error:
                            logger.info(f"🚨 ❌ Fix failed: {retry_error}")


                # scripts/py/func/map_reloader.py:151
                except Exception as e:
                    # -------------------------------------------------------
                    # EXCEPTION HANDLER -> PRIVATE MAP CHECK
                    # -------------------------------------------------------

                    # DEBUG: Log that we hit an exception (expected for key files)
                    # logger.info(f"💥 Import Exception - check its private? for {module_name}: {e}")

                    # func/map_reloader.py:153
                    was_private_map = _private_map_unpack(map_file_key, logger)



                    if was_private_map:
                        # Successfully handled a private map. Skip to next file.
                        continue

                        # If it wasn't a private map, log the original error

                    logger.info(f"🚨 ❌ Failed to reload module '{module_name}': {e}")

                    # logger.error(f"❌ Failed to reload module '{module_name}': {e}")
                    # todo: # scripts/py/func/map_reloader.py:135 run the into auto-repair function


            else:
                # No change detected, but ensure initialization logic handles new paths if needed
                if map_file_key not in LAST_MODIFIED_TIMES:
                    LAST_MODIFIED_TIMES[map_file_key] = current_mtime
                    map_file_path = Path(map_file_path)
                    ensure_init_files(map_file_path.parent, logger)

        # scripts/py/func/map_reloader.py:155


        # Optional: Final cleanup if any reload occurred
        if reload_performed:
            gc.collect()

            # if log_all_map_reloaded:
            #     logger.info("🗑️ Final garbage collection after map scan.")

    except Exception as e:
        logger.error(f"🚨 Error during map reload check: {e}")

    if getattr(settings, "DEV_MODE_memory", False):
        from .log_memory_details import log_memory_details

        log_memory_details("def end", logger)

# scripts/py/func/map_reloader.py:174
# --- HELPER FUNCTION  ---







# following can make the script littlbe bit faster sometimes (1% or so)
# log:
# 11:23:31,808 - INFO     - ⌚ self_test_readable_duration: 0:00:58.448283
# 11:50:31,284 - INFO     - ⌚ self_test_readable_duration: 0:00:57.441311
INITIAL_WAIT_TIME = 2.0
MAX_WAIT_TIME = 60.0

def ensure_init_files(current_dir: Path, logger):
    """
    Stellt sicher, dass __init__.py Dateien existieren.
    Wandert von current_dir nach OBEN.
    Nutzt ein SET, um Verzeichnisse nicht doppelt zu prüfen (statt Zeit-Drosselung).
    """

    # --- 1. Cache Logic (Ersetzt Time Throttling) ---
    # Wir merken uns, welche Pfade wir schon "repariert" haben.
    if not hasattr(ensure_init_files, 'checked_paths'):
        ensure_init_files.checked_paths = set()

    # Wenn wir diesen Start-Ordner schon erledigt haben, brechen wir sofort ab.
    # Das spart Performance in der Schleife.
    if current_dir in ensure_init_files.checked_paths:
        return True

    # --- 2. SICHERE REKURSION NACH OBEN ---

    temp_path = current_dir.resolve()
    user_home = Path.home().resolve()

    # Liste der Ordner-Namen, bei denen wir definitiv aufhören
    stop_markers = {'maps', 'config', 'STT', 'projects'}

    # Sicherheits-Limit: Max 10 Ebenen hoch
    for _ in range(10):

        # Wenn wir diesen Pfad schonmal geprüft haben, können wir hier stoppen.
        # (Wir wissen ja, dass wir von dort aus schonmal nach oben gewandert sind)
        if temp_path in ensure_init_files.checked_paths:
            break

        # NOTBREMSE 1: Wir sind im Home-Dir oder Root
        if temp_path == user_home or temp_path == Path('/'):
            break

        # __init__.py erstellen
        _create_init_file(temp_path / "__init__.py", logger)

        # Pfad als "erledigt" markieren
        ensure_init_files.checked_paths.add(temp_path)

        # NOTBREMSE 2: Wir haben gerade 'maps' oder 'config' bearbeitet -> Fertig.
        if temp_path.name in stop_markers:
            break

        # Eine Ebene höher gehen
        temp_path = temp_path.parent

    return True

def _create_init_file(file_path: Path, logger):
    if not file_path.exists():
        try:
            file_path.touch(exist_ok=True)
            if settings.DEV_MODE:
                logger.info(f"🔧 Auto-Repair: Created package marker '{file_path}'")
            return True
        except OSError:
            pass
    return False



# scripts/py/func/map_reloader.py:321
def _trigger_upstream_hooks(start_path: Path, project_root: Path, logger):
    """
    Traverses up the directory tree from start_path up to 'config/maps'.
    Looks for sibling/parent Python files that have an 'on_folder_change' hook
    and executes them. This ensures packers (like secure_packer.py) are triggered.
    """
    if start_path.name.startswith('.'):
        return

    import importlib
    import sys

    log_everything = False
    # log_everything = True

    # 1. Define the stop boundary
    # We stop scanning when we reach 'config/maps' to avoid scanning the whole project
    # logger.info(f'scripts/py/func/map_reloader.py:_trigger_upstream_hooks:518')
    stop_dir = project_root / "config" / "maps"
    # logger.info(f'scripts/py/func/map_reloader.py:_trigger_upstream_hooks:521')
    current_dir = start_path.parent
    if log_everything:
        logger.info(f'scripts/py/func/map_reloader.py:_trigger_upstream_hooks:523 -> current_dir:{current_dir}')

    # Safety check: verify we are inside config/maps
    try:
        current_dir.relative_to(stop_dir)
    except ValueError as e:
        logger.info(f'x scripts/py/func/map_reloader.py:_trigger_upstream_hooks:533 -> {e}')
        return  # Outside of scope

    # 2. Traverse Upwards
    start_path_current_dir = ancestor_up_to_last_underscore_no_io(start_path)

    # scripts/py/func/map_reloader.py:355
    while stop_dir in current_dir.parents or current_dir == stop_dir:

        # Iterate over all .py files in this directory level
        for file_path in current_dir.glob("*.py"):

            if file_path.name.startswith('__'):
                continue
            if log_everything:
                logger.info(f"🔍 Scanning for lifecycle hooks in: {str(current_dir)[-35:]}")

            if log_everything:
                logger.info(f"🔍:304 ...{str(file_path)[-35:]}")

            # Skip the file we just reloaded (avoid infinite loop or double execution)
            if file_path.resolve() == start_path.resolve():
                if log_everything:
                    logger.info(f"🔍:308 {str(file_path)[-35:]}")
                continue

            # Skip hidden files (except maybe the ones explicitly needed, but usually hidden are keys)
            if file_path.name.startswith('.'):
                if log_everything:
                    logger.info(f"🔍:313 {str(file_path)[-35:]}")
                continue

            try:
                # Calculate module name for import
                relative_path = file_path.relative_to(project_root)
                module_name = str(Path(relative_path.with_suffix(''))).replace(os.path.sep, '.')
                if log_everything:
                    logger.info(f"🔍🔍 module_name: {module_name} | relative_path: {relative_path}")

                # We only want to trigger modules that are ALREADY loaded or are the Packer.
                # If we blindly import everything, we might start modules that should be off.
                # BUT: secure_packer.py should be in sys.modules if it ran at start.

                module = None
                if module_name in sys.modules:
                    module = sys.modules[module_name]
                else:
                    # Optional: explicit check for packer naming convention if needed?
                    # For now, we try to import to be safe if it was unloaded.
                    try:
                        module = importlib.import_module(module_name)
                    except (ImportError, ModuleNotFoundError):
                        if log_everything:
                            logger.info(f"ℹ️ Ignoring non-importable file: {module_name}")
                        continue

                    # scripts/py/func/map_reloader.py:368
                    except (NameError, SyntaxError, Exception) as e:
                        logger.error(f"🚨 Error Import: {e}")
                        logger.info(f"🚨 Error Import: {e}")

                        was_fixed = try_auto_fix_module(file_path, e, logger)

                        if was_fixed:
                            logger.info("🔧 Fix wurde angewendet. Starte sofortigen Reload-Versuch...")

                            try:
                                # WICHTIG: Caches leeren, damit Python merkt, dass die Datei auf der Platte neu ist
                                importlib.invalidate_caches()

                                # 2. Versuch: Erneuter Import
                                module = importlib.import_module(module_name)
                                importlib.reload(module)  # Sicherstellen, dass es wirklich frisch ist

                                logger.info(f"✅ Reload good, Auto-Fix: {module_name}")

                                # Hier machen wir weiter, als ob nichts passiert wäre
                                # (Der Code unter dem try/except Block nutzt jetzt das reparierte 'module')
                                # Falls du danach Code hast, der 'module' nutzt, läuft er jetzt durch.

                            except Exception as retry_error:
                                logger.info(f"error 🚨 ❌ Reload failed: retry_error: {retry_error}")
                                continue  # Abbrechen für dieses Modul
                        else:
                            # Kein Fix möglich -> Weiter zum nächsten
                            continue

                        if log_everything:
                            log4DEV('Example: ',logger)

                            """
14:47:20,095 - ERROR    - 🔥 Error in zip_all/de-DE/zip.py:236 on_reload: attempted relative import with no known parent package
14:47:20,959 - INFO     - ❌ scripts/py/func/map_reloader.py:361 -> _trigger_upstream_hooks(start_path ...) 🚨 error importing module 🚨 
config.maps.plugins.sandbox.de-DE.FUZZY_MAP_pre: name 'lauffe' is not defined

                            """

                    except Exception as e:
                        logger.info(f'❌ scripts/py/func/map_reloader.py:361 -> _trigger_upstream_hooks(start_path ...) '
                                    f'🚨 error importing module 🚨 {module_name}: {e}')
                        continue

                # scripts/py/func/map_reloader.py:355
                # 3. Check and Execute Hook

                # scripts/py/func/map_reloader.py
                # Add a log before the hasattr check
                # logger.info(f"375: Checking module {module_name} for hooks...")

                if module is not None and module and hasattr(module, 'on_folder_change') and callable(module.on_folder_change):

                    if (not start_path_current_dir
                            or not start_path_current_dir.name):
                        continue


                    if not start_path_current_dir.name.startswith('_'):
                        if log_everything:
                            logger.info(f"🛑 Skipping hook for '{start_path_current_dir.name}' - folder does not start with '_'")
                        continue

                    if log_everything:
                        logger.info(f"🔗 Triggering upstream hook: 📜{module_name}.on_folder_change(start_path_current_dir:📂...{str(start_path_current_dir)[-35:]}")
                    try:
                        module.on_folder_change(start_path_current_dir)
                    except Exception as e:
                        logger.info(f"Error: 🚨 scripts/py/func/map_reloader.py -> in ↖️upstream hook '{module_name}': Exception: {e}")

            # scripts/py/func/map_reloader.py:342
            except Exception as e:
                # Suppress errors from unrelated files
                logger.info(f'❌ 🚨 scripts/py/func/map_reloader.py:575 -> Exception: {e} <- …{str(file_path)[-45:]}')
                pass

        # Move one level up
        if current_dir == stop_dir:
            break
        current_dir = current_dir.parent

    # def ancestor_up_to_last_underscore(path):
    #     p = Path(path)
    #     # if it exists, decide by filesystem; otherwise use suffix heuristic
    #     if p.exists():
    #         start = p if p.is_dir() else p.parent
    #     else:
    #         start = p.parent if p.suffix else p
    #
    #     for candidate in (start, *start.parents):
    #         if candidate.name.startswith("_"):
    #             return candidate
    #     return None

# from pathlib import Path

def ancestor_up_to_last_underscore_no_io(path):
    p = Path(path)
    parts = p.parts
    # if the last part looks like a filename (has a dot), start from parent
    start_index = len(parts) - 1
    if '.' in parts[-1]:
        start_index -= 1
    for i in range(start_index, -1, -1):
        if parts[i].startswith('_'):
            return Path(*parts[: i + 1])
    return None


def zip_me_nopassword(zip_path_outer, current_dir_or_single_file):
    target_path = str(current_dir_or_single_file)

    # Standard Zip
    zip_context = zipfile.ZipFile(
        zip_path_outer,
        "w",
        compression=zipfile.ZIP_DEFLATED
    )

    # 2. Open Zip and Write Files
    with zip_context as zf:

        # CASE A: Single File
        if os.path.isfile(target_path):
            arc_name = os.path.basename(target_path)
            zf.write(target_path, arc_name)

        # CASE B: Directory
        else:
            # We want the archive names relative to the target directory
            # If target is /tmp/data, and file is /tmp/data/sub/img.jpg
            # arc_name should be sub/img.jpg (or data/sub/img.jpg depending on preference)

            # This logic mimics your original string slicing (contents relative to root):
            parent_dir = target_path

            for root, _, files in os.walk(target_path): # map_reloader.py:533
                for fn in files:
                    full_path = os.path.join(root, fn)
                    # relpath calculates the correct relative path automatically
                    arc_name = os.path.relpath(full_path, start=parent_dir)
                    zf.write(full_path, arc_name)

    #logger.info(f"📄 📦 Zip Output: {zip_path_outer}")
# scripts/py/func/map_reloader.py:546
