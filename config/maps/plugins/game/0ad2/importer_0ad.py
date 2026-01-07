import re
import subprocess
import sys
from pathlib import Path

# --- PFADE ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CFG = Path.home() / ".config/0ad/config/user.cfg"
TARGET_MAP = PROJECT_ROOT / "config/maps/plugins/0ad/de-DE/FUZZY_MAP_pre.py"

TRANSLATE_SCRIPT = PROJECT_ROOT / 'tools' / 'simple_translate.py'
PYTHON_EXECUTABLE = PROJECT_ROOT / '.venv' / 'bin' / 'python3'
if sys.platform == "win32":
    PYTHON_EXECUTABLE = PROJECT_ROOT / '.venv' / 'Scripts' / 'python.exe'

# --- KONFIGURATION (Variablen für den Dateikopf) ---
PREFIX_DEFS = {
    "place": r"(baue|errichte|platziere|build|place|bau|paul)",
    "select": r"(select|auswählen|markieren|fokus|fokussiert|focus|fokussiere)",
}

# Spezial-Mappings (Vosk-Fixes und manuelle Korrekturen)
LABEL_MAP = {
    "house": ["haus", r"\w?aus", "house", "bauhaus", r"b\w+aus"],
    "civilcentre": ["zentrum", "dorfzentrum", "cc"],
}

translation_cache = {}

def get_translation(text):
    if text in translation_cache: return translation_cache[text]
    try:
        result = subprocess.run(
            [str(PYTHON_EXECUTABLE), str(TRANSLATE_SCRIPT), text, 'de'],
            capture_output=True, text=True, check=True, encoding='utf-8'
        )
        translated = result.stdout.strip().lower()
        translation_cache[text] = translated
        return translated
    except: return text

def generate_0ad_map():
    if not SOURCE_CFG.exists(): return print(f"Error: {SOURCE_CFG} not found.")

    # Header mit Definitionen
    output = ["# Auto-generated 0 A.D. Hotkeys\n"]
    for var, regex in PREFIX_DEFS.items():
        output.append(f'{var} = r"{regex}"')

    output.append("\nFUZZY_MAP_pre = [")

    with open(SOURCE_CFG, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r'^\s*([\w\.\(\)\|]+)\s*=\s*"([^"]+)"', line)
            if not match: continue

            key_path, raw_value = match.groups()

            # --- POSITIV FILTER ---
            if not any(word in key_path.lower() for word in ["place", "select"]):
                continue

            hotkeys = [v.strip() for v in raw_value.split(",")]
            context_var = "select" if ("Ctrl" in raw_value or "Alt" in raw_value) else "place"

            sub_matches = re.search(r"\(([\w\|]+)\)", key_path)
            raw_labels = sub_matches.group(1).split("|") if sub_matches else [key_path.split(".")[-1]]

            for raw_label in raw_labels:
                label_en = raw_label.lower()
                label_de = get_translation(label_en)

                for hk in hotkeys:
                    clean_hk = hk.replace(" ", "")
                    # Varianten inkl. Bauhaus & HK-Buchstabe
                    variants = {label_en, label_de, clean_hk.lower()}
                    if label_en in LABEL_MAP:
                        variants.update(LABEL_MAP[label_en])

                    label_pattern = f"({'|'.join(variants)})"

                    # Nutzung von fr" und {variable}
                    # Resultat in Datei: ('H', fx"^{place}\s*(haus|h|bauhaus)\w*$")
                    regex_str = f'fr"^{{{context_var}}}\\s*{label_pattern}\\w*$"'
                    output.append(f"    ('{clean_hk}', {regex_str}),")

    output.append("]")
    TARGET_MAP.parent.mkdir(parents=True, exist_ok=True)
    TARGET_MAP.write_text("\n".join(output), encoding="utf-8")
    print(f"Done. Rules: {len(output)-len(PREFIX_DEFS)-3}")

if __name__ == "__main__":
    # generate_0ad_map()
    print('generate_0ad_map() actually off')
