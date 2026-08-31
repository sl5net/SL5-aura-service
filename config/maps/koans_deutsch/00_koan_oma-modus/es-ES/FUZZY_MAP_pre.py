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

# Mehr dazu: docs/FuzzyMapRuleGuide.mdFUZZY_MAP_pre = [



# ============================================================
# Koan 00: Oma-Modus — Regeln ohne Syntax

# ============================================================

#
# IDEE:

# Du musst keine Regeln (Regex) kennen. Schreib einfach ein einzelnes

# Wort — ohne Anführungszeichen.


# Aura erkennt es und korrigiert es automatisch zu einer

# gültigen Regel.

#
# AUFGABE:

# 1. Füge unter dieser Zeile ein einzelnes Wort ein, z.B.:

# Blume

# 2. Speiche als Wortatei.

# 3. Sprich ein Wort

#
# NÄCHSTER SCHRITT:

# Ändere das Wort zu einem Tupel mit eigener Ausgabe:

# ('Himbeere', '^Blume$', 0, {'command_flags': re.IGNORECASE})

