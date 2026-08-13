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

# configmaps/koans deutsch/02_koan_listen/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401

# ============================================================
# Koan 02: Your first regex rule – on or off?

# ============================================================
#
# LEARNING GOAL:

# Regex rules can apply multiple spoken words to one

# Map command. Here: Letter groups control "on"/"off".

#
# TASK:

# 1. Remove the '#' before ONE of the two rules below.

# 2. Save - Aura reloads the next time you press the button.

# 3. Say a word that begins with a-m (e.g. "hello")

# or one that begins with n-z (e.g. "water").

#
# EXPECTED RESULT:

# "hello" → "to"

# "water" → "out"

#
# QUESTION FOR THINKING:

# What happens if you activate both rules at the same time?

# Which one will win – and why?

# Tip: Rules are processed from top to bottom.

#
# NEXT STEP: Koan 03

# ============================================================

FUZZY_MAP_pre = [
    # ('an', r'^[a-m]+.*$'),

    # ('off', r'^[n-z]+.*$'),

]
