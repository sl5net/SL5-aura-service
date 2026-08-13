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

# config/maps/plugins/ki-maker-space/de-DE/FUZZY_MAP_pre.py

# config/langagetool_server/maps/plugins/ki-maker.space/de-DE/FUZZY_MAP_pr.py

# https://regex101.com/

import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702




# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.




"""

Mi

 Reboot - Wednesday



Do

Scratch-Thursday

    OpenLab:  11:00 - 22:00 Uhr



Fr

Fabric-Friday:  Feiertag - 3.10.2025

Open Lab ist geschlossen.

DO
Do
Scratch-Thursday
    OpenLab:  11:00 - 22:00 Uhr

Sa

Supercreative-Saturday

"""
FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.


    # ki make espace Réveils AI L'IA à la manière est k Conversation par e-mail Via conversation par e-mail

    # K i Sacks Makerspace KI Sacks Aspen

    # Bloqué par email ki-maker.space


    # EXAMPLE: fabricant de ki

    ('ki-maker.space', r'^(ki-fabricant|ki[\s]*faire[\se]*espace|k i [\s]*faire[\s\w]*espace|espace|ki réveil|IA dans le loin est|IA Sacs tremble|Caïn explosé|K \w*\s*faire espace|IA il|K i \w+ \w*|ki Menkès)\s*\w*$', 60, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Grégor

    ('Gregor Schulte, 07071- 6395627 Gregor.Schulte@ki-maker.space', r'^(Grégor|Schulte|ki-fabricant.espace)\s*\w*$', 80, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Bureau ki-maker.space x

    ('Bulsat', r'^(Bureau ki-fabricant.espace)\s*\w*$', 85, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # Gregor a formé Gregor

    # Par conversation par e-mail K i sacs de respect


]

