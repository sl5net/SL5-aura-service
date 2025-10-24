# config/languagetool_server/maps/plugins/web-radio-funk/de-DE/FUZZY_MAP_pr.py
# https://regex101.com/
import re # noqa: F401

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


    # deutsche radio

    ('https://www.deutschlandradio.de/streamingdienste-100.html', r'^(deutschlandfunk|Deutschlandradio|deutsch\w* radio)\s*$', 70, {'flags': re.IGNORECASE}),
]

