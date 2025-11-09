# bible_search.py

import logging
# import re
import requests
#import sys
#from pathlib import Path
from urllib.parse import quote

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
BIBLE_API_URL = "https://bible-api.com/"
# Default stable translation is KJV
DEFAULT_TRANSLATION = "kjv"

# No mapping needed, as input books are expected to be in English (e.g., 'John')
# We keep a placeholder map for consistency, but it's not strictly necessary here.
ENGLISH_BOOK_MAP = {}

# --- Core Logic ---

def search_bible_api(book_name, chapter, verse):
    """Fetches a specific Bible verse from the API using the default English translation (KJV)."""

    # Ensure the book name is title-cased for best API compatibility
    english_book = book_name.title()

    # Format the reference string for the API (e.g., "John 3:16")
    reference = f"{english_book} {chapter}:{verse}"
    encoded_ref = quote(reference)

    # Build URL using the default stable translation (kjv)
    full_url = f"{BIBLE_API_URL}{encoded_ref}?translation={DEFAULT_TRANSLATION}"

    logger.info(f"API Lookup URL: {full_url}")

    try:
        response = requests.get(full_url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if 'error' in data:
                logger.warning(f"API error for {reference}: {data['error']}")
                return f"I found the book '{english_book}', but the reference {chapter}:{verse} was not found."

            if data and data.get('text'):
                verse_text = data['text'].strip()
                translation = data.get('translation_name', DEFAULT_TRANSLATION)

                return f"Reference {data['reference']} ({translation}): {verse_text}"

            return f"The Bible API returned empty data for '{reference}'."

        else:
            logger.error(f"API request failed with status code {response.status_code}")
            return f"The external Bible service is currently unreachable (HTTP {response.status_code})."

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during Bible search: {e}")
        return "I encountered a network problem and cannot reach the Bible service."
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return f"An internal error occurred during search: {type(e).__name__}."


def execute(match_data):
    """
    Executes a search for a specific Bible verse reference based on the English voice command.
    """
    logger.info("Starting execution of the robust English Bible search action plugin.")

    try:
        match_obj = match_data['regex_match_obj']

        # Extract Data using Named Groups defined in the map file
        book_name = match_obj.group('book').strip()
        chapter = match_obj.group('chapter').strip()
        verse = match_obj.group('verse').strip()

        if not book_name or not chapter or not verse:
            return "Please specify the book, chapter, and verse clearly."

        # Perform Search (No dynamic language determination needed)
        result = search_bible_api(book_name, chapter, verse)

        logger.info(f"Search complete. Result length: {len(result)}")
        return result

    except IndexError:
        return "I could not correctly parse the book, chapter, and verse from your command."
    except Exception as e:
        logger.error(f"Error in execute function: {e}")
        return f"An unexpected error occurred during command processing: {type(e).__name__}."


if __name__ == "__main__":
    # Example test data (assuming the regex matched these groups)

    #test_data = {'regex_match_obj': DummyMatch()}
    print('execute(test_data)')
