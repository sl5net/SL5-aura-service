# config/languagetool_server/maps/plugins/ki-maker.space/de-DE/FUZZY_MAP.py
# https://regex101.com/
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most importend, lower rules maybe not get read.

    ('5', r'(\b|\d)(fünf)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('6', r'(\b|\d)(sechs)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('7', r'(\b|\d)(sieben)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('8', r'(\b|\d)(acht)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('9', r'(\b|\d)(neun)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('10', r'(\b|\d)(zehn)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('11', r'(\b|\d)(elf)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('12', r'(\b|\d)(zwölf)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('13', r'(\b|\d)(dreizehn)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('14', r'(\b|\d)(vierzehn)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('15', r'(\b|\d)(fünfzehn)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('16', r'(\b|\d)(sechzehn)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('17', r'(\b|\d)(siebzehn)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('18', r'(\b|\d)(achtzehn)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('19', r'(\b|\d)(neunzehn)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('20', r'(\b|\d)(zwanzig)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('30', r'(\b|\d)(dreißig)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('40', r'(\b|\d)(vierzig)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('50', r'(\b|\d)(fünfzig)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('60', r'(\b|\d)(sechzig)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('70', r'(\b|\d)(siebzig)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('80', r'(\b|\d)(achtzig)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('90', r'(\b|\d)(neunzig)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('100', r'(\b|\d)(hundert)(\b|\d)', 87, {'flags': re.IGNORECASE}),
    ('1000', r'(\b|\d)(tausend)(\b|\d)', 87, {'flags': re.IGNORECASE}),


]
