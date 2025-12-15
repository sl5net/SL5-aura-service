# scripts/py/func/map_reloader.py
import importlib
import sys
import gc # Added for forced garbage collection
from pathlib import Path
import os

from config.dynamic_settings import settings
from scripts.py.func.private_map_ex import _private_map_ex
LAST_MODIFIED_TIMES = {}  # noqa: F824

def auto_reload_modified_maps(logger,run_mode_override):
    # scripts/py/func/map_reloader.py:12

    # logger.info(f'31: run_mode_override: {run_mode_override}')

    from .process_text_in_background import clear_global_maps

    global LAST_MODIFIED_TIMES  # noqa: F824

    """
    Scans the map directories, detects changed files based on their
    modification time, and reloads only the necessary modules.
    """

    if settings.DEV_MODE_memory:
        from scripts.py.func.log_memory_details import log_memory_details
        log_memory_details(f"def start", logger)

    # logger.info("Starting map reload check.")

    try:
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        maps_base_dir = project_root / "config" / "maps"

        # Track if any maps were reloaded, to know if we need a final GC call
        reload_performed = False


        # run_mode_override # os.getenv('RUN_MODE')  # returns None or the value
        logger.info(f'run_mode_override: {run_mode_override}')

        for map_file_path in maps_base_dir.glob("**/*.py"):
            if map_file_path.name == "__init__.py":
                continue

            # Security Check: Prevent loading of private maps (starting with _) in API mode
            # This checks ANY part of the path relative to maps_base_dir
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

                # 3. FORCE GARBAGE COLLECTION
                # Placed outside to always clean up before re-import
                gc.collect()
                if log_all_map_reloaded:
                    logger.info("🗑️ Forced garbage collection before re-import.")
                # --- END OF CLEANUP ---




                try:
                    # -------------------------------------------------------
                    # STANDARD TRIGGER LOGIC
                    # We try to import. If it is a .key file, this MUST fail.
                    # -------------------------------------------------------
                    module_to_reload = importlib.import_module(module_name)
                    importlib.reload(module_to_reload)




                    # Lifecycle Hook (only for valid modules)
                    # scripts/py/func/map_reloader.py:117
                    if hasattr(module_to_reload, 'on_reload') and callable(module_to_reload.on_reload):
                        try:
                            if log_all_map_reloaded:
                                logger.info(f"🚀 Triggering on_reload() for '{module_name}'")
                            module_to_reload.on_reload()
                        except Exception as hook_error:
                            logger.error(f"❌ Error in on_reload() for '{module_name}': {hook_error}")

                    LAST_MODIFIED_TIMES[map_file_key] = current_mtime
                    if log_all_map_reloaded:
                        logger.info(f"✅ Successfully reloaded '{module_name}'.")

                    # --- NEW CODE START ---
                    # logger.info(f'before run: _trigger_upstream_hooks({map_file_path}, {project_root}, logger) ')
                    _trigger_upstream_hooks(map_file_path, project_root, logger)
                    # --- NEW CODE END ---



                except Exception as e:
                    # -------------------------------------------------------
                    # EXCEPTION HANDLER -> PRIVATE MAP CHECK
                    # -------------------------------------------------------

                    # DEBUG: Log that we hit an exception (expected for key files)
                    # logger.info(f"💥 Import Exception - check its private? for {module_name}: {e}")

                    was_private_map = _private_map_ex(map_file_key, logger)



                    if was_private_map:
                        # Successfully handled a private map. Skip to next file.
                        continue

                        # If it wasn't a private map, log the original error

                    logger.error(f"❌ Failed to reload module '{module_name}': {e}")

                    # logger.error(f"❌ Failed to reload module '{module_name}': {e}")
                    # todo: # scripts/py/func/map_reloader.py:135 run the into autorepair function

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
        logger.error(f"Error during map reload check: {e}")

    if settings.DEV_MODE_memory:
        from scripts.py.func.log_memory_details import log_memory_details

        log_memory_details(f"def end", logger)

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



# scripts/py/func/map_reloader.py

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

    # 1. Define the stop boundary
    # We stop scanning when we reach 'config/maps' to avoid scanning the whole project
    # logger.info(f'scripts/py/func/map_reloader.py:_trigger_upstream_hooks:518')
    stop_dir = project_root / "config" / "maps"
    # logger.info(f'scripts/py/func/map_reloader.py:_trigger_upstream_hooks:521')
    current_dir = start_path.parent
    # logger.info(f'scripts/py/func/map_reloader.py:_trigger_upstream_hooks:523 -> current_dir:{current_dir}')

    # Safety check: verify we are inside config/maps
    try:
        current_dir.relative_to(stop_dir)
    except ValueError as e:
        logger.info(f'x scripts/py/func/map_reloader.py:_trigger_upstream_hooks:533 -> {e}')
        return  # Outside of scope

    # 2. Traverse Upwards
    while stop_dir in current_dir.parents or current_dir == stop_dir:
        # logger.info(f"🔍 Scanning for lifecycle hooks in: {current_dir}")

        # Iterate over all .py files in this directory level
        for file_path in current_dir.glob("*.py"):
            # Skip the file we just reloaded (avoid infinite loop or double execution)
            if file_path.resolve() == start_path.resolve():
                continue

            # Skip hidden files (except maybe the ones explicitly needed, but usually hidden are keys)
            if file_path.name.startswith('.'):
                continue

            try:
                # Calculate module name for import
                relative_path = file_path.relative_to(project_root)
                module_name = str(relative_path.with_suffix('')).replace(os.path.sep, '.')

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
                    except Exception as e:
                        logger.info(f'error importing module {module_name}: {e}')
                        continue

                # 3. Check and Execute Hook
                if module and hasattr(module, 'on_folder_change') and callable(module.on_folder_change):
                    # logger.info(f"🔗 Triggering upstream hook: {module_name}.on_folder_change()")
                    try:
                        module.on_folder_change()
                    except Exception as e:
                        logger.error(f"scripts/py/func/map_reloader.py -> in upstream hook '{module_name}': Exception: {e}")

            except Exception as e:
                # Suppress errors from unrelated files
                logger.info(f'❌ scripts/py/func/map_reloader.py:575 -> Exception: {e}')
                pass

        # Move one level up
        if current_dir == stop_dir:
            break
        current_dir = current_dir.parent
