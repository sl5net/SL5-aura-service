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

                relative_path = map_file_path.relative_to(project_root)
                module_name = str(relative_path.with_suffix('')).replace(os.path.sep, '.')

                log_all_map_reloaded = settings.DEV_MODE_all_processing

                # --- START OF COMPLETE MEMORY LEAK FIX & CLEANUP ---
                if module_name in sys.modules:
                    # 1. CLEAR CENTRAL REGISTRY (Breaks references to old ast.* objects)
                    logger.info("🗑️ Calling clear_global_maps to release old function references.")
                    clear_global_maps(logger)

                    # 2. DELETE OLD MODULE (Breaks the global reference in Python's cache)
                    logger.info(f"🗑️ Deleting old module reference for {module_name} from sys.modules.")
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

                except Exception as e:
                    # -------------------------------------------------------
                    # EXCEPTION HANDLER -> PRIVATE MAP CHECK
                    # -------------------------------------------------------

                    # DEBUG: Log that we hit an exception (expected for key files)
                    # logger.info(f"💥 Import Exception for {module_name}: {e}")

                    was_private_map = _handle_private_map_exception(module_name, 
                                                                    map_file_key, 
                                                                    logger)
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
    Checks if a failed module load is actually a private ZIP/Key pattern.
    Unpacks the ZIP (supports standard and Matryoshka/Blob formats) and returns True.
    """
    # 1. Determine the map directory
    map_dir = str(pathlib.Path(map_file_key).parent)

    # 2. Check for the private map pattern in this directory
    key_file = None
    zip_file = None

    try:
        for item in os.listdir(map_dir):
            path_item = os.path.join(map_dir, item)
            # Trigger is a .py file that starts with a dot
            if item.startswith('.') and item.endswith('.py') and os.path.isfile(path_item):
                key_file = path_item

            if item.lower().endswith('.zip') and os.path.isfile(path_item):
                zip_file = path_item
                logger.info(f"zip found: {zip_file}")

        if not (key_file and zip_file):
            return False  # Not a private map pattern

        # --------------------------------------------------------------------------------
        # 3. PREPARATION & SECURITY

        # CRITICAL SECURITY CHECK
        if not _check_gitignore_for_security(logger):
            return False

        logger.info(f"found key_file: {key_file}")


            # Read Password (robust handling for comments)
        password = None
        with open(key_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    # Remove # and whitespace
                    clean = line.lstrip("#").strip()
                    if clean:
                        password = clean
                        break
                elif line:
                    password = line
                    break

        if not password:
            logger.error(f"❌ Key file found but empty or invalid: {key_file}")
            return False

        # Determine Paths
        zip_name_base = pathlib.Path(zip_file).stem
        if zip_name_base.startswith('_'):
            target_maps_dir = os.path.join(map_dir, f"{zip_name_base}")
        else:
            target_maps_dir = os.path.join(map_dir, f"_{zip_name_base}")

        # Check if already unpacked
        if os.path.exists(target_maps_dir):
            return True

        # --------------------------------------------------------------------------------
        # 4. UNPACKING LOGIC (Matryoshka-Support)

        temp_unpack_dir = os.path.join(map_dir, f".__tmp_unpack_{os.getpid()}")
        os.makedirs(temp_unpack_dir, exist_ok=False)

        logger.info(f"🔑 Unpacking '{zip_file}' to TEMP: '{temp_unpack_dir}'.")

        try:
            # A) Outer Unpack (Decryption)
            with zipfile.ZipFile(zip_file, 'r') as outer_zip:
                outer_zip.extractall(temp_unpack_dir, pwd=password.encode('utf-8'))

            # B) Matryoshka Check (Is there a blob inside?)
            unpacked_files = os.listdir(temp_unpack_dir)
            source_dir = temp_unpack_dir  # Default: Flat structure

            if len(unpacked_files) == 1 and unpacked_files[0] == "aura_secure.blob":
                logger.info("🪆 Detected Matryoshka-Container (Nested ZIP). Unpacking inner layer...")
                blob_path = os.path.join(temp_unpack_dir, "aura_secure.blob")
                inner_temp = os.path.join(temp_unpack_dir, "_inner")
                os.makedirs(inner_temp, exist_ok=True)

                # Unpack the blob (unencrypted inner container)
                with zipfile.ZipFile(blob_path, 'r') as inner_zip:
                    inner_zip.extractall(inner_temp)

                # Clean up blob to save space, switch source to inner folder
                os.remove(blob_path)
                source_dir = inner_temp

            # --------------------------------------------------------------------------------
            # 5. NORMALIZATION & MOVE

            # Check for nested single-folder (Zip-Artifacts)
            content = os.listdir(source_dir)
            if len(content) == 1 and os.path.isdir(os.path.join(source_dir, content[0])):
                final_source = os.path.join(source_dir, content[0])
            else:
                final_source = source_dir

            # Create FINAL target directory
            os.makedirs(target_maps_dir, exist_ok=True)

            # Move files
            for item in os.listdir(final_source):
                shutil.move(os.path.join(final_source, item), target_maps_dir)

            logger.info(f"📦 Unpack complete. Files ready in '{target_maps_dir}'.")

        except Exception as e:
            logger.error(f"❌ ZIP/Unpack Error (Wrong Password?): {e}")
            # Cleanup on failure
            if os.path.exists(temp_unpack_dir):
                shutil.rmtree(temp_unpack_dir)
            return False

        # Cleanup Temp Dir on Success
        if os.path.exists(temp_unpack_dir):
            shutil.rmtree(temp_unpack_dir)

        return True

    except Exception as e:
        logger.error(f"❌ General Error in private map handler: {e}")
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
