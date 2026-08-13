# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/volkshochschule_tue/de-DE/FUZZY_MAP_pre.py

# config/languagetool_server/maps/plugins/Volkshochschule/de-DE/FUZZY_MAP_pr.py

import re

# This map uses a hybrid approach:

# 1. Regex entries are checked first. They are powerful and can be case-insensitive.

# Structure: ('replacement', r'regex_pattern', threshold, flags)

# - The threshold is ignored for regex.

# - flags: Use {'command_flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.

# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.


"""
Important: Please apply the regular expressions in the correct order.

You must use the composite (more general) regular expression first, and then apply the specialized one.

The reason is that if the shorter, specialized regex runs first, it might match a part of the string that is essential for the larger, composite regex. This would make it impossible for the composite regex to find its match afterwards.
"""

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.

    # Important to know:

    # - it stops with first full match. Examples: ^...$ = Full Match = Stop Criterion!

    # - first is read first imported, lower rules maybe not get read.

    # EXAMPLE: title textr

    ('Timo Stösser', r'^(ti\w+r|T\w+i\w+o)\s+(stäfa|steffen|stripper|stefan|stürz\w*|stötz\w*|Sturz|stösse|Stoffe|Schlösser|stöße|stöpsel|Störche)$', 7, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: title textr

    ('Timo', r'\b(ti\w+r|T\w+i\w+o)\b', 70, {'command_flags': re.IGNORECASE,
        'only_in_windows': [r'email',r'gmail',r'email',r'inbox']}),

    # EXAMPLE: Stäfa

    ('Stösser', r'^(stäfa|steffen|stripper|stefan|stürz\w*|stötz\w*|Sturz|stösse|Schlösser|stöße|stöpsel|Störche)$', 70, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: department head

    ('Fachbereichsleitung', r'^(department head)$', 60, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: texttxn book

    ('Python-Buch', r'^(\w+t\wn Book)$', 60, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Python book

    ('Python-Buch', r'^(Python Book)$', 60, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Btextixttext book

    ('Python-Buch', r'^(B\w+i\wt\w+ Book)$', 60, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Python book

    ('Python-Buch', r'^([PBW]\w+i\w*t\w*e\w* Book)$', 60, {'command_flags': re.IGNORECASE}),

    # ('Course instructor training', r'^(Course instructor\s*schu\w*| Lecturer training Lecturer training)$', 60, {'command_flags': re.IGNORECASE})


    # EXAMPLE: Instructor

    ('Kursleiterschulung', r'^(Instructor|Lecturers)[\w\s]*(\s*sho\w*|Further training)$', 60, {'command_flags': re.IGNORECASE})

]

# Timo Stösser



# Instructor training Python book, department head

# Python book wide book Python book Python book at in the book

# Brighton Book Python Book Whip Book Wide BookTimoTchibo Plunge

# Second Book At Dead Book Python Book Wide Book Wide Book Python Book

# Cheers book

# Python book

