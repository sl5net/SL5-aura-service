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

# config/maps/koans_english/06_koan_wikipedia_suche/de-DE/bible_search.py

# bible_search.py


import logging
# importer re

from pathlib import Path
from rapidfuzz import fuzz


# --- Journalisation de configuration ---

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


import sqlite3

# logger = logging.getLogger("bible_search_sqlite")

# Facultatif : logging.basicConfig(level=logging.INFO)


# Assurez-vous de saisir correctement « traduction » (par exemple : « kjv », « luther »)

TRANSLATION ='GerElb1905' # 'kjv'
# GerElb1905_books


# 
# project_dir = Chemin(__file__).parent.parent.parent.parent.parent.parent


# TRANSLATE_SCRIPT = rép_projet / 'outils' / 'simple_translate.py'

# PYTHON_EXECUTABLE = rép_projet/'.venv'/'bin'/'python3'




# DATABASE_PATH = 'bible.sqlite3' # Ajuster si nécessaire

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

        # Citations sur les noms de tables !

        table_books = f'"{translation}_books"'
        table_verses = f'"{translation}_verses"'





        # --- DÉBUT DU BLOC DE RECHERCHE MIS À JOUR ---


        # 1. Interrogez TOUS les livres car nous devons calculer la similarité en Python.

        try:
            cur.execute(f"SELECT id, name FROM {table_books}")
            all_books = cur.fetchall()
        except sqlite3.OperationalError:
            logger.error(f"Tabelle {table_books} nicht gefunden.")
            return f"Fehler: Die Übersetzung '{translation}' ist nicht verfügbar."

        if not all_books:
            logger.warning(f"Keine Bücher in Tabelle {table_books} gefunden.")
            return "Keine Bücher gefunden."

        # Initialisation de la meilleure correspondance

        best_score = -1
        best_match_row = None
        user_input_lower = book_name.lower()

        # Définir le seuil : Si la similarité est inférieure à cette valeur, un avertissement est donné

        # mais le meilleur coup était toujours utilisé.

        MIN_ACCEPTABLE_SCORE = 60

        # 2. Effectuer une comparaison floue

        for book_row in all_books:
            book_name_db = book_row['name']

            # Nous utilisons fuzz.ratio pour mesurer la similarité globale des caractères.

            # Pour les noms très courts, fuzz.partial_ratio peut également être utile.

            score = fuzz.ratio(user_input_lower, book_name_db.lower())

            if score > best_score:
                best_score = score
                best_match_row = book_row

        # 3. Évaluer et attribuer les résultats

        if best_match_row:
            book_id = best_match_row['id']
            matched_name = best_match_row['name']

            # Si le score est inférieur au seuil, nous enregistrons un avertissement

            if best_score < 100:
                logger.info(f"Fuzzy Match: Eingabe '{book_name}' (Score: {best_score:.2f}) führte zu '{matched_name}'.")

            # Si le score est très mauvais, nous vous fournirons des commentaires informatifs

            if best_score < MIN_ACCEPTABLE_SCORE:
                # Ici, nous émettons un avertissement amical à l'utilisateur

                # Cependant, nous fournissons toujours le meilleur résultat souhaité

                print(f"Warnung: Die Spracheingabe '{book_name}' war undeutlich. Ich habe das ähnlichste Buch '{matched_name}' gewählt.")


            book_name = matched_name

            # Ici, vous pouvez continuer à travailler avec book_id et matched_name

            # Exemple:

            # print(f"Livre trouvé (ID : {book_id}) : {matched_name}")


            # return True # Ou appelle la fonction suivante

        else:
            # Cela ne devrait théoriquement pas se produire si la base de données contient des livres

            logger.error("Unerwarteter Fehler: Kein bestes Match gefunden.")
            return "Ein interner Fehler ist aufgetreten."

        # --- FIN DU BLOC DE RECHERCHE MIS À JOUR ---







        # Recherche par chapitre et verset

        cur.execute(
            f"SELECT text FROM {table_verses} WHERE book_id=? AND chapter=? AND verse=?",
            (book_id, int(chapter), int(verse))
        )
        verse_row = cur.fetchone()
        if not verse_row:
            return f"{book_name} {chapter}:{verse} konnte nicht gefunden werden in '{translation}'."

        # Facultatif : Obtenir les métadonnées de traduction

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
    # Exemples de données de test (en supposant que l'expression régulière corresponde à ces groupes)


    # test_data = {'regex_match_obj' : DummyMatch()}

    print('execute(test_data)')
