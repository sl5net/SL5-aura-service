# migrate_database.py
from pathlib import Path

from .utils import STOP_WORDS_DE_EXTREME # noqa: F401
from .normalizer import *

#from cache_core import *
from .utils import log_debug

"""
cd config/maps/plugins/z_fallback_llm/de-DE/                                                                                                  1 ✘    STT 
    ~/pr/py/STT/config/maps/plugins/z_fallback_llm/de-DE    master wip !6 ?6  python migrate_database.py                                                                                   ✔    STT 
Starte Datenbank-Migration für 'llm_cache.db'...

----------------------------------------------------
MIGRATION ABGESCHLOSSEN
Total Einträge verarbeitet: 4273
Direkt geupdatete Hashes: 4199
Auf bestehende Hashes verschmolzen (Hits gewonnen!): 62
Geschätzter neuer Max-Hit-Count: 4261 Einträge verbleiben.
----------------------------------------------------
Bitte prüfen Sie die DB mit der SQL GROUP BY Abfrage!

"""

import sqlite3
import hashlib
#import re
from nltk.stem.snowball import GermanStemmer # Benötigt: pip install nltk
#from utils import log_debug

# ----------------------------------------------------
# 1. KONFIGURATION (Bitte anpassen!)
# ----------------------------------------------------

PLUGIN_DIR = Path(__file__).parent
MEMORY_FILE = PLUGIN_DIR / "conversation_history.json"
BRIDGE_FILE = Path("/tmp/aura_clipboard.txt")
DB_FILE = PLUGIN_DIR / "llm_cache_OFF_DUMMY.db"
log_debug(f'DB_FILE = {DB_FILE }')




# ----------------------------------------------------
# 2. HASH-LOGIK (Muss EXAKT der Logik der Live-Anwendung entsprechen!)
# ----------------------------------------------------

# (A) Globale Definitionen (für die einmalige Initialisierung)
COMMAND_SYNONYMS = {
    "erstelle": "neu", "erstellen": "neu", "generiere": "neu", "mach": "neu",
    "mache": "neu", "schreibe": "neu", "füge": "neu", "neue": "neu",
    "zeig": "info", "zeige": "info", "wo": "info", "wie": "info", "hilfe": "info", "erklär": "info",
    "lösche": "del", "entferne": "del", "vergiss": "del",
    "config": "konfig", "configuration": "konfig", "einstellungen": "konfig",
    "regex": "regel", "regeln": "regel", "pattern": "regel"
}




GLOBAL_STEMMER = GermanStemmer()




# ----------------------------------------------------
# 3. MIGRATIONSLOGIK
# ----------------------------------------------------
def migrate_database():
    print(f"Starte Datenbank-Migration für '{DB_FILE}'...")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    #conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA foreign_keys = OFF;")

    # Hole alle Prompts und den Originaltext (alten Hash und Original-Text)
    c.execute("SELECT hash, prompt_text FROM prompts")
    rows = c.fetchall()

    updates_performed = 0
    collisions_prevented = 0

    for old_hash, prompt_text in rows:

        # 1. NEUE Werte berechnen
        new_clean_input = create_ultimate_cache_key(prompt_text)
        new_hash = hashlib.sha256(new_clean_input.encode('utf-8')).hexdigest()


        if new_hash == old_hash:
            # Der Hash hat sich nicht geändert (z.B. weil der Text schon bereinigt war)
            continue

        # 2. Kollisionsprüfung (WICHTIG!)
        c.execute("SELECT hash, prompt_text FROM prompts WHERE hash = ?", (new_hash,))
        existing_row = c.fetchone()

        target_hash = new_hash # Dies ist der Hash, unter dem die Daten gespeichert werden

        if existing_row:
            # KOLLISION: Der Prompt-Eintrag existiert bereits. Lösche den alten.
            target_hash = existing_row[0] # Sicherstellen, dass der Ziel-Hash der existierende Hash ist

            c.execute("UPDATE responses SET prompt_hash = ? WHERE prompt_hash = ?", (target_hash, old_hash))
            c.execute("DELETE FROM prompts WHERE hash = ?", (old_hash,))
            collisions_prevented += 1

        else:
            # KEINE KOLLISION: Zuerst Responses updaten, dann DELETE/INSERT des Prompts

            # 1. Responses updaten (funktioniert jetzt, da FK ausgeschaltet ist)
            c.execute("UPDATE responses SET prompt_hash = ? WHERE prompt_hash = ?", (new_hash, old_hash))

            # 2. Daten des alten Eintrags abrufen, LÖSCHEN, und NEU EINFÜGEN
            c.execute("SELECT prompt_text, last_used FROM prompts WHERE hash=?", (old_hash,))
            old_data = c.fetchone()

            if old_data:
                c.execute("DELETE FROM prompts WHERE hash = ?", (old_hash,))
                c.execute("INSERT INTO prompts (hash, prompt_text, clean_input, keywords, last_used) VALUES (?, ?, ?, ?, ?)",
                         (new_hash, old_data[0], new_clean_input, new_clean_input, old_data[1]))
                updates_performed += 1
            else:
                log_debug(f"⚠️ WARNUNG: Eintrag mit Hash {old_hash[:8]} nicht gefunden.")


    conn.commit()
    conn.close()

    print("\n----------------------------------------------------")
    print("MIGRATION ABGESCHLOSSEN")
    print(f"Total Einträge verarbeitet: {len(rows)}")
    print(f"Direkt geupdatete Hashes: {updates_performed}")
    print(f"Auf bestehende Hashes verschmolzen (Hits gewonnen!): {collisions_prevented}")
    print(f"Geschätzter neuer Max-Hit-Count: {updates_performed + collisions_prevented} Einträge verbleiben.")
    print("----------------------------------------------------")
    print("Bitte prüfen Sie die DB mit der SQL GROUP BY Abfrage!")


# Führen Sie die Funktion aus:
# migrate_database()


def main():
    migrate_database()


if __name__ == "__main__":
    main()
