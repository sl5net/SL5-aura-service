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

# config/maps/plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py

# fichier config/maps/plugins/digits_to_numbers/FUZZY_MAP_pr.py

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

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.


    # 1 2 3 un 2 3 essai

    #

    # EXAMPLE: b 0 b

    ('null', r'\b(0)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b1b

    ('one', r'\b(1)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b2b

    ('two', r'\b(2)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b3b

    ('three', r'\b(3)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b4b

    ('four', r'\b(4)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b5b

    ('five', r'\b(5)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b6b

    ('six', r'\b(6)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b7b

    ('seven', r'\b(7)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b8b

    ('eight', r'\b(8)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b9b

    ('nine', r'\b(9)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 10

    ('ten', r'\b(10)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 15

    ('fifteen', r'\b(15)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b 0 b

    ('null', r'\b(0)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: b1b

    ('eins', r'\b(1)\b', 100, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b2b

    ('zwei', r'\b(2)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b3b

    ('drei', r'\b(3)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b4b

    ('vier', r'\b(4)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b5b

    ('fünf', r'\b(5)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b6b

    ('sechs', r'\b(6)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b7b

    ('sieben', r'\b(7)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b8b

    ('acht', r'\b(8)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: b9b

    ('neun', r'\b(9)\b', 100, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 10

    ('zehn', r'\b(10)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 11

    ('elf', r'\b(11)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 12

    ('zwölf', r'\b(12)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 13

    ('dreizehn', r'\b(13)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 14

    ('vierzehn', r'\b(14)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 15

    ('fünfzehn', r'\b(15)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 16

    ('sechzehn', r'\b(16)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 17

    ('siebzehn', r'\b(17)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 20

    ('zwanzig', r'\b(20)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 30

    ('dreißig', r'\b(30)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 40

    ('vierzig', r'\b(40)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 50

    ('fünfzig', r'\b(50)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 60

    ('sechzig', r'\b(60)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 70

    ('siebzig', r'\b(70)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 80

    ('achtzig', r'\b(80)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 90

    ('neunzig', r'\b(90)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 100

    ('hundert', r'\b(100)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),
    # EXAMPLE: 1000

    ('tausend', r'\b(1000)\b', 89, # min_accuracy
 {'command_flags': re.IGNORECASE}),


]



