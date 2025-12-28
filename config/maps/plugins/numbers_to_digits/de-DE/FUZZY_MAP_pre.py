# config/maps/plugins/numbers_to_digits/de-DE/FUZZY_MAP_pre.py
# # file config/maps/plugins/spoken_numbers_to_digits/FUZZY_MAP_pr.py
import re

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match (^ ... $)!
    # - first is read first imported, lower rules maybe not get read.



    # EXAMPLE: None
    ('1', r'(\b|\d)(one)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('2', r'(\b|\d)(two)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('3', r'(\b|\d)(three)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('4', r'(\b|\d)(four)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('5', r'(\b|\d)(five)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('6', r'(\b|\d)(six)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('7', r'(\b|\d)(seven)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('8', r'(\b|\d)(eight)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('9', r'(\b|\d)(nine)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('10', r'(\b|\d)(ten)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: None
    ('15', r'(\b|\d)(fifteen)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

#  eins2025-1005-1324 eins eins rein Hi Heinz eins
# 5 3ich 5 fluss 4

    # EXAMPLE: None
    ('0', r'(\b|\d)(null)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('1', r'(\b|\d)(eins)(\b|\d)', 99, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('2', r'(\b|\d)(zwei|Zuruf|zwo|u)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('3', r'(\b|\d)(drei)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('4', r'(\b|\d)(vier)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('5', r'(\b|\d)(fünf)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('6', r'(\b|\d)(sechs|schecks)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('7', r'(\b|\d)(sieben|schieben)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('8', r'(\b|\d)(acht)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('9', r'(\b|\d)(neun)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('10', r'(\b|\d)(zehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('11', r'(\b|\d)(elf)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('12', r'(\b|\d)(zwölf)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('13', r'(\b|\d)(dreizehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('14', r'(\b|\d)(vierzehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('15', r'(\b|\d)(fünfzehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('16', r'(\b|\d)(sechzehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('17', r'(\b|\d)(siebzehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('18', r'(\b|\d)(achtzehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('19', r'(\b|\d)(neunzehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('20', r'(\b|\d)(zwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('21', r'(\b|\d)(einundzwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('22', r'(\b|\d)(zweiundzwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('23', r'(\b|\d)(dreiundzwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('24', r'(\b|\d)(vierundzwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('25', r'(\b|\d)(zip wird zwanzig|fünfundzwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('26', r'(\b|\d)(sechsundzwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('27', r'(\b|\d)(siebenundzwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('28', r'(\b|\d)(achtundzwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('29', r'(\b|\d)(neunundzwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('30', r'(\b|\d)(dreißig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('40', r'(\b|\d)(vierzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('50', r'(\b|\d)(fünfzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('60', r'(\b|\d)(sechzig)(\b|\d)', 78, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('70', r'(\b|\d)(siebzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('80', r'(\b|\d)(achtzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('90', r'(\b|\d)(neunzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('100', r'(\b|\d)(hundert|einhundert)(\b|\d)', 80, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('1000', r'(\b|\d)(tausend)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('2024', r'(\b|\d)(zweitausend\s*vierundzwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('2025', r'(\b|\d)(zweitausend\s*fünfundzwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: None
    ('2026', r'(\b|\d)(zweitausend\s*sechsundzwanzig|zweitausend\s*sechs\s*und\b.*)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
]


