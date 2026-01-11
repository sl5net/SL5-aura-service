import json
from pathlib import Path

POSSIBLE_PATHS = [
    Path("quiz_db.json"),
    Path("de-DE/quiz_db.json"),

    Path("config/maps/plugins/anki_quiz/de-DE/quiz_db.json"),
    Path("../config/maps/plugins/anki_quiz/de-DE/quiz_db.json"),
]

DB_PATH = None
for p in POSSIBLE_PATHS:
    if p.exists():
        DB_PATH = p
        break


# Pfad zur Problem-Datei (bitte anpassen falls nötig)

print(f"Prüfe Datei: {DB_PATH.resolve()}")

if not DB_PATH.exists():
    print("FEHLER: Datei existiert nicht!")
    exit()

try:
    with open(DB_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"Dateigröße: {len(content)} Zeichen")

    # Der Fehler war ca. bei Zeichen 34059
    # Wir schauen uns den Bereich davor und danach an
    ERROR_POS = 34059
    START = max(0, ERROR_POS - 100)
    END = min(len(content), ERROR_POS + 100)

    print("\n--- UMGEBUNG DES FEHLERS ---")
    snippet = content[START:END]
    print(snippet)
    print("----------------------------")
    print(f"Zeichen an Position {ERROR_POS}: {repr(content[ERROR_POS]) if ERROR_POS < len(content) else 'EOF'}")

    # Versuch zu parsen, um den Fehler zu reproduzieren
    print("\nVersuche Parse...")
    json.loads(content)
    print("SUCCESS: JSON ist valide!")

except json.JSONDecodeError as e:
    print(f"\nCRASH: {e}")
    print(f"Fehler ist in Zeile {e.lineno}, Spalte {e.colno}, Char {e.pos}")
except Exception as e:
    print(f"\nAllgemeiner Fehler: {e}")
