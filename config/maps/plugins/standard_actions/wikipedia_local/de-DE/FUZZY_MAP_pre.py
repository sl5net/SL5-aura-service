# config/maps/plugins/standard_actions/wikipedia_local/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

CONFIG_DIR = Path(__file__).parent

wikipedia = r"\s*\b(?:wikipedia|pedia|wiki|pedi|wik|pe|suche auf wikipedia nach)\b\s*"

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match (^ ... $)!
    # - first is read first imported, lower rules maybe not get read.

    # EXAMPLE:  was ist ein haus
    ("Wiki was ist ein haus (Begriffsklärung)", rf'^{wikipedia}was ist (ein|dein|den) haus$', 90,
     {
    'flags': re.IGNORECASE,
    'skip_list': ['LanguageTool','fullMatchStop'],
    }),


    # EXAMPLE: Computer
    ('', rf'^(?!Computer|Aura){wikipedia}(?:suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| dein| den| die| das| der| Herr)* (?P<search>.*)', 90, { 'flags': re.IGNORECASE,
     'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
    }),


    #

    # EXAMPLE: Computer
    ('', rf'^(?!Computer|Aura){wikipedia}(?: ein| die| das| der| Herr)? (?P<search>.*)', 90, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
    }),




    #  config/maps/plugins/standard_actions/wikipedia_local/de-DE/FUZZY_MAP_pre.py:251




]

