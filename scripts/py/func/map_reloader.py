# scripts/py/func/map_reloader.py
import importlib
import re
import sys
import gc # Added for forced garbage collection
import pathlib
from io import BytesIO
from pathlib import Path
import os
import shutil

import pyzipper
# PyZipper (~20MB):
from config.dynamic_settings import settings
LAST_MODIFIED_TIMES = {}  # noqa: F824

def auto_reload_modified_maps(logger,run_mode_override):
    # scripts/py/func/map_reloader.py:12

    logger.info(f'31: run_mode_override: {run_mode_override}')

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
                continue  # Ignore __init__.py files

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
                    logger.info(f'before run: _trigger_upstream_hooks({map_file_path}, {project_root}, logger) ')
                    _trigger_upstream_hooks(map_file_path, project_root, logger)
                    # --- NEW CODE END ---



                except Exception as e:
                    # -------------------------------------------------------
                    # EXCEPTION HANDLER -> PRIVATE MAP CHECK
                    # -------------------------------------------------------

                    # DEBUG: Log that we hit an exception (expected for key files)
                    logger.info(f"💥 Import Exception for {module_name}: {e}")

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
                logger.info(f"scripts/py/func/map_reloader.py:204 -> zip found: {zip_file}")

        if not (key_file and zip_file):
            return False  # Not a private map pattern

        # --------------------------------------------------------------------------------
        # 3. PREPARATION & SECURITY

        # CRITICAL SECURITY CHECK
        if not _check_gitignore_for_security(logger):
            return False

        logger.info(f"found key_file: {key_file}")

        pw_bytes = _extract_password(key_file, logger)
        if not pw_bytes:
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
            logger.info('scripts/py/func/map_reloader.py:244: already unpacked -> return True')
            return True

        # 4. UNPACKING LOGIC (Matryoshka-Support)

        temp_unpack_dir = os.path.join(map_dir, f".__tmp_unpack_{os.getpid()}")
        os.makedirs(temp_unpack_dir, exist_ok=False)

        logger.info(f"🔑 Unpacking '{zip_file}' to TEMP: '{temp_unpack_dir}'.")
        try:
            # A) Outer Unpack (Decryption)
            with pyzipper.AESZipFile(zip_file, 'r') as outer_zip:
                outer_zip.setpassword(pw_bytes)
                outer_zip.extractall(temp_unpack_dir)

            # B) Matryoshka Check (Is there a blob inside?)
            unpacked_files = os.listdir(temp_unpack_dir)
            source_dir = temp_unpack_dir  # Default: Flat structure

            if len(unpacked_files) == 1 and unpacked_files[0] == "aura_secure.blob":
                logger.info("🔎 Detected Matryoshka-Container (Nested ZIP). Unpacking inner layer...")
                blob_path = os.path.join(temp_unpack_dir, "aura_secure.blob")
                inner_temp = os.path.join(temp_unpack_dir, "_inner")
                os.makedirs(inner_temp, exist_ok=True)

                # Read the blob bytes and open inner zip from memory (works for encrypted inner zips too)
                with open(blob_path, 'rb') as f:
                    blob_bytes = f.read()

                with pyzipper.AESZipFile(BytesIO(blob_bytes), 'r') as inner_zip:
                    inner_zip.setpassword(pw_bytes)
                    inner_zip.extractall(inner_temp)

                os.remove(blob_path)
                source_dir = inner_temp

            #scripts/py/func/map_reloader.py:261
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

    except Exception as e:
        logger.error(f"❌ ZIP/Unpack Error (Wrong Password?): {e}")

    return True


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

    # scripts/py/func/map_reloader.py:319
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

from typing import Optional
def _extract_password(key_path: str, logger, encoding: str = "utf-8") -> Optional[bytes]:
    """
    Read key file and return password as bytes (or None on failure).

    Heuristics:
    - skip empty lines
    - prefer comment lines starting with '#' (take text after '#')
    - accept common assignment patterns (password=..., key: ..., secret = "...")
    - strip surrounding quotes and whitespace, remove BOM and CR/LF
    - return as bytes using given encoding
    """
    logger.info(f"📖scripts/py/func/map_reloader.py:453: Reading key file: {key_path}")
    try:
        with open(key_path, "r", encoding=encoding, errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        logger.error(f"❌ Error reading key file: {e}")
        return None

    # helper to normalise candidate and return bytes if valid
    def normalise(s: str) -> Optional[bytes]:
        if not s:
            return None
        # remove BOM if present
        s = s.lstrip("\ufeff").strip()
        # strip surrounding single/double quotes
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        # remove inline comments after value (e.g. secret # comment)
        s = re.split(r"\s+#", s, 1)[0].strip()
        if not s:
            return None
        try:
            b = s.encode(encoding)
            return b
        except Exception as e:
            logger.warning(f"⚠ Could not encode password candidate: {e}")
            return None

    # patterns to detect assignment-like lines
    assign_re = re.compile(r'^(?:password|pass|secret|key)\s*[:=]\s*(.+)$', re.IGNORECASE)

    # 1) scan for explicit assignment lines (high priority)
    for i, line in enumerate(lines):
        raw = line.rstrip("\n\r")
        m = assign_re.match(raw.strip())
        if m:
            candidate = m.group(1).strip()
            pw = normalise(candidate)
            if pw:
                logger.info("✓ Found password via assignment pattern.")
                return pw

    # 2) scan for comment lines that contain a candidate (lines starting with '#')
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            candidate = stripped.lstrip("#").strip()
            pw = normalise(candidate)
            if pw:
                logger.info("scripts/py/func/map_reloader.py:491 ✓ Found password in comment.")
                return pw

    # 3) fallback: first non-empty, non-comment line
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            pw = normalise(stripped)
            if pw:
                logger.info("✓ Found password in plaintext line.")
                return pw

    logger.warning("⚠ No valid password pattern found in key file.")
    return None


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
    logger.info(f'scripts/py/func/map_reloader.py:_trigger_upstream_hooks:518')
    stop_dir = project_root / "config" / "maps"
    logger.info(f'scripts/py/func/map_reloader.py:_trigger_upstream_hooks:521')
    current_dir = start_path.parent
    logger.info(f'scripts/py/func/map_reloader.py:_trigger_upstream_hooks:523 -> current_dir:{current_dir}')

    # Safety check: verify we are inside config/maps
    try:
        current_dir.relative_to(stop_dir)
    except ValueError as e:
        logger.info(f'x scripts/py/func/map_reloader.py:_trigger_upstream_hooks:533 -> {e}')
        return  # Outside of scope

    # 2. Traverse Upwards
    while stop_dir in current_dir.parents or current_dir == stop_dir:
        logger.info(f"🔍 Scanning for lifecycle hooks in: {current_dir}")

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
                    logger.info(f"🔗 Triggering upstream hook: {module_name}.on_folder_change()")
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
