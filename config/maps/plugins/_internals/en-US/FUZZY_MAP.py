# file config/languagetool_server/maps/en-US/FUZZY_MAP.py

# Map for fuzzy matching. More flexible but slightly slower.
# Format: (replacement_text, text_to_match, required_similarity_score_%)
# A higher score means the typo must be closer to the original text.
#


# The REGEX_MAP is currently kept minimal as most logic moves to the more robust FUZZY_MAP.
# Todo: REGEX_MAP not implemented actually 21.7.'25 07:27 Mon
REGEX_MAP = {
    # This map is processed first for high-priority, exact matches.
}

# Map for fuzzy matching. More flexible but slightly slower.
# Format: (replacement_text, text_to_match_regex, required_similarity_score_%)
# A higher score means the typo must be closer to the original text.
# The regex is anchored (^...$) to ensure it matches the whole phrase.

FUZZY_MAP = [


    # EXAMPLE: period
    ('.', r'\bperiod|full stop|dot|point\b', 95),
    # EXAMPLE: comma
    (',', r'\bcomma\b', 95),
    # EXAMPLE: question mark
    ('?', r'\bquestion mark|christian monk|Christian luck|christian mk|question mk\b', 85),
    # EXAMPLE: exclamation mark
    ('!', r'\bexclamation mark|exclamation point\b', 95),

]
