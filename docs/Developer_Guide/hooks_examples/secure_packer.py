# example: 11.12.'25 22:26 Thu
# config/maps/_privat/secure_packer.py
# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY

import logging
from pathlib import Path
# Import the new library
from scripts.py.func import secure_packer_lib

logger = logging.getLogger(__name__)

def on_folder_change():
    """
    Triggered by map_reloader.py when anything in this folder changes.
    Delegates work to the central library.
    """
    current_dir = Path(__file__).parent

    # Execute the logic located in the public library
    logger.info(f"config/maps/_privat/secure_packer.py:19  current dir: {current_dir}")
    secure_packer_lib.execute_packing_logic(current_dir, logger)
