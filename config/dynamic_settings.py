# config/dynamic_settings.py
import collections.abc # Corrected import to collections.abc
import importlib
import sys
import os
from datetime import time
from pathlib import Path
from threading import RLock
from config import settings
from config.settings_local import DEV_MODE
# Get a logger instance instead of direct print statements for better control
import logging

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_ROOT / "log/dynamic_settings.log"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Clear any pre-existing handlers to prevent duplicates.
if len(logger.handlers) > 0:
    logger.handlers.clear()

# Create a shared formatter with the custom formatTime function.
def formatTime(record, datefmt=None):
    time_str = time.strftime("%H:%M:%S")
    milliseconds = int((record.created - int(record.created)) * 1000)
    ms_str = f",{milliseconds:03d}"
    return time_str + ms_str

log_formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
log_formatter.formatTime = formatTime

# Create, configure, and add the File Handler.
file_handler = logging.FileHandler(f'{PROJECT_ROOT}/log/dynamic_settings.log', mode='w')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

logger.info(f"👀 dynamic_settings.py: DEV_MODE={DEV_MODE}, settings.DEV_MODE = {settings.DEV_MODE}")


class DynamicSettings:
    _instance = None
    _lock = RLock()

    _last_modified_time = 0

    _settings_module = None

    _settings_local_module = None

    _last_base_modified_time = None
    _last_local_modified_time = None

    _settings_file_path = None
    _settings_local_file_path = None

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DynamicSettings, cls).__new__(cls)
                logger.info(f"👀 dynamic_settings.py: DEV_MODE={DEV_MODE}, settings.DEV_MODE = {settings.DEV_MODE}")

                if settings.DEV_MODE:
                    print("👀 DEBUG: DynamicSettings.__new__ called, initializing instance.")
                cls._instance._init_settings()
        return cls._instance

    def _init_settings(self):
        self._settings_file_path = os.path.join(
            os.path.dirname(__file__), "settings.py"
        )
        self._settings_local_file_path = os.path.join(
            os.path.dirname(__file__), "settings_local.py"
        )

        self._last_base_modified_time = os.path.getmtime(self._settings_file_path)
        self._last_local_modified_time = os.path.getmtime(self._settings_local_file_path)

        logger.info(f"👀 dynamic_settings.py: settings.DEV_MODE = {settings.DEV_MODE}")

        if settings.DEV_MODE:
            print(f"👀 DEBUG: DynamicSettings._init_settings called. Base settings file: {self._settings_file_path}")
            print(f"👀 DEBUG: DynamicSettings._init_settings called. Local settings file: {self._settings_local_file_path}")
            logger.info(f"👀 DEBUG: DynamicSettings._init_settings called. Base settings file: {self._settings_file_path}")
        self.reload_settings(force=False)

    def reload_settings(self, force=False):
        # config/dynamic_settings.py:44
        logger.info(f"👀 dynamic_settings.py:reload_settings():44 DEV_MODE={DEV_MODE}, settings.DEV_MODE = {settings.DEV_MODE}")
        print(f"👀 dynamic_settings.py:reload_settings():44 DEV_MODE={DEV_MODE}, settings.DEV_MODE = {settings.DEV_MODE}")


        if settings.DEV_MODE:
            print("👀 DEBUG: reload_settings called.")
        with self._lock:
            if settings.DEV_MODE:
                print("👀 DEBUG: Lock acquired for settings reload.")

            current_base_modified_time = os.path.getmtime(self._settings_file_path) if os.path.exists(
                self._settings_file_path) else 0
            current_local_modified_time = 0
            if self._settings_local_file_path and os.path.exists(self._settings_local_file_path):
                current_local_modified_time = os.path.getmtime(self._settings_local_file_path)

            any_file_modified = (
                    current_base_modified_time > self._last_base_modified_time or
                    current_local_modified_time > self._last_local_modified_time
            )
            if force or self._settings_module is None or any_file_modified:

                if settings.DEV_MODE:

                    logger.info(
                        f"👀 Triggering full settings reload. Reasons: force={force}, _settings_module is None={self._settings_module is None}, any_file_modified={any_file_modified}")
                    logger.info(
                        f"👀【┘】⌚ ⏳ self._settings_file_path: {self._settings_file_path} | self._settings_local_file_path={self._settings_local_file_path} | any_file_modified={any_file_modified}")
                    logger.info(
                        f"👀【┘】⌚ ⏳ current_base_modified_time: {current_base_modified_time} | current_local_modified_time: {current_local_modified_time}")
                    logger.info(
                        f"👀【┘】⌚ ⏳ _last_base_modified_time: {self._last_base_modified_time} | _last_local_modified_time: {self._last_local_modified_time}")
                self._last_base_modified_time = current_base_modified_time
                self._last_local_modified_time = current_local_modified_time



                # --- Reloading base settings (config.settings) ---
                if 'config.settings' in sys.modules:
                    if settings.DEV_MODE:
                        print("👀 DEBUG: Calling importlib.reload(sys.modules['config.settings'])")
                    self._settings_module = importlib.reload(sys.modules['config.settings'])
                else:
                    if settings.DEV_MODE:
                        print("👀 DEBUG: Calling importlib.import_module('config.settings')")
                    self._settings_module = importlib.import_module('config.settings')
                if settings.DEV_MODE:
                    print("👀 DEBUG: Base settings loaded.")

                # --- Reloading local settings (config.settings_local) ---
                try:
                    if os.path.exists(self._settings_local_file_path):
                        if 'config.settings_local' in sys.modules:
                            if settings.DEV_MODE:
                                print("👀 DEBUG: Calling importlib.reload(sys.modules['config.settings_local'])")
                            self._settings_local_module = importlib.reload(sys.modules['config.settings_local'])
                        else:
                            if settings.DEV_MODE:
                                print("👀 DEBUG: Calling importlib.import_module('config.settings_local')")
                            self._settings_local_module = importlib.import_module('config.settings_local')
                        if settings.DEV_MODE:
                            print("👀 DEBUG: Local settings loaded.")
                    else:
                        print("👀 INFO: config.settings_local.py does not exist. Skipping local settings load.")
                        self._settings_local_module = None
                except ModuleNotFoundError:
                    print("👀 WARNING: config.settings_local module not found. This might indicate a path issue or missing file.")
                    self._settings_local_module = None
                except Exception as e:
                    print(f"👀 CRITICAL ERROR: Exception during config.settings_local import/reload: {e}")
                    import traceback
                    traceback.print_exc()
                    raise

                if settings.DEV_MODE:
                    print("👀 DEBUG: --- Merging settings ---")
                # Clear existing attributes to ensure a clean merge
                for attr in list(self.__dict__.keys()):
                    # IMPORTANT: Do not delete 'settings' itself or internal attributes like '_instance', '_lock', etc.
                    # Ensure that we only delete dynamically added configuration attributes.
                    # A robust way might be to keep track of which attributes were added,
                    # but for now, checking for standard internal attributes should be sufficient.
                    if not attr.startswith('_') and attr not in ['settings', '_settings_module', '_settings_local_module']:
                        delattr(self, attr)

                # Apply base settings
                if self._settings_module:
                    for attr in dir(self._settings_module):
                        if not attr.startswith('__'):
                            value = getattr(self._settings_module, attr)
                            setattr(self, attr, value)
                    if settings.DEV_MODE:
                        print("👀 DEBUG: Base settings attributes applied to DynamicSettings instance.")

                # Apply/Merge local settings
                if self._settings_local_module:
                    for attr in dir(self._settings_local_module):
                        if not attr.startswith('__'):
                            local_value = getattr(self._settings_local_module, attr)


                        # --- START MODIFICATION ---
                            # Special handling for PRELOAD_MODELS: always override
                            if attr == "PRELOAD_MODELS":
                                setattr(self, attr, local_value)
                                if settings.DEV_MODE:
                                    print(f"👀 DEBUG: Overrode PRELOAD_MODELS with local value: {local_value}")
                            # --- END MODIFICATION ---
                            elif hasattr(self, attr) and isinstance(getattr(self, attr), collections.abc.MutableMapping) and isinstance(local_value, collections.abc.MutableMapping):
                                merged_dict = getattr(self, attr)
                                merged_dict.update(local_value)
                                setattr(self, attr, merged_dict)
                                if settings.DEV_MODE:
                                    print(f"👀 DEBUG: Merged dictionary setting '{attr}': {getattr(self, attr)}")
                            elif hasattr(self, attr) and isinstance(getattr(self, attr), collections.abc.MutableSequence) and not isinstance(getattr(self, attr), (str, bytes)) and isinstance(local_value, collections.abc.MutableSequence) and not isinstance(local_value, (str, bytes)):
                                merged_list = getattr(self, attr)
                                # Only append items if they are not already in the list
                                for item in local_value:
                                    if item not in merged_list:
                                        merged_list.append(item)
                                setattr(self, attr, merged_list)
                                if settings.DEV_MODE:
                                    print(f"👀 DEBUG: Merged list setting '{attr}': {getattr(self, attr)}")
                            else:
                                # Default: override with local value
                                setattr(self, attr, local_value)
                                if settings.DEV_MODE:
                                    print(f"👀 DEBUG: Overrode setting '{attr}' with local value: {local_value}")
                                    print("👀 DEBUG: Local settings attributes applied/merged to DynamicSettings   instance.")

settings = DynamicSettings() # noqa: F811
