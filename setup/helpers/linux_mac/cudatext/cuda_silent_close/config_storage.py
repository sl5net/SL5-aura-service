import json
import os
from cudatext import APP_DIR_SETTINGS, app_path


def get_settings_file_path(filename):
    return os.path.join(app_path(APP_DIR_SETTINGS), filename)


def load_plugin_state(filename, default_state):
    config_path = get_settings_file_path(filename)
    try:
        if os.path.isfile(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return bool(data.get('enabled', default_state))
    except Exception:
        pass
    return default_state


def save_plugin_state(filename, state):
    config_path = get_settings_file_path(filename)
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump({'enabled': bool(state)}, f, indent=2)
    except Exception:
        pass