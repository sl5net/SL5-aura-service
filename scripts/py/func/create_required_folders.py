# file: scripts/py/func/create_required_folders.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
LOG_DIR = BASE_DIR / "log"
config = BASE_DIR / "config"
MODEL_DIR = BASE_DIR / "model"
TMP_DIR = Path("/tmp")
TMP_DICTATION_DIR = Path("/tmp/sl5_dictation")

# Eine Liste aller zu erstellenden Verzeichnisse
REQUIRED_DIRS = [
    LOG_DIR,
    config,
    MODEL_DIR,
    TMP_DIR,
    TMP_DICTATION_DIR
]

def create_required_folders():

    print("Ensuring all required directories exist...")
    for dir_path in REQUIRED_DIRS:
        try:
            # exist_ok=True:
            # parents=True:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  -> OK: {dir_path}")
        except Exception as e:
            print(f"  -> ERROR: Could not create directory {dir_path}: {e}")

if __name__ == "__main__":
    create_required_folders()

