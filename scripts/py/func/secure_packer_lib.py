# scripts/py/func/secure_packer_lib.py:1
import os
#import subprocess
import logging
#import shutil
from pathlib import Path
import pyzipper

from scripts.py.func.password_extract import _extract_password

logger = logging.getLogger(__name__)

def execute(data):
    pass

def execute_packing_logic(current_dir, logger):
    """
    Creates a 'Matryoshka-ZIP' with extensive debug logging.
    """
    # logger.info("==================================================")
    # logger.info("🚀 secure_packer_lib triggered.")

    try:
        # 1. PATH ANALYSIS
        #current_file = Path(__file__)

        # current_dir = current_file.parent
        #current_dir = target_dir

        # parent_dir = current_dir.parent
        parent_dir = current_dir.parent


        #logger.info(f"📍 Script Location: {current_file}")
        # logger.info(f"📂 Directory to pack (Source): {current_dir}")
        # logger.info(f"📂 Parent Directory (Target):  {parent_dir}")

        # 2. NAME CALCULATION
        folder_name = current_dir.name
        # logger.info(f"🔍 Analyzing Folder Name: '{folder_name}'")

        if folder_name.startswith('_'):
            base_name = folder_name[1:]
            # logger.info(f"✂ Removed leading underscore. Base: '{base_name}'")
        else:
            base_name = folder_name
            # logger.warning(f"⚠ Folder name '{folder_name}' does not start with '_'. Using asis.")

        zip_name_outer = base_name + ".zip"
        zip_path_outer = parent_dir / zip_name_outer
        # logger.info(f"🎯 Target ZIP Path: {zip_path_outer}")

        # ... nach: zip_path_outer = parent_dir / zip_name_outer ...

        # --- SMART TIMESTAMP CHECK (DEBUG VERSION) ---
        if zip_path_outer.exists():
            try:
                zip_mtime = zip_path_outer.stat().st_mtime

                latest_source_mtime = 0.0
                newest_file = "None"

                for root, dirs, files in os.walk(current_dir):
                    # 1. EXCLUDE NOISE: Ignore __pycache__ directories
                    if "__pycache__" in dirs:
                        dirs.remove("__pycache__")

                    for file in files:
                        # 2. EXCLUDE NOISE: Ignore hidden files and .pyc
                        if file.startswith('.') or file.endswith('.pyc'):
                            continue

                        file_path = Path(root) / file
                        mtime = file_path.stat().st_mtime

                        if mtime > latest_source_mtime:
                            latest_source_mtime = mtime
                            newest_file = str(file_path)

                # if False:
                #     logger.info(f"⏱️ Timestamp Check:")
                #     logger.info(f"   - ZIP Date:    {zip_mtime}")
                #     logger.info(f"   - Source Date: {latest_source_mtime}")
                #     logger.info(f"   - Newest File: {newest_file}")

                # Check if ZIP is newer or equal (with 1s buffer)
                if zip_mtime >= (latest_source_mtime - 1.0):
                    # logger.info(f"⏭️ ZIP is up-to-date. Skipping repack.")
                    return

                logger.info(f"♻️ Content changed (Source is newer). Repacking...")

            except Exception as e:
                logger.warning(f"⚠️ Timestamp check failed, forcing repack: {e}")
        # ---------------------------------------------



        # 3. KEY FILE SEARCH
        # logger.info("🔎 Searching for .auth_key file...")
        key_file = next(parent_dir.glob(".*.py"), None)

        if not key_file:
            logger.error(f"❌ No key file found in {parent_dir} matching '.*.py'")
            # Listing files to help debug
            files_in_parent = [f.name for f in parent_dir.iterdir()]
            logger.info(f"ℹ Files actually present in parent: {files_in_parent}")
            return

        # logger.info(f"🔑 Key File found: {key_file}")

        # 4. PASSWORD EXTRACTION
        password = _extract_password(key_file,logger)
        if not password:
            logger.error("❌ Password extraction returned None/Empty!")
            return
        # Mask password for logs (show only length)
        pass_len = len(password)
        # logger.info(f"🔐 Password extracted successfully (Length: {pass_len} chars).")
        blob_name = "aura_secure.blob"
        blob_path = parent_dir / blob_name
        zip_me(blob_path, current_dir,password)

        zip_me(zip_path_outer, blob_path,password)
        # config/maps/_privat555/secure_packer.py:72
        os.remove(blob_path)

        # logger.info("🏁 SecurePacker finished.")
    except Exception as e:
        logger.error(f"❌ CRITICAL EXCEPTION in SecurePacker: {e}", exc_info=True)

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

    # logger.info(f"📄 Zip Output: {zip_path_outer}")
