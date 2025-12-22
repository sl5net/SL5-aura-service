# config/maps/secure_packer.py
# example: 11.12.'25 22:26 Thu
# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY

import logging
from pathlib import Path
from config.dynamic_settings import settings

# Import the new library
from scripts.py.func import secure_packer_lib

logger = logging.getLogger(__name__)

def on_folder_change(current_dir=None):
    """
    Triggered by map_reloader.py when anything in this folder changes.
    Delegates work to the central library.
    """
    if not current_dir:
        current_dir = Path(__file__).parent

    # Execute the logic located in the public library
    if settings.DEV_MODE:
        logger.info(f"📂>📦..{str(current_dir)[-35:]}/secure_packer.py:19")
    secure_packer_lib.execute_packing_logic(current_dir, logger)
