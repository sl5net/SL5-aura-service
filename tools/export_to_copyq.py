#!/usr/bin/env python3
import os
import re
import sys
import shutil
import subprocess

# -----------------------------------------------------------------------------
# KONFIGURATION
# -----------------------------------------------------------------------------
COPYQ_TAB_NAME = "SL5-Demo"
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
MAPS_DIR = os.path.join(TOOL_DIR, "..", "config", "maps")
TARGET_FILES = ["FUZZY_MAP.py", "FUZZY_MAP_pre.py"]

# -----------------------------------------------------------------------------
# CHECK COPYQ & ENVIRONMENT
# -----------------------------------------------------------------------------
if not shutil.which("copyq"):
    print("Fehler: 'copyq' Befehl nicht gefunden.")
    sys.exit(1)

# Fix für die Locale-Warnungen (Qt braucht UTF-8)
env = os.environ.copy()
env["LANG"] = "C.UTF-8"
env["LC_ALL"] = "C.UTF-8"

try:
    subprocess.run(["copyq", "version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
except Exception:
    print("Fehler: CopyQ läuft nicht. Bitte starten.")
    sys.exit(1)

# -----------------------------------------------------------------------------
# EXTRAKTION
# -----------------------------------------------------------------------------
def collect_examples():
    examples = set() # Set verhindert Duplikate automatisch
    total_tags_found = 0

    regex_example = re.compile(r'^\s*#\s*EXAMPLE:\s*(.*)$')

    if not os.path.isdir(MAPS_DIR):
        print(f"Fehler: Ordner {MAPS_DIR} nicht gefunden.")
        sys.exit(1)

    print(f"Scanne {os.path.relpath(MAPS_DIR)} ...")

    file_count = 0
    for root, dirs, files in os.walk(MAPS_DIR):
        for file in files:
            if file in TARGET_FILES:
                file_path = os.path.join(root, file)
                file_count += 1
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            match = regex_example.search(line)
                            if match:
                                content = match.group(1).strip()
                                if content:
                                    total_tags_found += 1
                                    examples.add(content) # Fügt nur hinzu, wenn neu
                except Exception as e:
                    print(f"Warnung bei {file}: {e}")

    unique_examples = sorted(list(examples))

    print(f"Statistik:")
    print(f"  - Dateien gescannt: {file_count}")
    print(f"  - Tags gefunden:    {total_tags_found}")
    print(f"  - Einzigartig:      {len(unique_examples)} (Duplikate entfernt)")

    return unique_examples

# -----------------------------------------------------------------------------
# COPYQ EXPORT
# -----------------------------------------------------------------------------
def export_to_copyq(items):
    if not items:
        print("Keine Beispiele gefunden.")
        return

    print(f"removetab Tab fist'{COPYQ_TAB_NAME}' ...")
    subprocess.run(["copyq", "removetab", COPYQ_TAB_NAME], check=True, env=env)

    print(f"Erstelle/Wechsle zu Tab '{COPYQ_TAB_NAME}' ...")
    subprocess.run(["copyq", "tab", COPYQ_TAB_NAME], check=True, env=env)

    print("Leere alten Inhalt ...")
    # Löscht alles im aktuellen Tab
    subprocess.run(["copyq", "eval", f"tab('{COPYQ_TAB_NAME}'); if(size()>0) remove(0, size())"], check=True, env=env)

    print(f"Importiere {len(items)} Beispiele ...")

    # Batch-Processing
    BATCH_SIZE = 50
    total = len(items)

    for i in range(0, total, BATCH_SIZE):
        batch = items[i:i+BATCH_SIZE]
        # Wir fügen die Liste rückwärts ein oder nutzen 'add'.
        # CopyQ 'add' packt das neueste Item nach ganz oben (Stack).
        # Damit A oben ist und Z unten, müssten wir Z zuerst einfügen.
        # Wir drehen den Batch hier um, damit die Reihenfolge im Tab halbwegs alphabetisch wirkt.
        batch_reversed = batch[::-1]

        cmd = ["copyq", "tab", COPYQ_TAB_NAME, "add"] + batch_reversed
        subprocess.run(cmd, check=True, env=env)
        print(f"  ... {min(i+BATCH_SIZE, total)} / {total}")

    print("\nFertig! Viel Erfolg bei der Demo.")

# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    data = collect_examples()
    # Damit es im CopyQ von oben nach unten A->Z lesbar ist,
    # müssen wir es Z->A einfügen (da CopyQ wie ein Stapel ist).
    # Wir drehen die ganze Liste einmal um, bevor wir sie batchen.
    data.reverse()
    export_to_copyq(data)
