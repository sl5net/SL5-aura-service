import logging
import json
import os
import sys
import importlib.util
from pathlib import Path

# --- Configuration ---
CURRENT_DIR = Path(__file__).parent
JSON_DB_PATH = CURRENT_DIR / "zip_registry.json"

# 0=Dateiname, 1=de-DE, 2=zip_all, ... 7=STT (Root)
project_dir = Path(__file__).parents[6]
SCAN_ROOT = project_dir / "config" / "maps"

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# --- Import Helper for secure_packer_lib ---
def get_packer_lib():
    """Dynamically imports the secure_packer_lib module."""
    lib_path = Path("/home/seeh/projects/py/STT/scripts/py/func/secure_packer_lib.py")

    if not lib_path.exists():
        logger.error(f"❌ secure_packer_lib not found at {lib_path}")
        return None

    spec = importlib.util.spec_from_file_location("secure_packer_lib", lib_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["secure_packer_lib"] = module
    spec.loader.exec_module(module)
    return module

# --- JSON Helpers ---
def load_registry():
    if not JSON_DB_PATH.exists():
        return []
    try:
        with open(JSON_DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("watched_folders", [])
    except Exception:
        return []

def save_registry(folder_list):
    try:
        with open(JSON_DB_PATH, 'w', encoding='utf-8') as f:
            json.dump({"watched_folders": list(set(folder_list))}, f, indent=4)
        logger.info(f"💾 Registry saved with {len(folder_list)} entries.")
    except Exception as e:
        logger.error(f"❌ Failed to save JSON: {e}")

# --- TIMESTAMPS LOGIC ---
def _needs_update(source_folder: Path, zip_file: Path) -> bool:
    """
    Returns True if the folder content is newer than the zip file.
    """
    if not zip_file.exists():
        # Zip doesn't exist yet -> Update needed
        return True

    zip_time = zip_file.stat().st_mtime

    # Check modification time of all files inside the folder
    # This covers PDFs, TXTs, scripts, etc.
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root) / file
            # If any file is newer than the zip archive -> Update needed
            if file_path.stat().st_mtime > zip_time:
                # logger.debug(f"File {file} is newer than zip.")
                return True

    return False

# --- 1. THE MANUAL PART (Scanning) ---
def scan_and_register_folders():
    """
    MANUAL ONLY: Scans the file system for folders starting with '_'.
    Updates the JSON registry.
    """
    logger.info(f"🕵️ Scanning for zip-targets in: {SCAN_ROOT}")
    found_folders = []

    for root, dirs, files in os.walk(SCAN_ROOT):
        path_obj = Path(root)

        # Ignoriere versteckte Systemordner
        if path_obj.name.startswith('.') or '__pycache__' in path_obj.parts:
            continue

        # Prüfen ob der Ordner mit '_' beginnt (aber nicht '__')
        if path_obj.name.startswith('_') and not path_obj.name.startswith('__'):
            found_folders.append(str(path_obj.resolve()))

    save_registry(found_folders)
    return len(found_folders)

# --- 2. THE AUTOMATIC PART (Updating) ---
def update_existing_zips():
    """
    AUTOMATIC: Reads JSON, checks timestamps, and calls the packer ONLY if needed.
    """
    folders = load_registry()
    if not folders:
        return

    packer_lib = get_packer_lib()
    if not packer_lib:
        return

    updates_count = 0

    for folder_str in folders:
        folder_path = Path(folder_str)

        if not folder_path.exists():
            continue

        # Determine Target Zip Name
        # Rule: Folder "_t1" -> Zip "t1.zip" (Remove leading underscore)
        zip_name = folder_path.name.lstrip('_') + ".zip"
        zip_target = folder_path.parent / zip_name

        # CHECK: Do we really need to zip?
        if _needs_update(folder_path, zip_target):
            logger.info(f"♻️ Content changed. Zipping: {folder_path.name} -> {zip_name}")
            try:
                # Call the external lib to do the actual work
                packer_lib.execute_packing_logic(folder_path, logger)
                updates_count += 1
            except Exception as e:
                logger.error(f"⚠️ Error packing {folder_path.name}: {e}")
        # else:
            # logger.debug(f"Skipping {folder_path.name}, zip is up to date.")

    if updates_count > 0:
        logger.info(f"✅ Updated {updates_count} zip archives.")

# --- Hooks & Commands ---

def on_reload():
    """
    AUTOMATIC TRIGGER:
    Runs every time the map system reloads.
    Checks timestamps for all known folders in JSON.
    """
    try:
        update_existing_zips()
    except Exception as e:
        logger.error(f"🔥 Error in zip.py on_reload: {e}")


def execute(match_data):
    """
    MANUAL VOICE TRIGGER:
    Scans the disk for NEW folders, then checks all zips.
    """
    logger.info("🎤 Voice Command: Scanning system for new '_folders'...")

    count = scan_and_register_folders()
    update_existing_zips()

    return f"Scan complete. Found {count} targets. Zips updated."
