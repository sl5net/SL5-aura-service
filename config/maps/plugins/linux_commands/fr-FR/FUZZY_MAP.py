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

# config/maps/plugins/linux_commands/de-DE/FUZZY_MAP.py

# https://regex101.com/

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



    # EXAMPLE: Fichier de numéros

    ("nl -ba search_rules.ps1 | sed -n '385,435p'", r'^(Nombre déposer)$', 75, {'command_flags': re.IGNORECASE}),


    ('Brighton', r'^Brighton$'),
    ('Python', r'^(\b)(Brighton|large déjà|Parachute|fouet|fois|titane|Échouer)(\b)$', 75, {'command_flags': re.IGNORECASE}),



    # un peu radial avec les lignes suivantes mais j'aime ça en fait 17.11.'25 16:12 lundi

    # EXAMPLE: Brighton

    ('Python', r'(\b)(Brighton|fouet|titane)(\b)', 75, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Horaires programmés

    ('Python prog', r'\bTimes programme', 80, {'command_flags': re.IGNORECASE}),

    # EXAMPLE: rituel

    ('Virtual environment', r'\b(rituel|Virtuel|virtuel|veuve\w*|veuf|devient déjà|devient difficile|entreprise|sanglier)\w* (dans |blanc |dans le |un )?(Environnement|femme|blanc|weima|métal|blanc|chaud|blanc avec|tourbillon|et Deibel|dans Frotter|frotter|Avis)\w*\b', 75, {'command_flags': re.IGNORECASE}),


]
