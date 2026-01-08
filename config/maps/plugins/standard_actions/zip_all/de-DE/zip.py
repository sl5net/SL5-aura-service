# config/maps/plugins/standard_actions/zip_all/de-DE/zip.py
import logging
import json
import os
import sys
import shutil
import importlib.util
from pathlib import Path

# --- Configuration ---
CURRENT_DIR = Path(__file__).parent
JSON_DB_PATH = CURRENT_DIR / "zip_registry.json"
# Geht 7 Ebenen hoch zum Projekt-Root -> config -> maps
SCAN_ROOT = Path(__file__).resolve().parents[6] / "config" / "maps"

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# --- DYNAMIC IMPORTS ---

def get_packer_lib():
    """Import secure_packer_lib for PACKING."""
    lib_path = SCAN_ROOT.parents[1] / "scripts" / "py" / "func" / "secure_packer_lib.py"
    if not lib_path.exists():
        logger.error(f"❌ secure_packer_lib not found at {lib_path}")
        return None
    spec = importlib.util.spec_from_file_location("secure_packer_lib", lib_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["secure_packer_lib"] = module
    spec.loader.exec_module(module)
    return module

def get_unpacker_lib():
    """Import private_map_ex for UNPACKING."""
    lib_path = SCAN_ROOT.parents[1]  / "scripts" / "py" / "func" / "private_map_ex.py"
    if not lib_path.exists():
        logger.error(f"❌ private_map_ex not found at {lib_path}")
        return None
    spec = importlib.util.spec_from_file_location("private_map_ex", lib_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["private_map_ex"] = module
    spec.loader.exec_module(module)
    return module

# --- JSON Helpers ---
def load_registry():
    if not JSON_DB_PATH.exists(): return []
    try:
        with open(JSON_DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("watched_folders", [])
    except Exception as e:
        print(f"54:{e}")
        return []

def save_registry(folder_list):
    try:
        with open(JSON_DB_PATH, 'w', encoding='utf-8') as f:
            json.dump({"watched_folders": list(set(folder_list))}, f, indent=4)
    except Exception as e: logger.error(f"❌ Failed to save JSON: {e}")

# --- TIMESTAMPS / SEARCH LOGIC ---

from enum import Enum

class PackingStatus(Enum):
    NOT_NEEDED = 0
    CONTENT_CHANGED = 1
    ZIP_MISSING = 2

def _needs_packing(source_folder: Path, zip_file: Path) -> PackingStatus:
    """Returns the specific reason why packing is needed or NOT_NEEDED."""
    if not zip_file.exists():
        return PackingStatus.ZIP_MISSING

    zip_time = zip_file.stat().st_mtime

    grace_period = 1.0

    for root, dirs, files in os.walk(source_folder):
        if "__pycache__" in root:
            continue

        for file in files:
            if file.startswith('.') or file.endswith('.pyc') or file.endswith('~'):
                continue

            file_path = Path(root) / file
            file_time = file_path.stat().st_mtime

            if file_time > (zip_time + grace_period):
                # logger.info(f"File {file} is newer than ZIP. File: {file_time}, Zip: {zip_time}")
                return PackingStatus.CONTENT_CHANGED

    return PackingStatus.NOT_NEEDED

def _needs_unpacking(target_folder: Path, zip_file: Path) -> bool:
    """True if Zip is NEWER than Folder (or Folder missing)."""
    if not zip_file.exists(): return False
    if not target_folder.exists(): return True
    # Buffer of 2 seconds for filesystem precisions
    return zip_file.stat().st_mtime > (target_folder.stat().st_mtime + 2)

def find_password_file(start_dir: Path) -> Path:
    """
    Search upwards for a file starting with '.' (the key/password).
    Stops at 'config/maps'.
    """
    current = start_dir
    limit = SCAN_ROOT
    i = 0
    while True:
        i += 1
        logger.info(f'i={i}   standard_actions/zip_all/de-DE/zip.py:113')
        if current.exists():
            for item in current.iterdir():
                if item.is_file() and item.name.startswith('.'):
                    # Filter out system files
                    if item.name in ['.DS_Store', '.gitignore', '.gitkeep']:
                        continue
                    return item

        if current == limit: break
        if current.parent == current: break
        current = current.parent

    return None

# --- WORKFLOWS ---

def scan_and_register_folders():
    """MANUAL: Scans disk for '_folders', updates JSON."""
    logger.info(f"🕵️ Scanning for zip-targets in: {SCAN_ROOT}")
    found = []
    for root, dirs, files in os.walk(SCAN_ROOT):
        path_obj = Path(root)
        if path_obj.name.startswith('.') or '__pycache__' in path_obj.parts: continue

        if path_obj.name.startswith('_') and not path_obj.name.startswith('__'):
            found.append(str(path_obj.resolve()))

    save_registry(found)
    return len(found)

def check_and_unpack_zips():
    """
    Checks Registry. If Zip > Folder:
    1. Find key file (upwards).
    2. Copy key file to zip directory (if not already there).
    3. Run existing unpacker.
    4. Delete temporary key copy.
    """
    folders = load_registry()
    if not folders: return

    unpacker_module = get_unpacker_lib()
    if not unpacker_module: return

    for folder_str in folders:
        folder_path = Path(folder_str)
        # _t1 -> t1.zip (Sibling)
        zip_name = folder_path.name.lstrip('_') + ".zip"
        zip_dir = folder_path.parent
        zip_path = zip_dir / zip_name

        if _needs_unpacking(folder_path, zip_path):
            logger.info(f"🔓 Update available for {folder_path.name}...")

            # 1. Find the key (somewhere up the tree)
            found_pw_file = find_password_file(folder_path)

            if found_pw_file:
                # 2. Determine local path for the key (next to zip)
                local_key_path = zip_dir / found_pw_file.name
                created_temp_copy = False

                try:
                    # If key is further up, copy it down temporarily
                    if found_pw_file.parent.resolve() != zip_dir.resolve():
                        logger.info(f"   🔑 Copying temp key to: {local_key_path.name}")
                        shutil.copy2(found_pw_file, local_key_path)
                        created_temp_copy = True

                    # 3. Call existing unpacker with the LOCAL key path
                    unpacker_module._private_map_unpack(str(local_key_path), logger)

                    # Touch folder to update mtime (prevent loop)
                    if folder_path.exists():
                        os.utime(folder_path, None)

                except Exception as e:
                    logger.error(f"❌ Failed to unpack {zip_path.name}: {e}")

                finally:
                    # 4. Cleanup: Remove the copied key
                    if created_temp_copy and local_key_path.exists():
                        try:
                            local_key_path.unlink()
                            # logger.debug("🧹 Removed temp key file.")
                        except Exception as cleanup_err:
                            logger.warning(f"⚠️ Could not remove temp key {local_key_path}: {cleanup_err}")

            else:
                logger.warning(f"⚠️ No password file found for {folder_path.name}. Cannot unpack.")

def check_and_pack_zips():
    """Checks Registry. If Folder > Zip, calls secure_packer_lib."""
    folders = load_registry()
    if not folders: return

    packer_lib = get_packer_lib()
    if not packer_lib: return

    for folder_str in folders:
        folder_path = Path(folder_str)
        if not folder_path.exists(): continue

        zip_name = folder_path.name.lstrip('_') + ".zip"
        zip_target = folder_path.parent / zip_name

        if (_needs_packing(folder_path, zip_target) == PackingStatus.CONTENT_CHANGED
                or _needs_unpacking(folder_path, zip_target) == PackingStatus.ZIP_MISSING):
            if _needs_packing(folder_path, zip_target) == PackingStatus.CONTENT_CHANGED:
                logger.info(f"♻️ Content changed. 📦 Zipping: ...{str(folder_path)[-30:]}")
                # missing a zip has maybe good reasons
            try:
                packer_lib.execute_packing_logic(folder_path, logger)
            except Exception as e:
                logger.error(f"⚠️ Error packing {str(folder_path)[-30:]}: {e}")

# --- HOOKS ---

def on_reload():
    """Runs automatically on every reload."""
    try:
        check_and_unpack_zips()
        check_and_pack_zips()
    except Exception as e:
        # STT/config/maps/plugins/standard_actions/zip_all/de-DE/zip.py:236
        logger.error(f"🔥 Error in zip_all/de-DE/zip.py:236 on_reload: {e}")
        # sys.exit(1)
        return f"🔥 Error in zip_all/de-DE/zip.py:236 on_reload: {e}"
        # 07:40:03,498 - ERROR    - 🔥 Error in zip_all/de-DE/zip.py:236 on_reload: attempted relative import with no known parent package

def execute(match_data):
    """Manual Voice Command."""
    logger.info("🎤 Voice Command: Full Scan & Sync...")

    count = scan_and_register_folders()

    check_and_unpack_zips()
    check_and_pack_zips()

    return f"Scan complete. {count} targets synced."

