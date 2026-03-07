#!/usr/bin/env python3
"""
Patcht radio_deep_dive.py um Modell aus config/internal/ai_model.txt zu lesen.
Ausfuehren aus dem STT-Repo-Verzeichnis:
    python patch_radio_model.py
"""
from pathlib import Path
import shutil

RADIO_PATH = Path("config/maps/plugins/z_fallback_llm/de-DE/radio_deep_dive.py")
AI_MODEL_PATH = Path("config/internal/ai_model.txt")

# 1. ai_model.txt erstellen
AI_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
if not AI_MODEL_PATH.exists():
    AI_MODEL_PATH.write_text("qwen2.5:3b\n", encoding="utf-8")
    print(f"✅ Erstellt: {AI_MODEL_PATH}")
else:
    print(f"   Existiert: {AI_MODEL_PATH} -> {AI_MODEL_PATH.read_text().strip()}")

# 2. radio_deep_dive.py patchen
if not RADIO_PATH.exists():
    print(f"!! Nicht gefunden: {RADIO_PATH}")
    exit(1)

content = RADIO_PATH.read_text(encoding="utf-8")

if "_load_model" in content:
    print("   radio_deep_dive.py bereits gepatcht.")
    exit(0)

# Backup
shutil.copy(RADIO_PATH, RADIO_PATH.with_suffix(".py.bak"))
print(f"   Backup: {RADIO_PATH.with_suffix('.py.bak')}")

load_func = '''def _load_model_from_config():
    """Liest Modellname aus config/internal/ai_model.txt, fallback: llama3.2:latest"""
    from pathlib import Path as _Path
    # radio liegt in config/maps/plugins/z_fallback_llm/de-DE/
    # 5 Ebenen hoch = Repo-Root
    cfg = _Path(__file__).parents[4] / "config" / "internal" / "ai_model.txt"
    if cfg.exists():
        model = cfg.read_text(encoding="utf-8").strip().splitlines()[0].strip()
        if model:
            return model
    return "llama3.2:latest"

MODEL_NAME = _load_model_from_config()'''

patched = False
for old in ['MODEL_NAME = "llama3.2:latest"', "MODEL_NAME = 'llama3.2:latest'"]:
    if old in content:
        content = content.replace(old, load_func, 1)
        patched = True
        break

if patched:
    RADIO_PATH.write_text(content, encoding="utf-8")
    print(f"✅ Gepatcht: {RADIO_PATH}")
    print(f"   Modell wird jetzt aus {AI_MODEL_PATH} gelesen.")
else:
    print(f"!! MODEL_NAME-Zeile nicht gefunden.")
    print("   Manuell ersetzen: MODEL_NAME = \"llama3.2:latest\"")
