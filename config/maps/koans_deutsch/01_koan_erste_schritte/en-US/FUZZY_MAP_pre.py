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

# configmaps/koans deutsch/01_koan_erste_stiege/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401

# too<-from

FUZZY_MAP_pre = [

# ============================================================
# Koan 01: Your first rule – Welcome to Aura!

# ============================================================
#
# Requirement: Aura is already running and your hotkey is configured.

# If not: see docs/GettingStarted.md

#
# TASK:

# Remove the '#' in front of the rule below (line with 'hello world').

# Save the file. Aura loads the rule on the next key press

# (Hotkey trigger) automatically new - in idle mode, Aura sleeps completely.

# Then press your hotkey and say: "hello world"

#
# EXPECTED RESULT:

# Aura types: “Hello World 01”

#
# WHY DOES THE PIPELINE STOP AFTER THIS?

# The pattern r'^.*$' fits EVERYTHING. As soon as this rule applies,

# no further rule is checked. This is the “Full Match Stop”.

# More about this: docs/FuzzyMapRuleGuide.md

#
# ============================================================

    # ('Hello world 01', r'^hello world$', 0, {'command_flags': re.IGNORECASE}),

]
