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

# config/maps/plugins/vsp_rt/de-DE/FUZZY_MAP_pre.py

# config/langagetool_server/maps/plugins/vsp_rt/de-DE/FUZZY_MAP_pr.py

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





FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.



    # EXAMPLE: Personnel du PSV

    ('Torsten Hau,Katja Janssens,Harald Uetz,Juliana Kunrad', r'^\b(V\s*S\s*P|V\s*[FS]\s*B)\s*(personne\w+)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Mme la directrice générale

    ('Torsten Hau', r'^\b(V\s*S\s*P|V\s*[FS]\s*B|Femme\s*s\s*p)\s*(Entreprise\w+|Chef)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Directeur Général Loisirs

    ('Torsten Hau ist gerne mit dem MTB unterwegs', r'^(\w+ubis|Loisirs)\b.*(V\s*S\s*P|V\s*[FS]\s*B|Femme\s*s\s*p)\s*(Entreprise\w+|Chef)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),


    # EXAMPLE: M. Schröder

    ('Herr Schröer', r'^(Herr Schröder|Herr hersteller|Herr Schröer|herr schrill)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Schrox

    ('Schröer', r'^(Schrö\w*r|schwör\w*|schworen|schon besorgt)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Ergox Schröx

    ('Ergotherapie Schröer', r'^Ergo\w* (Schrö\w*|schwör\w*|schworen|schon besorgt)\b$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Schröx Ergo

    ('Schröer Ergotherapie', r'^(Schrö\w*|jurer\w*|jurer|déjà inquiet)\b Donc\w*$', 70, # min_accuracy
 {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Donc, plus tôt



]
# Ergothérapie Schröer


