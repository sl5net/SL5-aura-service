# scripts/py/func/map_reloader.py
import importlib
import sys
import gc # Added for forced garbage collection
import pathlib
from pathlib import Path
import os
import zipfile
import shutil







#import time # Added for os.path.getmtime typing, just in case

from config.dynamic_settings import settings

#from .process_text_in_background import repariere_pakete_mit_laenderkuerzeln



LAST_MODIFIED_TIMES = {}  # noqa: F824


def auto_reload_modified_maps(logger):
    # scripts/py/func/map_reloader.py:12
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

        for map_file_path in maps_base_dir.glob("**/*.py"):
            if map_file_path.name == "__init__.py":
                continue  # Ignore __init__.py files

            map_file_key = str(map_file_path)


            # Using time.time() for current time, though os.path.getmtime is fine for file checks
            current_mtime = os.path.getmtime(map_file_key)
            last_mtime = LAST_MODIFIED_TIMES.get(map_file_key, 0)

            # CRITICAL CHECK: Reload if modified OR if it's a new file (last_mtime == 0)

            if last_mtime == 0:
                map_file_path_obj = Path(map_file_path)
                ensure_init_files(map_file_path_obj.parent, logger)

            if current_mtime > last_mtime:
                reload_performed = True

                if last_mtime != 0:
                    if settings.DEV_MODE:
                        logger.info(f"🔄 Detected change in '{map_file_path}'. Reloading...")
                # else:
                #     if settings.DEV_MODE:
                #         logger.info(f"🆕 Detected new map file: '{map_file_path}'. Loading...")

                relative_path = map_file_path.relative_to(project_root)
                module_name = str(relative_path.with_suffix('')).replace(os.path.sep, '.')

                log_all_map_reloaded = settings.DEV_MODE_all_processing

                # --- START OF COMPLETE MEMORY LEAK FIX ---
                if module_name in sys.modules:
                    # 1. CLEAR CENTRAL REGISTRY (Breaks references to old ast.* objects)
                    logger.info("🗑️ Calling clear_global_maps to release old function references.")
                    clear_global_maps(logger)

                    # 2. DELETE OLD MODULE (Breaks the global reference in Python's cache)
                    logger.info(f"🗑️ Deleting old module reference for {module_name} from sys.modules.")
                    del sys.modules[module_name]

                # 3. FORCE GARBAGE COLLECTION
                # Placed outside the 'if module_name in sys.modules' to always clean up before re-import
                # (in case a map was deleted, like in our test).
                gc.collect()
                if log_all_map_reloaded:
                    logger.info("🗑️ Forced garbage collection before re-import.")

                # --- END OF COMPLETE MEMORY LEAK FIX ---

                # scripts/py/func/map_reloader.py:82
                try:
                    # 4. CORRECT FRESH IMPORT
                    # Import fresh: This finds and executes the module again, populating the now-cleared global maps.
                    #module_to_reload = importlib.import_module(module_name)

                    # Note: importlib.reload() is not used after del sys.modules

                    module_to_reload = importlib.import_module(module_name)  # 4. Correct Fresh Import
                    importlib.reload(module_to_reload)

                    LAST_MODIFIED_TIMES[map_file_key] = current_mtime
                    if log_all_map_reloaded:
                        logger.info(f"✅ Successfully reloaded '{module_name}'.")

                    # CRITICAL STEP 4: Import the module fresh (instead of using importlib.reload)
                    # Re-importing from scratch is cleaner than reload for memory management.
                    module_to_reload = importlib.import_module(module_name)

                    # Note: If your system uses a central registry/list of map functions,
                    # you MUST clear the old functions from that registry NOW,
                    # then re-add the new functions from module_to_reload.

                    LAST_MODIFIED_TIMES[map_file_key] = current_mtime
                    if log_all_map_reloaded:
                        logger.info(f"✅ Successfully reloaded '{module_name}'.")

                    LAST_MODIFIED_TIMES[map_file_key] = current_mtime
                    if settings.DEV_MODE:
                        logger.info(f"✅ Successfully reloaded/loaded '{module_name}'.")

                except Exception as e:
                    # --- NEW LOGIC: Check for private map pattern ---
                    was_private_map = _handle_private_map_exception(module_name, map_file_key, logger)
                    # logger.info(f"??????🔄 should we do unpack")

                    if was_private_map:
                        # Successfully handled a private map. The files are now in the _*-dir.
                        # We can 'continue' the outer loop. The files will be picked up
                        # by the file scanning logic on the next iteration of 'check_and_reload_maps'.
                        # logger.info(f"🔄 pick up from '_'-directory in next scan.")
                        continue  # Skip to the next file in the list

                    # If it wasn't a private map, log the original error

                    # thats to much disturbinb messages in console.log there fadd comment:
                    logger.error(f"❌ Failed to reload module '{module_name}': {e}")

                    # todo: # scripts/py/func/map_reloader.py:135 run the into autorapair function

                    # ... existing comment block
                    """
                    Modules that you import with the import statement must follow the same naming rules set for variable names (identifiers). Specifically, they must start with either a letter1 or an underscore and then be composed entirely of letters, digits2, and/or underscores.
                    can used to protect folder from loading. when use . at beginning. 
                    """

            else:
                # If no change detected, just ensure its mtime is recorded if it's a new entry

                # 03:37:44,491 - INFO     - Checking map file: /home/seeh/projects/py/STT/config/maps/plugins/it-begriffe/php/codeigniter/de-DE/FUZZY_MAP_pre.py ööööööööööööööööööööööööööööööööööööööööööööööööööööööööö
                map_file_path = Path(map_file_path)
                map_dir_path = map_file_path.parent


                # Use the function by providing the directory path
                # ensure_init_files(map_dir_path,logger)
                ensure_init_files(map_dir_path, logger, stop_at_marker="maps")

                # init_file = map_dir_path / "__init__.py"
                # if not init_file.exists():
                #     try:
                #         init_file.touch()
                #         logger.info(f"init_file.touch ")
                #     except OSError as e:
                #         logger.error(
                #             f"err: init_file.touch: {e}")

                if map_file_key not in LAST_MODIFIED_TIMES:
                    LAST_MODIFIED_TIMES[map_file_key] = current_mtime
                    # 03:37:44,491 - INFO     - Checking map file: /home/seeh/projects/py/STT/config/maps/plugins/it-begriffe/php/codeigniter/de-DE/FUZZY_MAP_pre.py ööööööööööööööööööööööööööööööööööööööööööööööööööööööööö

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


