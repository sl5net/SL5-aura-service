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
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.


    ('1', r'(\b|\d)(one)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('2', r'(\b|\d)(two)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('3', r'(\b|\d)(three)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('4', r'(\b|\d)(four)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('5', r'(\b|\d)(five)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('6', r'(\b|\d)(six)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('7', r'(\b|\d)(seven)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('8', r'(\b|\d)(eight)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('9', r'(\b|\d)(nine)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('10', r'(\b|\d)(ten)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    ('15', r'(\b|\d)(fifteen)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

#  eins2025-1005-1324 eins eins rein Hi Heinz eins

    ('0', r'(\b|\d)(null)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('1', r'(\b|\d)(eins)(\b|\d)', 99, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('2', r'(\b|\d)(zwei)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('3', r'(\b|\d)(drei)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('4', r'(\b|\d)(vier)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('5', r'(\b|\d)(fünf)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('6', r'(\b|\d)(sechs)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('7', r'(\b|\d)(sieben)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('8', r'(\b|\d)(acht)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('9', r'(\b|\d)(neun)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('10', r'(\b|\d)(zehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('11', r'(\b|\d)(elf)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('12', r'(\b|\d)(zwölf)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('13', r'(\b|\d)(dreizehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('14', r'(\b|\d)(vierzehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('15', r'(\b|\d)(fünfzehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('16', r'(\b|\d)(sechzehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('17', r'(\b|\d)(siebzehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('18', r'(\b|\d)(achtzehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('19', r'(\b|\d)(neunzehn)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('20', r'(\b|\d)(zwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('30', r'(\b|\d)(dreißig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('40', r'(\b|\d)(vierzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('50', r'(\b|\d)(fünfzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('60', r'(\b|\d)(sechzig)(\b|\d)', 78, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('70', r'(\b|\d)(siebzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('80', r'(\b|\d)(achtzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('90', r'(\b|\d)(neunzig)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('100', r'(\b|\d)(hundert|einhundert)(\b|\d)', 80, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    ('1000', r'(\b|\d)(tausend)(\b|\d)', 87, {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
]
#  60 50witzig 13Drei SSW 2018 17Zweck ziehen 16100
#  1000Ein HuhnEin wundenEin wunderEin wunderEin unnützEin runde 90 80 70Schwächt sich


