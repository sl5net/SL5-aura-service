# scripts/py/func/secure_packer_lib.py
import os
import logging
import zipfile
from pathlib import Path
import pyzipper

from scripts.py.func.password_extract import _extract_password

logger = logging.getLogger(__name__)

def execute(data):
    pass

# scripts/py/func/secure_packer_lib.py:18
def execute_packing_logic(current_dir, logger):
    log_everything = True
    if log_everything:
        logger.info(f"🚀 secure_packer_lib triggered for: ...{str(current_dir)[-30:]}")

    try:
        current_dir = Path(current_dir)
        parent_dir = current_dir.parent

        # 1. Namen berechnen
        folder_name = current_dir.name
        base_name = folder_name[1:] if folder_name.startswith('_') else folder_name
        zip_path_outer = parent_dir / f"{base_name}.zip"

        # 2. Timestamp Check (Skip wenn ZIP aktuell)
        if zip_path_outer.exists():
            zip_mtime = zip_path_outer.stat().st_mtime
            latest_mtime = 0.0
            for root, _, files in os.walk(current_dir):
                for f in files:
                    if f.startswith('.') or f.endswith('.pyc') or "__pycache__" in root:
                        continue
                    m = (Path(root) / f).stat().st_mtime
                    if m > latest_mtime: latest_mtime = m

            if zip_mtime >= (latest_mtime - 1.0):
                if log_everything:
                    logger.info(f"⏭️ ZIP up-to-date: {zip_path_outer.name}")
                return

        # 3. Key-Datei Suche (FIX: Sucht jetzt auch versteckte Dateien)
        project_root = Path(__file__).resolve().parents[3]  # scripts/py/func/lib.py -> parents[3] is root
        stop_dir = project_root / "config"

        key_file = None
        search_dir = current_dir.parent  # Starte Suche im Parent des _Ordners

        while stop_dir in search_dir.parents or search_dir == stop_dir:
            if log_everything:
                logger.info(f"🔍 Searching key in {search_dir.name}")

            for file_path in search_dir.glob(".*.py"):  # Sucht explizit nach .pass.py etc.
                if log_everything:
                    logger.info(f"🔑 Key-File Kandidat gefunden: {file_path.name}")
                key_file = file_path
                # stop_search_key_file_is_found_year = True
                break


            if search_dir == stop_dir: break
            search_dir = search_dir.parent

        if not key_file:
            if log_everything:
                logger.info(f"ℹ️ No key found for {folder_name}, skipping.")
            return

        # 4. ZIP Vorgang
        logger.info(f"🔐 Packing {folder_name} using key: {key_file.name}")

        if key_file.name == '.nopassword.py':
            zip_me_nopassword(zip_path_outer, current_dir)
        else:
            password = _extract_password(key_file, logger)
            if password:
                blob_path = parent_dir / "aura_secure.blob"
                zip_me(blob_path, current_dir, password)
                zip_me(zip_path_outer, blob_path, password)
                if blob_path.exists(): os.remove(blob_path)
            else:
                logger.error("❌ Could not extract password!")

        # 5. Timestamp-Notiz erstellen
        import time
        ts_content = f"#!/usr/bin/env python3\nzip_created_at = '{time.strftime('%Y-%m-%d %H:%M:%S')}'"
        with open(f'{zip_path_outer}.py', 'w') as f:
            f.write(ts_content)

    except Exception as e:
        logger.error(f"❌ CRITICAL in secure_packer_lib: {e}", exc_info=True)


def zip_me(zip_path_outer, current_dir_or_single_file, password):
    pw = password.encode("utf-8") if isinstance(password, str) else password
    current = str(current_dir_or_single_file)

    with pyzipper.AESZipFile(zip_path_outer, 'w',
                             compression=pyzipper.ZIP_DEFLATED,
                             encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(pw)

        if os.path.isfile(current):
            arc_name = os.path.basename(current)
            zf.write(current, arc_name)
        else:
            base_len = len(current.rstrip(os.sep)) + 1
            for root, _, files in os.walk(current):
                for fn in files:
                    full = os.path.join(root, fn)
                    arc_name = full[base_len:]
                    zf.write(full, arc_name)

    # logger.info(f"📄 📦 Zip Output: {zip_path_outer}")

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

            for root, _, files in os.walk(target_path):
                for fn in files:
                    if '__init__.py' in fn:
                        continue
                    full_path = os.path.join(root, fn)
                    # relpath calculates the correct relative path automatically
                    arc_name = os.path.relpath(full_path, start=parent_dir)
                    zf.write(full_path, arc_name)

    logger.info(f"📄 📦 Zip Output: {zip_path_outer}")

