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
    # 1. ESSAYEZ : importation relative (pour l'appel python -m ...)


    from . import normalizer, utils

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

import hashlib
import sqlite3

# importer re

# from nltk.stem.snowball import GermanStemmer # Benötigt: pip install nltk

# à partir d'utils import utils.log_debug


# ----------------------------------------------------

# 1. CONFIGURATION (Veuillez ajuster !)

# ----------------------------------------------------






# ----------------------------------------------------

# 2. LOGIQUE DE HASH (Doit correspondre EXACTEMENT à la logique de l'application en direct !)

# ----------------------------------------------------


# (A) Définitions globales (pour une initialisation unique)

COMMAND_SYNONYMS = {
    "erstelle": "neu", "erstellen": "neu", "generiere": "neu", "mach": "neu",
    "mache": "neu", "schreibe": "neu", "füge": "neu", "neue": "neu",
    "zeig": "info", "zeige": "info", "wo": "info", "wie": "info", "hilfe": "info", "erklär": "info",
    "lösche": "del", "entferne": "del", "vergiss": "del",
    "config": "konfig", "configuration": "konfig", "einstellungen": "konfig",
    "regex": "regel", "regeln": "regel", "pattern": "regel"
}








# ----------------------------------------------------

# 3. LOGIQUE DE MIGRATION

# ----------------------------------------------------

def migrate_database():
    print(f"Starte Datenbank-Migration für '{utils.DB_FILE}'…")
    conn = sqlite3.connect(utils.DB_FILE)
    c = conn.cursor()

    # conn.execute("PRAGMA étrangers_keys = ON;")

    conn.execute("PRAGMA foreign_keys = OFF;")

    # Obtenez toutes les invites et le texte original (ancien hachage et texte original)

    c.execute("SELECT hash, prompt_text FROM prompts")
    rows = c.fetchall()

    updates_performed = 0
    collisions_prevented = 0

    for old_hash, prompt_text in rows:

        # 1. Calculer de NOUVELLES valeurs

        new_clean_input = normalizer.create_ultimate_cache_key(prompt_text)
        new_hash = hashlib.sha256(new_clean_input.encode('utf-8')).hexdigest()


        if new_hash == old_hash:
            # Le hachage n'a pas changé (par exemple parce que le texte a déjà été nettoyé)

            continue

        # 2. Contrôle de collision (IMPORTANT !)

        c.execute("SELECT hash, prompt_text FROM prompts WHERE hash = ?", (new_hash,))
        existing_row = c.fetchone()

        target_hash = new_hash # Dies ist der Hash, unter dem die Daten gespeichert werden

        if existing_row:
            # COLLISION : l'entrée d'invite existe déjà. Supprimez l'ancien.

            target_hash = existing_row[0] # Sicherstellen, dass der Ziel-Hash der existierende Hash ist

            c.execute("UPDATE responses SET prompt_hash = ? WHERE prompt_hash = ?", (target_hash, old_hash))
            c.execute("DELETE FROM prompts WHERE hash = ?", (old_hash,))
            collisions_prevented += 1

        else:
            # AUCUNE COLLISION : mettez d'abord à jour les réponses, puis SUPPRIMEZ/INSÉREZ l'invite


            # 1. Mettre à jour les réponses (fonctionne maintenant que FK est désactivé)

            c.execute("UPDATE responses SET prompt_hash = ? WHERE prompt_hash = ?", (new_hash, old_hash))

            # 2. Récupérez, SUPPRIMEZ et INSÉREZ les données de l'ancienne entrée

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


# Exécutez la fonction :

# migrer la base de données()



def main():
    utils.log_debug('migrate_database() deaktiviert 3.12.25 02:18 Wed')
    # migrer la base de données()



if __name__ == "__main__":
    main()
