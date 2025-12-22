# config/maps/plugins/standard_actions/wikipedia_local/en-US/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.


    # Regel für die WetterabfrageGoogle Jimmy datenGoogle ja bedeutenGoogle ja wiederGucke chapiteau a
    #Google TribüneGoogle Termine Google arm StudioTestGoogle eiche Stühlen TestGoogle Aviv du
    # Gucke gebiete
    # google gemini a chat mit cheminée


]

