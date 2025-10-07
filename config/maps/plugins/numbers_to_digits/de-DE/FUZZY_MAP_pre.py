# # file config/maps/plugins/spoken_numbers_to_digits/FUZZY_MAP_pr.py
import re

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use re.IGNORECASE for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.


    ('1', r'(\b|\d)(one)(\b|\d)', 80, re.IGNORECASE),
    ('2', r'(\b|\d)(two)(\b|\d)', 80, re.IGNORECASE),
    ('3', r'(\b|\d)(three)(\b|\d)', 80, re.IGNORECASE),
    ('4', r'(\b|\d)(four)(\b|\d)', 80, re.IGNORECASE),
    ('5', r'(\b|\d)(five)(\b|\d)', 80, re.IGNORECASE),
    ('6', r'(\b|\d)(six)(\b|\d)', 80, re.IGNORECASE),
    ('7', r'(\b|\d)(seven)(\b|\d)', 80, re.IGNORECASE),
    ('8', r'(\b|\d)(eight)(\b|\d)', 80, re.IGNORECASE),
    ('9', r'(\b|\d)(nine)(\b|\d)', 80, re.IGNORECASE),
    ('10', r'(\b|\d)(ten)(\b|\d)', 80, re.IGNORECASE),

    ('15', r'(\b|\d)(fifteen)(\b|\d)', 80, re.IGNORECASE),

#  eins2025-1005-1324 eins

    ('0', r'(\b|\d)(null)(\b|\d)', 80, re.IGNORECASE),
    ('1', r'(\b|\d)(eins)(\b|\d)', 80, re.IGNORECASE),
    ('2', r'(\b|\d)(zwei)(\b|\d)', 80, re.IGNORECASE),
    ('3', r'(\b|\d)(drei)(\b|\d)', 80, re.IGNORECASE),
    ('4', r'(\b|\d)(vier)(\b|\d)', 80, re.IGNORECASE),
    ('5', r'(\b|\d)(fünf)(\b|\d)', 80, re.IGNORECASE),
    ('6', r'(\b|\d)(sechs)(\b|\d)', 80, re.IGNORECASE),
    ('7', r'(\b|\d)(sieben)(\b|\d)', 80, re.IGNORECASE),
    ('8', r'(\b|\d)(acht)(\b|\d)', 80, re.IGNORECASE),
    ('9', r'(\b|\d)(neun)(\b|\d)', 80, re.IGNORECASE),
    ('10', r'(\b|\d)(zehn)(\b|\d)', 80, re.IGNORECASE),
    ('11', r'(\b|\d)(elf)(\b|\d)', 80, re.IGNORECASE),
    ('12', r'(\b|\d)(zwölf)(\b|\d)', 80, re.IGNORECASE),
    ('13', r'(\b|\d)(dreizehn)(\b|\d)', 80, re.IGNORECASE),
    ('14', r'(\b|\d)(vierzehn)(\b|\d)', 80, re.IGNORECASE),
    ('15', r'(\b|\d)(fünfzehn)(\b|\d)', 80, re.IGNORECASE),
    ('16', r'(\b|\d)(sechzehn)(\b|\d)', 80, re.IGNORECASE),
    ('17', r'(\b|\d)(siebzehn)(\b|\d)', 80, re.IGNORECASE),
    ('18', r'(\b|\d)(achtzehn)(\b|\d)', 80, re.IGNORECASE),
    ('19', r'(\b|\d)(neunzehn)(\b|\d)', 80, re.IGNORECASE),
    ('20', r'(\b|\d)(zwanzig)(\b|\d)', 80, re.IGNORECASE),
    ('30', r'(\b|\d)(dreißig)(\b|\d)', 80, re.IGNORECASE),
    ('40', r'(\b|\d)(vierzig)(\b|\d)', 80, re.IGNORECASE),
    ('50', r'(\b|\d)(fünfzig)(\b|\d)', 80, re.IGNORECASE),
    ('60', r'(\b|\d)(sechzig)(\b|\d)', 80, re.IGNORECASE),
    ('70', r'(\b|\d)(siebzig)(\b|\d)', 80, re.IGNORECASE),
    ('80', r'(\b|\d)(achtzig)(\b|\d)', 80, re.IGNORECASE),
    ('90', r'(\b|\d)(neunzig)(\b|\d)', 80, re.IGNORECASE),
    ('100', r'(\b|\d)(hundert)(\b|\d)', 80, re.IGNORECASE),
    ('1000', r'(\b|\d)(tausend)(\b|\d)', 80, re.IGNORECASE),
]



