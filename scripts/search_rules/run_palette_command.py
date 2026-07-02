# scripts/search_rules/run_palette_command.py:1
import sys
import os
import time
import traceback
import builtins
import logging

from pathlib import Path

# Sichert, dass der Log-Pfad korrekt aufgelöst wird
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
LOG_FILE_PATH = PROJECT_ROOT / 'log' / 'heavy_imports.log'

if not hasattr(builtins, "_logged_heavy_imports"):
    builtins._logged_heavy_imports = set()

_original_import = builtins.__import__
def _hook_import(name, *args, **kwargs):
    targets = ('pandas', 'scipy', 'pygame', 'audio_manager', 'sklearn', 'nltk', 'trino', 'vosk', 'sounddevice', 'watchdog')
    if name in targets and name not in builtins._logged_heavy_imports:
        builtins._logged_heavy_imports.add(name)
        try:
            trigger_file = "Unknown"
            trigger_line = 0
            for frame in reversed(traceback.extract_stack()):
                if "site-packages" not in frame.filename and "frozen" not in frame.filename and "run_palette_command" not in frame.filename:
                    trigger_file = frame.filename
                    trigger_line = frame.lineno
                    break
            with open(LOG_FILE_PATH, "a", encoding="utf-8") as f_log:
                f_log.write(f"📢 HEAVY IMPORT DETECTED: '{name}' imported by '{trigger_file}' on line {trigger_line}\n")
        except Exception:
            pass
    return _original_import(name, *args, **kwargs)
builtins.__import__ = _hook_import

# 1. Projekt-Root ermitteln und in den Python-Pfad eintragen
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

# 2. Standard-Logger aufbauen (unterdrückt Log-Meldungen im Terminal)
logger = logging.getLogger("AuraPalette")
logger.addHandler(logging.NullHandler())

try:
    from scripts.py.func.process_text_in_background import process_text_in_background
    from scripts.py.func.config.dynamic_settings import settings
except ImportError as e:
    print(f"Error importing Aura modules: {e}", file=sys.stderr)
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: run_palette_command.py <text_command>")
        sys.exit(1)

    raw_text = sys.argv[1]
    lang_code = "de-DE"

    # 3. LanguageTool-URL dynamisch aus den Einstellungen laden
    lt_url = getattr(settings, 'active_lt_url', None)

    # 4. Output-Verzeichnis für den Type-Watcher auflösen
    is_windows = (os.name == 'nt')
    tmp_dir = Path("C:/tmp") if is_windows else Path("/tmp")
    output_dir = tmp_dir / "sl5_aura" / "tts_output"

    # 5. Natives Aura-Backend synchron ausführen (erzeugt tts_output_*.txt automatisch)
    process_text_in_background(
        logger,
        lang_code,
        raw_text,
        None,
        time.time(),
        lt_url,
        output_dir_override=str(output_dir),
        session_id=999,
        chunk_id=1
    )

if __name__ == '__main__':
    main()
