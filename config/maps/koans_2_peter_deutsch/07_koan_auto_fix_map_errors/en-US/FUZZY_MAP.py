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

# config/maps/koans_2_peter_deutsch/07_koan_auto_fix_map_errors/de-DE/FUZZY_MAP.py

import re # noqa: F401
# Rule format: ('replacement text', r'pattern', threshold, flags)

# Logic: Top-down, first hit wins. Fullmatch (^...$) stops the pipeline.


# PETER TASK for Koan: 07_koan_auto_fix_map_errors

# No commented out rules found.

# -> Create a meaningful new rule for this koan.

FUZZY_MAP = [
    ('tübingen', 'tübingen'),
    ("hallo", "welt"),
"""
Profozieren Sie einen Fehler.
Schreiben Sie anstelle
    ('tübingen', 'tübingen'),
nur tübingen
Was passiert=
Lernziel:
Automatische Fehlerbehebung in Map-Plugins (z.B. NameError für nicht definierte Variablen)
Umwandlung von "bare words" in gültige Tuples
Header-Cleanup (Dubletten entfernen, Pfade aktualisieren)
"""
]

#





