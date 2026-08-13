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

# config/maps/koans_english/05_koan_search_example/de-DE/bible_search.py

# bible_search.py


import logging
# import re

from pathlib import Path
from rapidfuzz import fuzz


# --- Setup Logging ---

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


import sqlite3

# logger = logging.getLogger("bible_search_sqlite")

# Optional: logging.basicConfig(level=logging.INFO)


# Make sure you type ``translation`` correctly (e.g.: 'kjv', 'luther')

TRANSLATION ='GerElb1905' # 'kjv'
# GerElb1905_books


# 
# project_dir = Path(__file__).parent.parent.parent.parent.parent.parent


# TRANSLATE_SCRIPT = project_dir / 'tools' / 'simple_translate.py'

# PYTHON_EXECUTABLE = project_dir/'.venv'/'bin'/'python3'




# DATABASE_PATH = 'bible.sqlite3' # Adjust if necessary

DATABASE_PATH = Path(__file__).parent / 'GerElb1905.db'
# print(f"DATABASE_PATH={DATABASE_PATH}")



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

        # Quotes about the table names!

        table_books = f'"{translation}_books"'
        table_verses = f'"{translation}_verses"'





        # --- START OF UPDATED SEARCH BLOCK ---


        # 1. Query ALL books as we need to calculate similarity in Python.

        try:
            cur.execute(f"SELECT id, name FROM {table_books}")
            all_books = cur.fetchall()
        except sqlite3.OperationalError:
            logger.error(f"Tabelle {table_books} nicht gefunden.")
            return f"Fehler: Die Übersetzung '{translation}' ist nicht verfügbar."

        if not all_books:
            logger.warning(f"Keine Bücher in Tabelle {table_books} gefunden.")
            return "Keine Bücher gefunden."

        # Best match initialization

        best_score = -1
        best_match_row = None
        user_input_lower = book_name.lower()

        # Define threshold: If the similarity is below this value, a warning is given

        # but the best hit was still used.

        MIN_ACCEPTABLE_SCORE = 60

        # 2. Perform fuzzy comparison

        for book_row in all_books:
            book_name_db = book_row['name']

            # We use fuzz.ratio to measure overall character similarity.

            # For very short names, fuzz.partial_ratio can also be useful.

            score = fuzz.ratio(user_input_lower, book_name_db.lower())

            if score > best_score:
                best_score = score
                best_match_row = book_row

        # 3. Evaluate and assign results

        if best_match_row:
            book_id = best_match_row['id']
            matched_name = best_match_row['name']

            # If the score is below the threshold, we log a warning

            if best_score < 100:
                logger.info(f"Fuzzy Match: Eingabe '{book_name}' (Score: {best_score:.2f}) führte zu '{matched_name}'.")

            # If the score is very bad, we will provide informative feedback

            if best_score < MIN_ACCEPTABLE_SCORE:
                # Here we issue a friendly warning to the user

                # However, we still deliver the best result as desired

                print(f"Warnung: Die Spracheingabe '{book_name}' war undeutlich. Ich habe das ähnlichste Buch '{matched_name}' gewählt.")


            book_name = matched_name

            # Here you can continue working with book_id and matched_name

            # Example:

            # print(f"Book found (ID: {book_id}): {matched_name}")


            # return True # Or call the next function

        else:
            # This theoretically shouldn't happen if the database contains books

            logger.error("Unerwarteter Fehler: Kein bestes Match gefunden.")
            return "Ein interner Fehler ist aufgetreten."

        # --- END OF UPDATED SEARCH BLOCK ---







        # Search by chapter and verse

        cur.execute(
            f"SELECT text FROM {table_verses} WHERE book_id=? AND chapter=? AND verse=?",
            (book_id, int(chapter), int(verse))
        )
        verse_row = cur.fetchone()
        if not verse_row:
            return f"{book_name} {chapter}:{verse} konnte nicht gefunden werden in '{translation}'."

        # Optional: Get translation metadata

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


    # test_data = {'regex_match_obj': DummyMatch()}

    print('execute(test_data)')
