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
        # 1. Alle Prompts holen, die Keywords haben
        c.execute("SELECT hash, keywords FROM prompts WHERE keywords IS NOT NULL")
        rows = c.fetchall()

        print(f"🔎 Prüfe {len(rows)} Einträge...")
        updated_count = 0

        for row in rows:
            hash_key = row[0]
            raw_keywords = row[1]

            # --- SORTIER LOGIK ---
            # 1. Splitten
            words = raw_keywords.split()
            # 2. Sortieren
            words.sort()
            # 3. Zusammenfügen
            sorted_keywords = " ".join(words)

            # Nur Update machen, wenn sich was geändert hat
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
