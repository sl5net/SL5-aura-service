# config/maps/koan_english/01_koan_first_steps/
import re # noqa: F401
from pathlib import Path

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [

    #TODO

    #('hi 02_koan_listen', r'^.*$', 80, {'flags': re.IGNORECASE}),


]

