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

# config/maps/plugins/volkshochschule_tue/de-DE/FUZZY_MAP_pre.py

# config/langagetool_server/maps/plugins/Volkshochschule/de-DE/FUZZY_MAP_pr.py

import re

# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


"""
Important: Please apply the regular expressions in the correct order.

You must use the composite (more general) regular expression first, and then apply the specialized one.

The reason is that if the shorter, specialized regex runs first, it might match a part of the string that is essential for the larger, composite regex. This would make it impossible for the composite regex to find its match afterwards.
"""

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.

    # EXAMPLE: texte du titre

    ('Timo Stösser', r'^(ti\w+r|T\w+i\w+o)\s+(stäfa|steffen|stripper|stefan|stürz\w*|stötz\w*|Sturz|stösse|Stoffe|Schlösser|stöße|stöpsel|Störche)$', 7, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: texte du titre

    ('Timo', r'\b(ti\w+r|T\w+i\w+o)\b', 70, {'command_flags': re.IGNORECASE,
        'only_in_windows': [r'e-mail',r'gmail',r'e-mail',r'boîte de réception']}),

    # EXAMPLE: Stäfa

    ('Stösser', r'^(stäfa|steffen|stripper|stefan|stürz\w*|stötz\w*|Sturz|stösse|Schlösser|stöße|stöpsel|Störche)$', 70, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: chef de département

    ('Fachbereichsleitung', r'^(chef de département)$', 60, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: livre texte

    ('Python-Buch', r'^(\w+t\wn Livre)$', 60, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Livre Python

    ('Python-Buch', r'^(Python Livre)$', 60, {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Livre de texte Btextixt

    ('Python-Buch', r'^(B\w+i\poids\w+ Livre)$', 60, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Livre Python

    ('Python-Buch', r'^([PBW]\w+i\w*t\w*e\w* Livre)$', 60, {'command_flags': re.IGNORECASE}),

    # ("Formation d'instructeur de cours", r'^(Instructeur de cours\s*schu\w*| Formation de conférencier Formation de conférencier)$', 60, {'command_flags': re.IGNORECASE})


    # EXAMPLE: Instructeur

    ('Kursleiterschulung', r'^(Instructeur|Conférenciers)[\w\s]*(\s*sho\w*|Formation continue)$', 60, {'command_flags': re.IGNORECASE})

]

# Timo Stösser



# Livre Python de formation d'instructeur, chef de département

# Livre Python Livre large Livre Python Livre Python dans le livre

# Brighton Book Python Book Whip Book Wide BookTimoTchibo Plunge

# Deuxième livre At Dead Book Python Book Wide Book Wide Book Python Book

# Livre de salutations

# Livre Python

