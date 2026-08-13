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

# config/maps/plugins/z_fallback_llm/de-DE/fix_db_keywords.py

import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "llm_cache_OFFF.db"

def main():
    if not DB_FILE.exists():
        print("❌ Keine Datenbank gefunden.")
        return

    print(f"🔧 Öffne Datenbank: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    try:
        # 1. Obtenga todas las indicaciones que tengan palabras clave.

        c.execute("SELECT hash, keywords FROM prompts WHERE keywords IS NOT NULL")
        rows = c.fetchall()

        print(f"🔎 Prüfe {len(rows)} Einträge…")
        updated_count = 0

        for row in rows:
            hash_key = row[0]
            raw_keywords = row[1]

            # --- LÓGICA DE CLASIFICACIÓN ---

            # 1. Dividir

            words = raw_keywords.split()
            # 2. Ordenar

            words.sort()
            # 3. Armarlo

            sorted_keywords = " ".join(words)

            # Actualizar solo si algo ha cambiado

            if sorted_keywords != raw_keywords:
                c.execute("UPDATE prompts SET keywords = ? WHERE hash = ?", (sorted_keywords, hash_key))
                updated_count += 1
                print(f"   ♻️  Sortiert: '{raw_keywords}' -> '{sorted_keywords}'")

        conn.commit()
        print("-" * 40)
        print(f"✅ Fertig! {updated_count} Einträge wurden bereinigt.")

    except Exception as e:
        print(f"❌ Fehler: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
