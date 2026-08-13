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

# config/maps/plugins/numbers_to_digits/de-DE/FUZZY_MAP.py

# config/langagetool_server/maps/plugins/ki-maker.space/de-DE/FUZZY_MAP.py

# https://regex101.com/

import re # noqa: F401

# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


FUZZY_MAP = [
    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - signifie que le premier est le plus important, les règles inférieures peuvent ne pas être lues.


    # EXAMPLE: Aucun

    ('5', r'(\b|\d)(cinq)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('6', r'(\b|\d)(six)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('7', r'(\b|\d)(Sept)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('8', r'(\b|\d)(huit)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('9', r'(\b|\d)(neuf)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('10', r'(\b|\d)(dix)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('11', r'(\b|\d)(onze)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('12', r'(\b|\d)(douze)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('13', r'(\b|\d)(treize)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('14', r'(\b|\d)(quatorze)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('15', r'(\b|\d)(quinze)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('16', r'(\b|\d)(seize)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('17', r'(\b|\d)(dix-sept)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('18', r'(\b|\d)(dix-huit)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('19', r'(\b|\d)(dix-neuf)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('20', r'(\b|\d)(vingt)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('30', r'(\b|\d)(trente)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('40', r'(\b|\d)(quarante)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('50', r'(\b|\d)(cinquante)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('60', r'(\b|\d)(soixante)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('70', r'(\b|\d)(soixante-dix)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('80', r'(\b|\d)(quatre-vingts)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('90', r'(\b|\d)(quatre-vingt-dix)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('100', r'(\b|\d)(cent)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Aucun

    ('1000', r'(\b|\d)(mille)(\b|\d)', 87, {'command_flags': re.IGNORECASE}),


]