# --- HELPER FUNCTION (Needs to be added to map_reloader.py) ---
def _handle_private_map_exception(module_name: str, map_file_key: str, logger) -> bool:
    """
    Checks if a failed module load is actually a private ZIP/Key pattern
    (Triggered by a dot-prefixed .py file). Unpacks the ZIP and returns True.

    Returns:
        True if a private map was successfully unpacked (or found unpacked), False otherwise.
    """
    # 1. Determine the map directory
    map_dir = str(pathlib.Path(map_file_key).parent)

    # 2. Check for the private map pattern in this directory
    key_file = None
    zip_file = None

    for item in os.listdir(map_dir):
        # Trigger is now a .py file that starts with a dot
        if item.startswith('.') and item.endswith('.py') and os.path.isfile(os.path.join(map_dir, item)):
            key_file = os.path.join(map_dir, item)
        # ZIP file is the one we want to unpack
        if item.lower().endswith('.zip') and os.path.isfile(os.path.join(map_dir, item)):
            zip_file = os.path.join(map_dir, item)

    if not (key_file and zip_file):
        # Not the pattern we are looking for. (e.g., a real syntax error in a normal map)
        return False

    # 3. Pattern found: Extract Key and set Unpack Target
    try:

        # --------------------------------------------------------------------------------
        # CRITICAL SECURITY STEP (23.11.'25 14:07 Sun)
        if not _check_gitignore_for_security(logger):
            return False # ABORT! Do not unpack if security rules are missing.
        # --------------------------------------------------------------------------------


        with open(key_file, 'r') as f:
            password = f.read().strip()


        map_dir = str(pathlib.Path(map_file_key).parent)
        zip_name_base = pathlib.Path(zip_file).stem

        # The FINAL target directory where the maps will reside (e.g., config/maps/private/_privat)
        if zip_name_base.startswith('_'):
            target_maps_dir = os.path.join(map_dir, f"{zip_name_base}")
        else:
            target_maps_dir = os.path.join(map_dir, f"_{zip_name_base}")

        if os.path.exists(target_maps_dir):
            # If the final directory exists, we assume it's correctly unpacked and ready for editing.
            # logger.info(f"✅ Private maps already unpacked to '{target_maps_dir}'. Skipping ZIP operation.")
            return True

        # --------------------------------------------------------------------------------
        # 4. UNPACKING LOGIC: Use a temporary, hidden directory to neutralize ZIP's internal folder structure
        temp_unpack_dir = os.path.join(map_dir, f".__tmp_unpack_{os.getpid()}")  # Unique name
        os.makedirs(temp_unpack_dir, exist_ok=False)

        logger.info(f"🔑 Private map pattern found. Unpacking '{zip_file}' to TEMP: '{temp_unpack_dir}'.")

        with zipfile.ZipFile(zip_file, 'r') as zf:
            zf.extractall(temp_unpack_dir, pwd=password.encode('utf-8'))

        # --------------------------------------------------------------------------------
        # 5. NORMALIZATION LOGIC: Find the actual map files within the temp dir and move them

        # 5a. Find the directory that contains the real map files
        content = os.listdir(temp_unpack_dir)
        source_dir = temp_unpack_dir

        if len(content) == 1 and os.path.isdir(os.path.join(temp_unpack_dir, content[0])):
            # This is the 'extra' folder created by the 'Right-Click -> Zip' operation.
            # E.g., temp/__privat/
            source_dir = os.path.join(temp_unpack_dir, content[0])
            logger.info(f"📁 Found top-level folder in ZIP: '{source_dir}'. Normalizing path.")

        # 5b. Create the FINAL target directory
        os.makedirs(target_maps_dir, exist_ok=True)

        # 5c. Move all files/folders from the source_dir to the final target_maps_dir
        for item in os.listdir(source_dir):
            shutil.move(os.path.join(source_dir, item), target_maps_dir)

        # 5d. Cleanup
        shutil.rmtree(temp_unpack_dir)

        logger.info(f"📦 Unpack and Normalization complete. Files ready in '{target_maps_dir}'.")
        return True

    except Exception as e:
        # We explicitly log the exact error here to help with debugging the ZIP/Key/shutil process
        logger.error(f"❌ Failed to process private map ZIP/Key: {e}", exc_info=True)
        # Clean up in case of failure
        if os.path.exists(temp_unpack_dir):
            shutil.rmtree(temp_unpack_dir)
        return False

