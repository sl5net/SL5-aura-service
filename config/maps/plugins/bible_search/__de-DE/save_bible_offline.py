import logging
import re
from pathlib import Path
# import sys
import time

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "bible_text_lut.txt"

GERMAN_TRANSLATION_CODE = "LUT"
BIBLESCRAPER_URL_BASE = "https://www.bibleserver.com/text/"

# --- Canonical LUTHER66-Buchreihenfolge (korrigierbar/flexibel) ---
BIBLE_STRUCTURE = [
    ("Gen", "Genesis", 50, [31,25,24,26,32,22,24,22,29,32,32,20,18,24,21,16,27,33,38,18,34,24,20,67,34,35,46,22,35,43,55,32,20,31,29,43,36,30,23,23,57,38,34,34,28,34,31,22,33,26]),
    ("Ex",  "Exodus", 40, [22,25,22,31,23,30,25,32,35,29,10,51,22,31,27,36,16,27,25,26,36,31,33,18,40,37,21,43,46,38,18,35,23,35,35,38,29,31,43,38]),
    ("Lev", "Levitikus", 27, [17,16,17,35,19,30,38,36,24,20,47, 8,59,57,33,34,16,30,37,27,24,33,44,23,55,46,34]),
    ("Num", "Numeri", 36, [54,34,51,49,31,27,25,26,35,36,23,33,44,45,41,50,13,32,22,29,35,41,30,25,18,65,23,31,39,17,54,42,56,29,34,13]),
    ("Dtn", "Deuteronomium", 34, [46,37,29,49,33,25,26,20,29,22,32,32,18,29,23,22,20,22,21,20,23,29,26,22,19,19,26,68,29,20,30,52,29,12]),
    # ...
    # Add ALL other books (Jos, Ri, Rt, 1Sam, ... , Offb) --> See next comment for the full structure, or use an importable structure.
    # For brevity, demo includes only a few books. You **MUST FILL OUT** the full structure to get the entire Bible!
    # Use https://github.com/thiagobodruk/bible/blob/master/json/de_luther.json for full structure or Bibelverse.de / biblegateway.com for help.
]

def scrape_and_format_verse(book_abbr, chapter, verse):
    reference_key = f"{book_abbr}{chapter},{verse}"
    full_url = f"{BIBLESCRAPER_URL_BASE}{GERMAN_TRANSLATION_CODE}/{quote(reference_key)}"

    for _try in range(2):
        try:
            response = requests.get(full_url, headers={'User-Agent': 'SL5AuraDownloader/1.0'}, timeout=20)
            if response.status_code != 200:
                logger.error(f"HTTP {response.status_code} for {reference_key}")
                return None

            soup = BeautifulSoup(response.content, 'html.parser')
            verse_element = soup.select_one('div.verse span.text') or soup.select_one('div.verse') or soup.find('span', {'class': 'verse'})
            if verse_element:
                verse_text = verse_element.get_text(separator=' ', strip=True)
            else:
                # 2nd fallback: try regex
                match = re.search(rf'{verse}\s+(.*)', soup.text)
                if match:
                    verse_text = match.group(1).strip()
                else:
                    logger.warning(f"!!! Could not parse verse {reference_key}")
                    return None

            # Clean up verse text
            verse_text = re.sub(r'\s+', ' ', verse_text).strip()
            formatted = f"{book_abbr} {chapter}:{verse} {verse_text}"
            logger.debug(f"Fetched: {formatted}")
            return formatted
        except Exception as e:
            logger.error(f"Exception in {reference_key}: {e}")
            if _try == 0:
                time.sleep(3)
    return None

def dump_full_bible():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        total, failed = 0, 0
        for book_abbr, book_name, chapters_count, verses_per_chapter in BIBLE_STRUCTURE:
            logger.info(f"--- {book_abbr} ({book_name}) ---")
            for chapter in range(1, chapters_count+1):
                verse_count = verses_per_chapter[chapter-1]
                for verse in range(1, verse_count+1):
                    verse_text = scrape_and_format_verse(book_abbr, chapter, verse)
                    if verse_text:
                        f.write(verse_text + "\n")
                        total += 1
                    else:
                        failed += 1
                    time.sleep(1.5)  # polite waiting
                logger.info(f"{book_abbr} {chapter} complete")
        logger.info(f"Done: {total} verses written. {failed} failures.")

if __name__ == "__main__":
    logger.info("Starting full Bible download (Luther)...")
    dump_full_bible()
    logger.info(f"Bible saved to {DATA_FILE}")
