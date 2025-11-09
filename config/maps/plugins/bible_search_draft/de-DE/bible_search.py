# bible_search.py

import logging
# import re
from pathlib import Path

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


import sqlite3

# logger = logging.getLogger("bible_search_sqlite")
# Optional: logging.basicConfig(level=logging.INFO)

# Stelle sicher, dass du ``translation`` korrekt setzt (z.B.: 'kjv', 'luther')
TRANSLATION ='GerElb1905' # 'kjv'
#              GerElb1905_books


#project_dir = Path(__file__).parent.parent.parent.parent.parent.parent

#TRANSLATE_SCRIPT = project_dir / 'tools' / 'simple_translate.py'
#PYTHON_EXECUTABLE = project_dir / '.venv' / 'bin' / 'python3'



#DATABASE_PATH = 'bible.sqlite3'  # Passe ggf. an
DATABASE_PATH = Path(__file__).parent / 'GerElb1905.db'
print(f"DATABASE_PATH={DATABASE_PATH}")


def search_bible_sqlite(book_name, chapter, verse, translation=TRANSLATION, db_path=DATABASE_PATH):
    """
    Sucht einen bestimmten Bibelvers in der angegebenen SQLite-Datenbank.
    :param book_name: Name des Buches (z.B. 'John')
    :param chapter: Kapitelnummer als int oder str
    :param verse: Versnummer als int oder str
    :param translation: Übersetzungsname wie in 'translations' Tabelle und für Tabellennamen-Präfix
    :param db_path: Pfad zur SQLite-DB
    :return: String mit Referenz und Vers
    """
    try:
        con = sqlite3.connect(db_path)
        print(con.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())

        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Quotes um die Tabellennamen!
        table_books = f'"{translation}_books"'
        table_verses = f'"{translation}_verses"'

        # Suche id des Buchs
        cur.execute(f"SELECT id, name FROM {table_books} WHERE lower(name) = ?", (book_name.lower(),))
        book_row = cur.fetchone()
        if not book_row:
            logger.warning(f"Buch '{book_name}' nicht gefunden in Übersetzung '{translation}'")
            return f"Das Buch '{book_name}' existiert nicht in der Übersetzung '{translation}'."

        book_id = book_row['id']
        # Suche nach Kapitel und Vers
        cur.execute(
            f"SELECT text FROM {table_verses} WHERE book_id=? AND chapter=? AND verse=?",
            (book_id, int(chapter), int(verse))
        )
        verse_row = cur.fetchone()
        if not verse_row:
            return f"{book_name} {chapter}:{verse} konnte nicht gefunden werden in '{translation}'."

        # Optional: Übersetzungs-Metadaten holen
        trans_meta = cur.execute(
            "SELECT title FROM translations WHERE translation = ?",
            (translation,)
        ).fetchone()
        translation_title = trans_meta['title'] if trans_meta and 'title' in trans_meta.keys() else translation

        verse_text = verse_row['text'].strip()
        return f"{book_name} {chapter}:{verse} ({translation_title}): {verse_text}"

    except sqlite3.Error as e:
        logger.error(f"SQLite Fehler: {e}")
        return f"Ein Datenbankfehler ist aufgetreten. {e}"




    except Exception as e:
        logger.error(f"Allg. Fehler: {e}")
        return f"Ein unerwarteter Fehler ist aufgetreten: {type(e).__name__}."
    finally:
        con.close()


def execute(match_data, translation=TRANSLATION, db_path=DATABASE_PATH):
    """
    Führt die Suche nach einem bestimmten Bibelvers entsprechend der Nutzeranfrage aus (ohne API, nur lokal/SQLite).
    """
    logger.info("Beginne SQLite-Bibel-Suche.")
    try:
        match_obj = match_data['regex_match_obj']

        book_name = match_obj.group('book').strip()
        chapter = match_obj.group('chapter').strip()
        verse = match_obj.group('verse').strip()

        if not book_name or not chapter or not verse:
            return "Bitte gib Buch, Kapitel und Vers vollständig an."

        result = search_bible_sqlite(book_name, chapter, verse, translation=translation, db_path=db_path)
        logger.info(f"Suche abgeschlossen. Ergebnis-Länge: {len(result)}")
        return result

    except IndexError:
        return "Ich konnte Buch, Kapitel und Vers nicht korrekt erkennen."
    except Exception as e:
        logger.error(f"Fehler in execute: {e}")
        return f"Ein Fehler ist aufgetreten: {type(e).__name__}."





if __name__ == "__main__":
    # Example test data (assuming the regex matched these groups)

    #test_data = {'regex_match_obj': DummyMatch()}
    print('execute(test_data)')
