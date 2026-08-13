# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/z_fallback_llm/de-DE/migrate_database.py

# migrate_database.py # migrate_database


try:
    # 1. TRY: Relative import (for python -m ... call)


    from . import normalizer
    from . import utils

except ImportError:
    import normalizer
    import utils









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
# import re

# from nltk.stem.snowball import GermanStemmer # Requires: pip install nltk

# from utils import utils.log_debug


# ----------------------------------------------------

# 1. CONFIGURATION (Please adjust!)

# ----------------------------------------------------






# ----------------------------------------------------

# 2. HASH LOGIC (Must EXACTLY match the logic of the live application!)

# ----------------------------------------------------


# (A) Global definitions (for one-time initialization)

COMMAND_SYNONYMS = {
    "erstelle": "neu", "erstellen": "neu", "generiere": "neu", "mach": "neu",
    "mache": "neu", "schreibe": "neu", "füge": "neu", "neue": "neu",
    "zeig": "info", "zeige": "info", "wo": "info", "wie": "info", "hilfe": "info", "erklär": "info",
    "lösche": "del", "entferne": "del", "vergiss": "del",
    "config": "konfig", "configuration": "konfig", "einstellungen": "konfig",
    "regex": "regel", "regeln": "regel", "pattern": "regel"
}








# ----------------------------------------------------

# 3. MIGRATION LOGIC

# ----------------------------------------------------

def migrate_database():
    print(f"Starte Datenbank-Migration für '{utils.DB_FILE}'…")
    conn = sqlite3.connect(utils.DB_FILE)
    c = conn.cursor()

    # conn.execute("PRAGMA foreign_keys = ON;")

    conn.execute("PRAGMA foreign_keys = OFF;")

    # Get all prompts and original text (old hash and original text)

    c.execute("SELECT hash, prompt_text FROM prompts")
    rows = c.fetchall()

    updates_performed = 0
    collisions_prevented = 0

    for old_hash, prompt_text in rows:

        # 1. Calculate NEW values

        new_clean_input = normalizer.create_ultimate_cache_key(prompt_text)
        new_hash = hashlib.sha256(new_clean_input.encode('utf-8')).hexdigest()


        if new_hash == old_hash:
            # The hash has not changed (e.g. because the text was already cleaned)

            continue

        # 2. Collision check (IMPORTANT!)

        c.execute("SELECT hash, prompt_text FROM prompts WHERE hash = ?", (new_hash,))
        existing_row = c.fetchone()

        target_hash = new_hash # Dies ist der Hash, unter dem die Daten gespeichert werden

        if existing_row:
            # COLLISION: The prompt entry already exists. Delete the old one.

            target_hash = existing_row[0] # Sicherstellen, dass der Ziel-Hash der existierende Hash ist

            c.execute("UPDATE responses SET prompt_hash = ? WHERE prompt_hash = ?", (target_hash, old_hash))
            c.execute("DELETE FROM prompts WHERE hash = ?", (old_hash,))
            collisions_prevented += 1

        else:
            # NO COLLISION: First update responses, then DELETE/INSERT the prompt


            # 1. Update responses (works now that FK is turned off)

            c.execute("UPDATE responses SET prompt_hash = ? WHERE prompt_hash = ?", (new_hash, old_hash))

            # 2. Retrieve, DELETE, and INSERT data from the old entry

            c.execute("SELECT prompt_text, last_used FROM prompts WHERE hash=?", (old_hash,))
            old_data = c.fetchone()

            if old_data:
                c.execute("DELETE FROM prompts WHERE hash = ?", (old_hash,))
                c.execute("INSERT INTO prompts (hash, prompt_text, clean_input, keywords, last_used) VALUES (?, ?, ?, ?, ?)",
                         (new_hash, old_data[0], new_clean_input, new_clean_input, old_data[1]))
                updates_performed += 1
            else:
                utils.log_debug(f"⚠️ WARNUNG: Eintrag mit Hash {old_hash[:8]} nicht gefunden.")


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


# Run the function:

# migrate database()



def main():
    utils.log_debug('migrate_database() deaktiviert 3.12.25 02:18 Wed')
    # migrate database()



if __name__ == "__main__":
    main()
