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
                return 'de-DE'
            # Add more languages here if needed (fr, es, etc.)
    except Exception as e:
        print(f"WARNING: Could not detect system language ({e}). Defaulting to 'en'.")
    return 'en-US' # Default to English

def get_model_name_from_key(key):
    """Maps a simple language key to a full model directory name."""
    if key == 'de':
        key = 'de-DE'
    if key == 'en':
        key = 'en-US'
    model_map = {
        'de-DE': 'vosk-model-de-0.21',
        'en-US': 'vosk-model-en-us-0.22'
    }
    return model_map.get(key, model_map['en-US']) # Default to English model

def main():
    # Assume the script is run from the project root
    project_root = Path('.')
    config_dir = project_root / 'config'
    model_name_file = config_dir / 'model_name.txt'

    # Only run if the file does NOT exist
    if not model_name_file.exists():
        print("INFO: 'model_name.txt' not found. Setting it up now.")
        lang_key_short = get_system_language_code() # get_system_language_code get only a 2 letter long code
        model_name = get_model_name_from_key(lang_key_short)
        print(f"45: INFO: {model_name}")

        # lang_key = guess_lt_language_from_model(logger, model_name)

        try:
            model_name_file.write_text(model_name)
            print(f"SUCCESS: Set initial model to '{model_name}' in '{model_name_file}'.")
        except Exception as e:
            print(f"ERROR: Could not write to '{model_name_file}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"INFO: 'model_name.txt' {model_name_file} already exists -> Skipping create model_name.txt")
        #exit(1)

if __name__ == "__main__":
    main()
