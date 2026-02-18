# config/maps/secure_packer.py
import logging
from pathlib import Path
from scripts.py.func.config.dynamic_settings import DynamicSettings

# may read: https://github.com/sl5net/SL5-aura-service/tree/master/docs/Feature_Spotlight/zip

settings = DynamicSettings()
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
    if settings.DEV_MODE and (settings.DEV_MODE_all_processing or settings.DEV_MODE_zip_processing):
        logger.info(f"📂>📦..{str(current_dir)[-35:]} |||| {__file__} :19")
    secure_packer_lib.execute_packing_logic(current_dir, logger)
