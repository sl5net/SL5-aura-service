# config/maps/koans_english/01_koan_first_steps/en-US/FUZZY_MAP_pre.py
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

BTW = """
'... regular expressions began in the 1950s... Different syntaxes for writing regular expressions have existed since the 1980s, one being the POSIX standard and another, widely used, being the Perl syntax.
... Regular expressions are used in search engines, in search and replace dialogs of word processors and text editors, in text processing utilities ... and in lexical analysis. Regular expressions are supported in many programming languages. '
( https://en.wikipedia.org/wiki/Regular_expression )

You probably know it already somehow or a part of it.
"""












FUZZY_MAP_pre = [

    #TODO
    # ('1 ', r'hi'),

    # ('2 ', r'.*'),




]

