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

# config/maps/plugins/volkshochschule_tue/de-DE/FUZZY_MAP.py

# config/langagetool_server/maps/plugins/Volkshochschule/de-DE/FUZZY_MAP.py

import re

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



    # EXAMPLE: Timo Stösser

    ('Timo Stösser', r'\b(thiem\w|timo|thema|ti\w+r)\s+(stäfa|steffen|Stefan|stripper|stefan|stürze\w*|stütze\w*|Sturz|stösse|Schlösser|stöße|stößt|Stöße|stöpsel|stärker|Störche)\b', 70, {'command_flags': re.IGNORECASE}) ,

    # EXAMPLE: Responsable de département

    ('Fachbereichsleitung', r'\bSujet\w*\s+Gestion de zone\b', 70, {'command_flags': re.IGNORECASE}) ,

    # EXAMPLE: PBW textix tx ex livre

    ('Python-Buch', r'\b([PBW]\w+i\w*t\w*e\w* Livre)\b', 60, {'command_flags': re.IGNORECASE}),


    # EXAMPLE: Formation d'instructeur

    ('Kursleiterschulung', r'\b(Instructeur\s*sho\w*)\b', 60, {'command_flags': re.IGNORECASE})



]

