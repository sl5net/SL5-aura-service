# scripts/py/func/private_map_ex.py _private_map_unpack(map_file_key: str, logger) -> bool:
import os
import pathlib
import shutil
import sys
from zipfile import ZipFile
import pyzipper
# PyZipper (~20MB):
from io import BytesIO


from scripts.py.func.password_extract import _extract_password
def _private_map_unpack(map_file_key: str, logger) -> bool:
    """
    Checks if a failed module load is actually a private ZIP/Key pattern.
    Unpacks the ZIP (supports standard and Matryoshka/Blob formats) and returns True.
    """

    log_everything = False

    # 1. Determine the map directory
    map_dir = str(pathlib.Path(map_file_key).parent)

    file_key_name = pathlib.Path(map_file_key).name

    if log_everything:
        logger.info(f'22: map_dir=📂...{map_dir[-30:]} file_key_name:📜{file_key_name} ')


    # 2. Check for the private map pattern in this directory
    # startswith('.') and endswith('.py')
    key_file = map_file_key

    pw = None
    if file_key_name == '.nopassword.py':
        if log_everything:
            logger.info(f'{file_key_name} --> normal extract')
        pw = None
    else:
        pw = _extract_password(key_file, logger)
        if not pw:
            # logger.info("No valid passwords found or recalled to early in any key file.")
            return False

    # CRITICAL SECURITY CHECK
    if not _check_gitignore_for_security(logger):
        return False
    zip_file = None
    try:
        # try unzip all zips with this
        for item in os.listdir(map_dir):
            path_item = os.path.join(map_dir, item)

            if item.lower().endswith('.zip') and os.path.isfile(path_item):
                zip_file = path_item
                # logger.info(f"scripts/py/func/map_reloader.py:244: {map_file_key} > zip found: {zip_file}")
            if not zip_file:
                continue

            zip_name_base = pathlib.Path(zip_file).stem
            if zip_name_base.startswith('_'):
                target_maps_dir = os.path.join(map_dir, f"{zip_name_base}")
            else:
                target_maps_dir = os.path.join(map_dir, f"_{zip_name_base}")

            # Check if already unpacked
            if os.path.exists(target_maps_dir):
                # logger.info(f'scripts/py/func/map_reloader.py:244: {map_file_key} > {item} || {target_maps_dir} already unpacked -> return True')
                continue

            # UNPACKING LOGIC (Matryoshka-Support)
            temp_unpack_dir = os.path.join(map_dir, f".__tmp_unpack_{os.getpid()}")
            os.makedirs(temp_unpack_dir, exist_ok=False)

            # logger.info(f"🔑 Unpacking '{zip_file}' to TEMP: '{temp_unpack_dir}'.")
            try:
                # A) Outer Unpack (Decryption)

                if file_key_name == '.nopassword.py':
                    logger.info(f'TODO normal extract {file_key_name} -> sys.exit(0)')
                    logger.info(f'TODO normal extract {file_key_name} -> sys.exit(0)')
                    logger.info(f'TODO normal extract {file_key_name} -> sys.exit(0)')
                    logger.info(f'TODO normal extract {file_key_name} -> sys.exit(0)')
                    logger.info(f'TODO normal extract {file_key_name} -> sys.exit(0)')
                    logger.info(f'TODO normal extract {file_key_name} -> sys.exit(0)')

                    with ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(target_maps_dir)


                    sys.exit(0)
                    continue

                with pyzipper.AESZipFile(zip_file, 'r') as outer_zip:
                    outer_zip.setpassword(pw)
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
                        inner_zip.setpassword(pw)
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
                for item2 in os.listdir(final_source):
                    shutil.move(os.path.join(final_source, item2), target_maps_dir)

                logger.info(f"📦 Unpack complete. Files ready in '{target_maps_dir}'.")


            except Exception as e:
                logger.error(f"❌ ZIP/Unpack Error (Wrong Password?): {e}")
                # Cleanup on failure
                if os.path.exists(temp_unpack_dir):
                    shutil.rmtree(temp_unpack_dir)
                continue

            # Cleanup Temp Dir on Success
            if os.path.exists(temp_unpack_dir):
                shutil.rmtree(temp_unpack_dir)

    except Exception as e:
        logger.error(f"❌ ZIP/Unpack Error: {e}")

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
