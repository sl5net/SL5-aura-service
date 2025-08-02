# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# Filename: scripts/py/func/setup_initial_model.py
import locale
import sys
from pathlib import Path

def get_system_language_code():
    """Detects the system language and returns a Vosk-compatible model key."""
    try:
        lang, _ = locale.getdefaultlocale()
        if lang:
            if lang.lower().startswith('de'):
                return 'de'
            # Add more languages here if needed (fr, es, etc.)
    except Exception as e:
        print(f"WARNING: Could not detect system language ({e}). Defaulting to 'en'.")
    return 'en' # Default to English

def get_model_name_from_key(key):
    """Maps a simple language key to a full model directory name."""
    model_map = {
        'de': 'vosk-model-de-0.21',
        'en': 'vosk-model-en-us-0.22'
    }
    return model_map.get(key, model_map['en']) # Default to English model

def main():
    # Assume the script is run from the project root
    project_root = Path('.')
    config_dir = project_root / 'config'
    model_name_file = config_dir / 'model_name.txt'

    # Only run if the file does NOT exist
    if not model_name_file.exists():
        print("INFO: 'model_name.txt' not found. Setting it up now.")
        lang_key = get_system_language_code()
        model_name = get_model_name_from_key(lang_key)

        try:
            model_name_file.write_text(model_name)
            print(f"SUCCESS: Set initial model to '{model_name}' in '{model_name_file}'.")
        except Exception as e:
            print(f"ERROR: Could not write to '{model_name_file}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("INFO: 'model_name.txt' already exists. Skipping setup.")

if __name__ == "__main__":
    main()
