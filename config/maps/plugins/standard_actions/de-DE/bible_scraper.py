# bible_scraper.py

import logging
import re
import requests
from bs4 import BeautifulSoup
import sys
from pathlib import Path
from urllib.parse import quote

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
GERMAN_TRANSLATION_CODE = "LUT"
BIBLESCRAPER_URL_BASE = "https://www.bibleserver.com/text/"

# German book names mapped to standard German/English references required by Bibleserver
# NOTE: Bibleserver URLs often use German names or common abbreviations (e.g., 'Joh')
GERMAN_BOOK_MAP = {
    'johannes': 'Joh',
    'genesis': 'Gen',
    'matthäus': 'Mt',
    'psalm': 'Ps',
    'lukas': 'Lk',
    'markus': 'Mk',
    # Add common abbreviations here if needed, or stick to full names
}

# --- Core Scraping Logic ---

def scrape_bible_server(book_name, chapter, verse):
    """
    Scrapes the verse text from Bibleserver.com using BeautifulSoup.
    """
    # 1. Map German book name to Bibleserver's abbreviation (e.g., Joh)
    book_abbr = GERMAN_BOOK_MAP.get(book_name.lower(), book_name.title())

    # 2. Construct the URL (e.g., .../LUT/Joh3,16)
    reference = f"{book_abbr}{chapter},{verse}"
    encoded_ref = quote(reference)

    full_url = f"{BIBLESCRAPER_URL_BASE}{GERMAN_TRANSLATION_CODE}/{encoded_ref}"

    logger.info(f"Scraping URL: {full_url}")

    try:
        response = requests.get(full_url, headers={'User-Agent': 'SL5AuraScraper/1.0'}, timeout=10)

        if response.status_code != 200:
            logger.error(f"Scraping failed with HTTP {response.status_code}")
            return f"The Bible service (Bibleserver) is currently unreachable (HTTP {response.status_code})."

        soup = BeautifulSoup(response.content, 'html.parser')

        # 3. Find the verse container (Based on inspection of Bibleserver structure)
        # NOTE: This selector is HIGHLY dependent on the current HTML of Bibleserver!
        # A common class name for the text content is often something like 'verse' or 'text'
        verse_div = soup.find('div', class_='bibletext')
        # *Assuming a general class name here. This might need adjustment after testing.*

        verse_text_parts = []
        reference_found = ""

        if verse_div:
            # Try to find all verse segments inside the main container
            # Bibleserver usually wraps the verse text inside an element with class 'verse-text'
            for verse_span in verse_div.find_all(class_='verse-text'):
                verse_text_parts.append(verse_span.text.strip())

            # Try to extract the canonical reference (e.g., "Johannes 3,16 LUT")
            ref_header = soup.find('h1', class_='passage-title')
            if ref_header:
                 reference_found = ref_header.text.strip()
            else:
                 reference_found = f"{book_name.title()} {chapter}:{verse} ({GERMAN_TRANSLATION_CODE})"

            if verse_text_parts:
                full_text = " ".join(verse_text_parts).strip()
                # Clean up any remaining reference markers or footnotes (if necessary)
                cleaned_text = re.sub(r'\[.*?\]|\{\.*?\}', '', full_text).strip()

                logger.info(f"Successfully scraped reference: {reference_found}")
                return f"{reference_found}: {cleaned_text}"
            else:
                return f"Successfully reached Bibleserver, but could not find verse text for {reference}."

        return f"Could not parse the structure of Bibleserver for reference {reference}."

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during Bible search: {e}")
        return "I encountered a network problem and cannot reach the Bibleserver."
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return f"An internal error occurred during scraping: {type(e).__name__}."


# --- Execute Function (Simplified, English only requested) ---

def execute(match_data):
    """
    Executes a search for a specific Bible verse reference based on the German voice command.
    """
    logger.info("Starting execution of the robust German Bible scraper action plugin.")

    try:
        match_obj = match_data['regex_match_obj']

        # Extract Data using Named Groups
        book_name = match_obj.group('book').strip()
        chapter = match_obj.group('chapter').strip()
        verse = match_obj.group('verse').strip()

        if not book_name or not chapter or not verse:
            return "Please specify the book, chapter, and verse clearly."

        # Perform Search (Scraping)
        result = scrape_bible_server(book_name, chapter, verse)

        logger.info(f"Scraping complete. Result length: {len(result)}")
        return result

    except IndexError:
        return "I could not correctly parse the book, chapter, and verse from your command."
    except Exception as e:
        logger.error(f"Error in execute function: {e}")
        return f"An unexpected error occurred during command processing: {type(e).__name__}."


if __name__ == "__main__":
    # Example test data
    class DummyMatch:
        def group(self, name):
            if name == 'book': return "Johannes"
            if name == 'chapter': return "3"
            if name == 'verse': return "16"
            return ""

    test_data = {'regex_match_obj': DummyMatch()}
    print(execute(test_data))
