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

# config/maps/koans_deutsch/00_koan_oma-modus/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401

# too<-from

FUZZY_MAP_pre = [
    ('oma', '^oma$'),
]

# More about this: docs/FuzzyMapRuleGuide.mdFUZZY_MAP_pre = [



# ============================================================
# Koan 00: Granny Mode — Rules Without Syntax

# ============================================================

#
# IDEA:

# You don't need to know any rules (regex). Just write a single one

# Word — without quotation marks.


# Aura detects it and automatically corrects it to one

# valid rule.

#
# TASK:

# 1. Add a single word below this line, e.g.:

# flower

# 2. Spoke as a word file.

# 3. Say a word

#
# NEXT STEP:

# Change the word to a tuple with its own output:

# ('raspberry', '^flower$', 0, {'command_flags': re.IGNORECASE})

