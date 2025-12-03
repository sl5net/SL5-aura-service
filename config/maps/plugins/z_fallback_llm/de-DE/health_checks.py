import sys
import sqlite3

from nltk.stem.snowball import GermanStemmer
GLOBAL_STEMMER = GermanStemmer()


from . import utils

def check_db_statistics_and_exit_if_invalid():
    """Prüft die DB-Statistiken (Total Hits > Unique Prompts) und bricht bei Inkonsistenz ab."""
    conn = None
    try:
        absolute_db_path = str(utils.DB_FILE)
        conn = sqlite3.connect(f'file:{absolute_db_path}?mode=ro', timeout=10, uri=True)
        if not conn:
            print("!!! DATENBANK keine Verbindung !!!")
            print('sys.exit(1) 2025-1201-1802')
            sys.exit(1)

        c = conn.cursor()

        # Total Hits korrekt abfragen
        S1 = "SELECT COUNT(*) FROM responses"
        print(f"{S1}")
        c.execute(S1)
        row = c.fetchone()
        total_hits = row[0] if row and row[0] is not None else 0

        # Unique Prompts korrekt abfragen
        S2 = "SELECT COUNT(DISTINCT prompt_hash) FROM responses"
        print(f"{S2}")
        c.execute(S2)
        row = c.fetchone()
        unique_prompts = row[0] if row and row[0] is not None else 0

        # Verbessertes Prüfungs-Logik
        if unique_prompts == 0:
            diagnosis = f"{utils.DB_FILE} ist LEER. Es sind 0 eindeutige Fragen vorhanden. sqlitebrowser {utils.DB_FILE} & "
        elif unique_prompts < 2:
            diagnosis = f"Datenbank ist zu leer. Nur {unique_prompts} eindeutige Fragen."
        elif total_hits < unique_prompts:
            diagnosis = f"LOGIKFEHLER! Total Hits ({total_hits}) sind kleiner als Unique Prompts ({unique_prompts})."
        else:
            print(f"[STATISTIK OK] Cache-Hits: {total_hits}, Eindeutige Fragen: {unique_prompts}")
            if conn:
                conn.close()
            return True

        # Fehler-Ausgabe bei Fehlschlag
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! KRITISCHER FEHLER: DATENBANK INKONSISTENT/ZU LEER !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"DIAGNOSE: {diagnosis}")
        print(f"PRÜFUNG: Ist die Datenbank '{utils.DB_FILE}' die richtige Datei?")
        if conn:
            conn.close()
        print('sys.exit(1) 2025-1201-1801')
        sys.exit(1)

    except Exception as e:
        print(f"KRITISCHER FEHLER: Datenbankfehler: {e}")
        if conn:
            conn.close()
        print('sys.exit(1) 2025-1201-18022')
        sys.exit(1)