def _check_gitignore_for_security(logger) -> bool:
    """
    Verifies that the required .gitignore entries for private maps are present
    in the main .gitignore file by direct string check.

    Returns:
        True if all required security rules are present, False otherwise.
    """
    # Assuming the main .gitignore is in the project's root directory (or equivalent base)
    # We need to find the root of the project to locate the main .gitignore
    # Let's assume the root is two levels up from scripts/py/func/
    gitignore_path = pathlib.Path(__file__).parents[3] / ".gitignore"

    if not gitignore_path.exists():
        logger.critical("🛑 SECURITY ALERT: Main gitignore:{gitignore_path} file not found at expected path. ABORTING.")
        return False

    # The two mandatory security rules
    required_rules = [
        "config/maps/**/.*",  # Dot-prefixed files/dirs (passwords/keys)
        "config/maps/**/_*"  # Underscore-prefixed files/dirs (unencrypted working area)
    ]

    try:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read().splitlines()

        all_checks_pass = True

        for rule in required_rules:
            # Check if the rule is present (ignoring comments and whitespace)
            is_present = any(
                line.strip() == rule for line in content if not line.strip().startswith('#') and line.strip())

            if not is_present:
                logger.critical(
                    f"🛑 SECURITY ALERT: Required rule '{rule}' is MISSING from .gitignore. "
                    f"ABORTING private map loading. Please add it to the file."
                )
                all_checks_pass = False
            # else:
            #     logger.info(f"✅ Security Check Passed: Rule '{rule}' is present in .gitignore.")

        return all_checks_pass

    except Exception as e:
        logger.error(f"Error reading .gitignore file: {e}")
        return False





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


# def ensure_init_files2(root_dir: Path, logger):
#     """
#     Stellt sicher, dass __init__.py im root_dir und in allen
#     unmittelbaren Unterverzeichnissen (erste Ebene) existiert.
#     __pycache__ wird ignoriert.
#     """
#
#     # Sicherstellen, dass root_dir ein Path-Objekt ist (für Konsistenz)
#     root_dir = Path(root_dir)
#
#     # 1. __init__.py im Hauptverzeichnis (root_dir) erstellen
#     init_file_root = root_dir / "__init__.py"
#     if not init_file_root.exists():
#         try:
#             init_file_root.touch(exist_ok=True)
#             logger.info(f"Created __init__.py in root: {root_dir}")
#         except OSError as e:
#             logger.error(f"Error creating __init__.py in {root_dir}: {e}")
#
#     # 2. Durch die unmittelbaren Kinder (erste Schicht/Ebene) iterieren
#     try:
#         for item in root_dir.iterdir():
#             # Prüfen, ob es ein Verzeichnis ist und ob es NICHT __pycache__ ist
#             if item.is_dir() and item.name != '__pycache__':
#
#                 # Pfad zur __init__.py im Unterverzeichnis
#                 init_file_subdir = item / "__init__.py"
#
#                 if not init_file_subdir.exists():
#                     try:
#                         init_file_subdir.touch(exist_ok=True)
#                         logger.info(f"Created __init__.py in subdirectory: {item}")
#                     except OSError as e:
#                         logger.error(f"Error creating __init__.py in {item}: {e}")
#
#     except FileNotFoundError:
#         logger.error(f"Root directory not found: {root_dir}")
#     except PermissionError as e:
#         logger.error(f"Permission denied accessing directory {root_dir}: {e}")















#
# def ensure_init_files_in_all_folder_full_recursiv(root_dir,logger):
#     for dir_path, _, files in os.walk(root_dir):
#         if dir_path == '__pycache__':
#                 continue
#         if not (root_dir / "__init__.py").exists():
#             (root_dir / "__init__.py").touch(exist_ok=True)
#             logger.info(f"Created __init__.py in {root_dir}")
#
#         for sub_dir in os.listdir(dir_path):
#             sub_dir_path = os.path.join(dir_path, sub_dir)
#             if os.path.isdir(sub_dir_path):
#                 init_file = (Path(sub_dir_path) / "__init__.py")
#                 if not init_file.exists():
#                     try:
#                         init_file.touch(exist_ok=True)
#                         logger.info(f"Created __init__.py in {sub_dir_path}")
#                     except OSError as e:
#                         logger.error(f"Error creating __init__.py in {sub_dir_path}: {e}")
#
