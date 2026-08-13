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

# config/maps/plugins/game/dealers_choice/de-DE/FUZZY_MAP_pre.py

# config/dealers_choice/maps/FUZZY_MAP_pre.py

import re

# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - signifie que le premier est le plus important, les règles inférieures peuvent ne pas être lues.


    # EXAMPLE: appel

    ('c', r'^\s*(appel|vérifier)\s*$', 85, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: augmenter s

    ('r', r'^\s*(raise)\s*$', 85, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: plier s

    ('f', r'^\s*(pli)\s*$', 85, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: jeter s

    ('d', r'^\s*(jeter)\s*$', 85, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: parier s

    ('b', r'^\s*(pari)\s*$', 85, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: échange m

    ('x', r'^\s*(échange)\s*$', 85, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # Touches de montant

    # EXAMPLE: 100

    ('1', r'^\s*(100|un cent)\s*$', 85, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 280

    ('2', r'^\s*(280|deux cinquante)\s*$', 85, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 80

    ('3', r'^\s*(80|cinquante)\s*$', 85, # min_accuracy
 {'command_flags': re.IGNORECASE}),


]
