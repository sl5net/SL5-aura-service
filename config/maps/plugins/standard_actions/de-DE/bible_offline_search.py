import logging
import re
from pathlib import Path
import sys
# --- HINZUGEFÜGTE IMPORTE FÜR DEN INITIALEN DOWNLOAD ---
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "bible_text_lut.txt"

# Store pre-loaded data globally to avoid reading the file repeatedly
BIBLE_DATA = {}

# Global default content for self-creation
DEFAULT_CONTENT = "Joh 3:16 Also hat Gott die Welt geliebt, dass er seinen eingeborenen Sohn gab, auf dass alle, die an ihn glauben, nicht verloren werden, sondern das ewige Leben haben."

# Konfiguration für den Initial-Download (Scraping)
GERMAN_TRANSLATION_CODE = "LUT"
BIBLESCRAPER_URL_BASE = "https://www.bibleserver.com/text/"
INITIAL_VERSES_TO_FETCH = [
    ("Joh", 3, 16),
    ("Gen", 1, 1),
    ("Ps", 23, 1),
    ("Mt", 6, 33),
    ("1Kor", 13, 13)
]
# German book names mapped to Bibleserver's abbreviation (Nur Beispiele)
GERMAN_BOOK_MAP = {
    'johannes': 'Joh', 'genesis': 'Gen', 'matthäus': 'Mt', 'psalm': 'Ps',
    'lukas': 'Lk', 'markus': 'Mk', 'korinther': 'Kor', '1korinther': '1Kor',
    # Die Mappings werden hier nur informativ genutzt, da wir im INITIAL_VERSES_TO_FETCH
    # die Abkürzungen direkt nutzen.
}

# --- HILFSFUNKTION FÜR DEN DOWNLOAD ---

