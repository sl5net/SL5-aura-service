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

# config/maps/plugins/numbers_to_digits/de-DE/FUZZY_MAP_pre.py


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



    # EXAMPLE: Aucun

    ('1', r'(\b|\d)(un)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('2', r'(\b|\d)(deux)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('3', r'(\b|\d)(trois)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('4', r'(\b|\d)(quatre)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('5', r'(\b|\d)(cinq)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('6', r'(\b|\d)(six)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('7', r'(\b|\d)(Sept)(\b|\d)', 87, # min_accuracy
    {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('8', r'(\b|\d)(huit)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('9', r'(\b|\d)(neuf)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('10', r'(\b|\d)(dix)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Aucun

    ('15', r'(\b|\d)(quinze)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

# one2025-1005-1324 un un dans Salut Heinz un

# 5 3ich 5 rivière 4nlosönun0un zéro cinq


    # EXAMPLE: zéro

    ('0', r'^(zéro|non|donc|aller)$', 87,  # min_accuracy
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: zéro

    ('0', r'(\b|\d)(zéro)(\b|\d)', 87,  # min_accuracy
     {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # EXAMPLE: Aucun

    ('1', r'(\b|\d)(un)(\b|\d)', 99, # min_accuracy
        {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('2', r'(\b|\d)(deux|crier|deux|u)(\b|\d)', 87, # min_accuracy
        {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('3', r'(\b|\d)(trois)(\b|\d)', 87, # min_accuracy
        {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('4', r'(\b|\d)(quatre)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('5', r'(\b|\d)(cinq)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('6', r'(\b|\d)(six|chèques)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('7', r'(\b|\d)(Sept|pousser)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('8', r'(\b|\d)(huit)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('9', r'(\b|\d)(neuf)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('10', r'(\b|\d)(dix)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('11', r'(\b|\d)(onze)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('12', r'(\b|\d)(douze)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('13', r'(\b|\d)(treize)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('14', r'(\b|\d)(quatorze)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('15', r'(\b|\d)(quinze)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('16', r'(\b|\d)(seize)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('17', r'(\b|\d)(dix-sept)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('18', r'(\b|\d)(dix-huit)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('19', r'(\b|\d)(dix-neuf)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('20', r'(\b|\d)(vingt)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('21', r'(\b|\d)(vingt-et-un)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('22', r'(\b|\d)(vingt-deux)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('23', r'(\b|\d)(vingt-trois)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('24', r'(\b|\d)(vingt-quatre)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('25', r'(\b|\d)(fermeture éclair devient vingt|vingt cinq)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('26', r'(\b|\d)(vingt-six)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('27', r'(\b|\d)(vingt-sept)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('28', r'(\b|\d)(vingt-huit)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('29', r'(\b|\d)(vingt-neuf)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('30', r'(\b|\d)(trente)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('40', r'(\b|\d)(quarante)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('50', r'(\b|\d)(cinquante)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('60', r'(\b|\d)(soixante)(\b|\d)', 78, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('70', r'(\b|\d)(soixante-dix)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('80', r'(\b|\d)(quatre-vingts)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('90', r'(\b|\d)(quatre-vingt-dix)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('100', r'(\b|\d)(cent|cent)(\b|\d)', 80, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('1000', r'(\b|\d)(mille)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('2024', r'(\b|\d)(deux mille\s*vingt-quatre)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('2025', r'(\b|\d)(deux mille\s*vingt cinq)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),
    # EXAMPLE: Aucun

    ('2026', r'(\b|\d)(deux mille\s*vingt-six|deux mille\s*six\s*et\b.*)(\b|\d)', 87, # min_accuracy
 {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # JOIN_NUMBERS_EVERYWHERE : rassemble toujours les chiffres s'ils sont adjacents. ne fonctionne pas à pleine puissance (quelque part dans votre chaîne)

    # EXAMPLE: 1 1

    (r'\1', r'(\d)\s+(?=\d)', 95, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),

    # JOIN_NUMBERS_AT_END : rassemble les chiffres si seuls les chiffres/espaces suivent

    # (r'', r'(?=[\d ]+$)(?<=\d)\s+(?=\d)', 95, {'command_flags' : re.IGNORECASE, 'skip_list' : ['LanguageTool']})

    # (r'', r'(?=[\d ]+$)(?<=\d)\s+(?=\d)', 95, {'command_flags' : re.IGNORECASE, 'skip_list' : ['LanguageTool']})


    # SUPPRIMER 1 ESPACE ENTRE 2 CHIFFRES fullmachtch

    # (r'\1\2', r'^(\d+)\s+(\d+)$', 95, {'command_flags' : re.IGNORECASE, 'skip_list' : ['LanguageTool']}),




]


