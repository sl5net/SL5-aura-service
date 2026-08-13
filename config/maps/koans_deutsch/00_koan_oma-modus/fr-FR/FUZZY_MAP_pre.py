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
# aussi<-de

FUZZY_MAP_pre = [
    ('oma', '^oma$'),
]

# Pour en savoir plus : docs/FuzzyMapRuleGuide.mdFUZZY_MAP_pre = [



# ============================================================
# Koan 00 : Mode Granny — Règles sans syntaxe

# ============================================================

#
# IDÉE:

# Vous n'avez pas besoin de connaître de règles (regex). Écrivez-en juste un seul

# Word — sans guillemets.


# Aura le détecte et le corrige automatiquement à un

# règle valide.

#
# TÂCHE:

# 1. Ajoutez un seul mot sous cette ligne, par exemple :

# fleur

# 2. Parlé sous forme de fichier Word.

# 3. Dites un mot

#
# PROCHAINE ÉTAPE :

# Changez le mot en tuple avec sa propre sortie :

# ('framboise', '^flower$', 0, {'command_flags' : re.IGNORECASE})