def scrape_and_format_verse(book_abbr, chapter, verse):
    """Holt einen Vers von Bibleserver und formatiert ihn für die lokale Speicherung."""
    # Beispiel-Referenz: Joh3,16
    reference_key = f"{book_abbr}{chapter},{verse}"
    full_url = f"{BIBLESCRAPER_URL_BASE}{GERMAN_TRANSLATION_CODE}/{quote(reference_key)}"

    try:
        response = requests.get(full_url, headers={'User-Agent': 'SL5AuraDownloader/1.0'}, timeout=10)

        if response.status_code != 200:
            logger.error(f"Scraping failed with HTTP {response.status_code} for {reference_key}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        verse_text_parts = []

        # Suchen nach dem Vers-Text (Klasse ist spekulativ und muss ggf. angepasst werden)
        verse_div = soup.find('div', class_='bibletext')

        if verse_div:
            # Suchen Sie den Vers-Text innerhalb des Hauptcontainers
            for verse_span in verse_div.find_all(class_='verse-text'):
                 verse_text_parts.append(verse_span.text.strip())

            if verse_text_parts:
                full_text = " ".join(verse_text_parts).strip()
                # Rückgabe im Format: Joh 3:16 Text...
                return f"{book_abbr} {chapter}:{verse} {full_text}"

        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during initial data fetch: {e}")
        return None
    except Exception as e:
        logger.error(f"Scraping error: {e}")
        return None

# --- REVIDIERTE load_bible_data FUNKTION ---

# --- REVIDIERTE load_bible_data FUNKTION ---

def load_bible_data():
    """Lädt die statische Bibeldatei und initialisiert sie bei Bedarf über Online-Scraping."""
    global BIBLE_DATA
    if BIBLE_DATA:
        return True

    logger.info(f"Attempting to load offline Bible data from {DATA_FILE}")
    content_read = None

    # 1. VERSUCH: Lese die lokale Datei
    try:
        file_path = DATA_FILE.resolve()

        if file_path.exists():
            file_size_bytes = file_path.stat().st_size
            MIN_SIZE_BYTES = 5 * 1024 # 5 KB Minimum

            # --- NEUE LOGIK: GRÖSSENPRÜFUNG ---
            if file_size_bytes < MIN_SIZE_BYTES:
                logger.warning(f"File size check: {DATA_FILE.name} is only {file_size_bytes / 1024:.2f} KB. Proceeding to online fetch.")
                # content_read bleibt None, was den Fallback triggert
            else:
                 # Datei ist groß genug, lies den Inhalt
                 with open(file_path, 'r', encoding='utf-8') as f:
                    content_read = f.read().strip()

    except FileNotFoundError:
        logger.warning(f"Offline Bible data file not found at {DATA_FILE}. Starting initial online fetch.")
    except Exception as e:
        logger.error(f"Error reading offline data: {e}")
        return False


    # --- PARSING & PRÜFUNG ---
    if content_read:
        try:
            for line in content_read.splitlines():
                line = line.strip()
                if not line: continue

                match = re.match(r'([A-Za-z]+\s*\d+:\d+)', line)
                if match:
                    book_ref = match.group(1).strip()
                    lookup_key = f"{book_ref.replace(' ', '').lower()}"
                    BIBLE_DATA[lookup_key] = line.strip()

            logger.info(f"Successfully loaded {len(BIBLE_DATA)} verses from file.")
            if len(BIBLE_DATA) > 0:
                 return True
            logger.warning("File was empty after reading. Proceeding to initial online fetch.")

        except Exception as e:
            logger.error(f"Error parsing loaded data: {e}")
            logger.warning("Parsing failed. Proceeding to initial online fetch.")


    # 2. FALLBACK: Führe den initialen Online-Download durch (Nur wenn BIBLE_DATA leer ist)
    if not BIBLE_DATA:
        fetched_lines = []

        try:
            # --- ONLINE FETCH LOGIC ---
            for abbr, ch, vs in INITIAL_VERSES_TO_FETCH:
                logger.info(f"Fetching: {abbr} {ch}:{vs}")
                formatted_verse = scrape_and_format_verse(abbr, ch, vs)
                if formatted_verse:
                    fetched_lines.append(formatted_verse)

            if fetched_lines:
                # Erfolgreich Daten geholt, speichern und dann Parsen (Rekursion ist hier OK)
                try:
                    with open(DATA_FILE, 'w', encoding='utf-8') as f:
                        f.write("\n".join(fetched_lines) + "\n")
                    logger.info(f"Successfully created and saved {len(fetched_lines)} verses locally.")
                    return load_bible_data()

                except Exception as create_e:
                    logger.error(f"FATAL: Failed to create or write file during online fallback: {create_e}")
                    # Weiter zum Minimal-Fallback (Schritt 3)
                    pass
        except Exception as fetch_e:
             logger.error(f"Error during online fetch: {fetch_e}")


    # 3. ZWECKS MINIMALFUNKTION: Notfall-Default-Vers (Wenn Online-Fallback und Parsing fehlschlagen)
    if not BIBLE_DATA:
        logger.error("Online fetch failed. Using hardcoded default verse as last resort.")
        try:
            # Wir schreiben den Default-Inhalt, aber laden ihn DIREKT, ohne Rekursion, um den Loop zu vermeiden.
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                f.write(DEFAULT_CONTENT + "\n")

            # Inhalt direkt in BIBLE_DATA laden
            match = re.match(r'([A-Za-z]+\s*\d+:\d+)', DEFAULT_CONTENT)
            if match:
                book_ref = match.group(1).strip()
                lookup_key = f"{book_ref.replace(' ', '').lower()}"
                BIBLE_DATA[lookup_key] = DEFAULT_CONTENT

            logger.info("Successfully loaded default content. Initialization successful.")
            return True

        except Exception:
            logger.error("Failed even to write default content.")
            return False

    return False # Endgültiger Misserfolg


def execute(match_data):
    """
    Executes a search for a specific Bible verse reference using ONLY local data.
    """
    # ... (Rest der execute Funktion bleibt gleich) ...
    if not load_bible_data():
        return "Offline data file is missing. The Bible search cannot be executed."

    logger.info("Starting execution of the 100% OFFLINE Bible search action plugin.")

    try:
        # ... (Extraktionslogik bleibt gleich) ...
        match_obj = match_data['regex_match_obj']
        book_name = match_obj.group('book').strip()
        chapter = match_obj.group('chapter').strip()
        verse = match_obj.group('verse').strip()

        lookup_book = 'joh' if book_name.lower() == 'johannes' else book_name[:3].lower()
        lookup_key = f"{lookup_book}{chapter}:{verse}".lower()

        result = BIBLE_DATA.get(lookup_key)

        if result:
            logger.info(f"Successfully retrieved offline verse for key: {lookup_key}")
            return result
        else:
            return f"Offline verse for {book_name} {chapter}:{verse} was not found in the local file."

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return f"An internal error occurred during offline search: {type(e).__name__}."


if __name__ == "__main__":
    # --- BLOCK REQUIRED FOR CONSOLE FEEDBACK ---

    class DummyMatch:
        def group(self, name):
            if name == 'book': return "Johannes"
            if name == 'chapter': return "3"
            if name == 'verse': return "16"
            return ""

    test_data = {'regex_match_obj': DummyMatch()}

    print("\n--- TEST EXECUTION ---")
    result = execute(test_data)
    print(f"\nRESULT: {result}")
    print("----------------------")
