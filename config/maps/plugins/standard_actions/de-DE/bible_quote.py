# bible_quote.py

import logging
import sys
from pathlib import Path

# Setup basic logging based on user directive
# NOTE: Since this is a simple action plugin returning text, extensive logging
# inside execute() is often not strictly necessary, but we include the handler structure.
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def execute(match_data):
    """
    Returns a powerful, predefined Bible quote to demonstrate custom text generation
    and specialized vocabulary handling within SL5 Aura.
    """
    logger.info("Starting execution of the Bible quote action plugin.")

    # A hardcoded quote for a reliable and impactful demonstration
    BIBLE_QUOTE = (
        "John 3:16: 'For God so loved the world, that he gave his only begotten Son, "
        "that whosoever believeth in him should not perish, but have everlasting life.'"
    )

    logger.info("Successfully retrieved hardcoded Bible quote.")

    # Returning the string causes SL5 Aura to output the text (e.g., speak it or type it).
    return BIBLE_QUOTE


if __name__ == "__main__":
    # This script is designed to be executed via the STT engine's execute() function,
    # so main() is typically unused unless for isolated testing.
    print(execute(None))
