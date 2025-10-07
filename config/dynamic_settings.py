# config/dynamic_settings.py
import collections.abc # Corrected import to collections.abc
import importlib
import sys
import os
from threading import RLock

class DynamicSettings:
    _instance = None
    _lock = RLock()

    _last_modified_time = 0

    _settings_module = None

    _settings_local_module = None

    _settings_file_path = None
    _settings_local_file_path = None

    import time  # Importiere time für os.path.getmtime

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DynamicSettings, cls).__new__(cls)
                print("DEBUG: DynamicSettings.__new__ called, initializing instance.")
                cls._instance._init_settings()
        return cls._instance

    def _init_settings(self):
        self._settings_file_path = os.path.join(
            os.path.dirname(__file__), "settings.py"
        )
        self._settings_local_file_path = os.path.join(
            os.path.dirname(__file__), "settings_local.py"
        )
        print(f"DEBUG: DynamicSettings._init_settings called. Base settings file: {self._settings_file_path}")
        print(f"DEBUG: DynamicSettings._init_settings called. Local settings file: {self._settings_local_file_path}")
        self.reload_settings(force=True)

    def reload_settings(self, force=False):
        print("DEBUG: reload_settings called.")
        with self._lock:
            print("DEBUG: Lock acquired for settings reload.")

            base_modified_time = os.path.getmtime(self._settings_file_path) if os.path.exists(self._settings_file_path) else 0
            local_modified_time = 0
            if self._settings_local_file_path and os.path.exists(self._settings_local_file_path):
                local_modified_time = os.path.getmtime(self._settings_local_file_path)

            any_file_modified = (
                base_modified_time > self._last_modified_time or
                local_modified_time > self._last_modified_time
            )

            # print(f"DEBUG: local_modified_time = {local_modified_time}")
            # print(f"DEBUG: local_modified_time = {local_modified_time}")
            # print(f"DEBUG: local_modified_time = {local_modified_time}")
            # print(f"DEBUG: local_modified_time = {local_modified_time}")
            # print(f"DEBUG: local_modified_time = {local_modified_time}")
            # print(f"DEBUG: local_modified_time = {local_modified_time}")
            # print(f"DEBUG: local_modified_time = {local_modified_time}")
            # print(f"DEBUG: local_modified_time = {local_modified_time}")

            if force or self._settings_module is None or any_file_modified:
                print("DEBUG: Reloading settings due to modification or force.")

                # --- Reloading base settings (config.settings) ---
                if 'config.settings' in sys.modules:
                    print("DEBUG: Calling importlib.reload(sys.modules['config.settings'])")
                    self._settings_module = importlib.reload(sys.modules['config.settings'])
                else:
                    print("DEBUG: Calling importlib.import_module('config.settings')")
                    self._settings_module = importlib.import_module('config.settings')
                print("DEBUG: Base settings loaded.")

                # --- Reloading local settings (config.settings_local) ---
                try:
                    if os.path.exists(self._settings_local_file_path):
                        if 'config.settings_local' in sys.modules:
                            print("DEBUG: Calling importlib.reload(sys.modules['config.settings_local'])")
                            self._settings_local_module = importlib.reload(sys.modules['config.settings_local'])
                        else:
                            print("DEBUG: Calling importlib.import_module('config.settings_local')")
                            self._settings_local_module = importlib.import_module('config.settings_local')
                        print("DEBUG: Local settings loaded.")
                    else:
                        print("INFO: config.settings_local.py does not exist. Skipping local settings load.")
                        self._settings_local_module = None
                except ModuleNotFoundError:
                    print("WARNING: config.settings_local module not found. This might indicate a path issue or missing file.")
                    self._settings_local_module = None
                except Exception as e:
                    print(f"CRITICAL ERROR: Exception during config.settings_local import/reload: {e}")
                    import traceback
                    traceback.print_exc()
                    raise

                print("DEBUG: --- Merging settings ---")
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
                    print("DEBUG: Base settings attributes applied to DynamicSettings instance.")

                # Apply/Merge local settings
                if self._settings_local_module:
                    for attr in dir(self._settings_local_module):
                        if not attr.startswith('__'):
                            local_value = getattr(self._settings_local_module, attr)

                            if hasattr(self, attr) and isinstance(getattr(self, attr), collections.abc.MutableMapping) and isinstance(local_value, collections.abc.MutableMapping):
                                merged_dict = getattr(self, attr)
                                merged_dict.update(local_value)
                                setattr(self, attr, merged_dict)
                                print(f"DEBUG: Merged dictionary setting '{attr}': {getattr(self, attr)}")
                            elif hasattr(self, attr) and isinstance(getattr(self, attr), collections.abc.MutableSequence) and not isinstance(getattr(self, attr), (str, bytes)) and isinstance(local_value, collections.abc.MutableSequence) and not isinstance(local_value, (str, bytes)):
                                merged_list = getattr(self, attr)
                                for item in local_value:
                                    if item not in merged_list:
                                        merged_list.append(item)
                                setattr(self, attr, merged_list)
                                print(f"DEBUG: Merged list setting '{attr}': {getattr(self, attr)}")
                            else:
                                setattr(self, attr, local_value)
                                print(f"DEBUG: Overrode setting '{attr}' with local value: {local_value}")
                    print("DEBUG: Local settings attributes applied/merged to DynamicSettings instance.")

                self._last_modified_time = max(base_modified_time, local_modified_time)
                print(f"DEBUG: Last modified time updated to: {self._last_modified_time}")
                print("DEBUG: Settings reloaded successfully. Lock released.")
            else:
                print("DEBUG: No settings file modification detected. Using existing settings.")
            print("DEBUG: Reload_settings finished.") # This line needs to be outside the 'if force or ...' but inside the 'with self._lock:'

settings = DynamicSettings()
