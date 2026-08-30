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

# config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py

import re

# depuis pathlib import Path as p;import os as o

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())





# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


# aussi<-de

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.


    # Cumul : les règles (s'accumulent) de sorte que seule la dernière règle soit visible. Exemples :


    # La règle suivante s'applique à tout :

    # ('---', r'^.*$', 5, # min_accuracy {'command_flags': re.IGNORECASE}),


    # La règle suivante s'applique à tout sauf au mot maison :

    # EXAMPLE: Maison

    # ('', r'^(?!Haus).*$', 5, {'command_flags': re.IGNORECASE}),

    # TestTestTestMaisonMaisonMaisonFemme deMaison Arbre sousBonne journéeÉchec et matÉchec et mat

    # Échec et matÉchec et mat


    # La règle suivante s'applique à tout sauf aux mots check, mate :

    # EXAMPLE: Échecs

    # ('', r'^(?!check|mate|bad|house).*$', 5, {'command_flags': re.IGNORECASE}),

    # ÉchecsÉchecsMaisonÉchecsÉchecsSalle de bain

    # Échec et mat


    # EXAMPLE: Échecs

    # ('Checkmate', r'^(Checkmate|bad|House).*$', 5, {'command_flags': re.IGNORECASE}),

    # Échec et matÉchec et mat




    ('LECKER_EXAKT', 'Marmelade', 100, {'command_flags': re.IGNORECASE}),
    # Jam JamLECKER_EXAKT


    # Test 2 : Règle de tolérance (erreurs de frappe autorisées)

    # Il faut également reconnaître 'Marmelada' ou 'Marmelad'.

    # ('LECKER_FUZZY', 'JAM', 1, {'command_flags' : re.IGNORECASE}),


    # Confiture Mammon Mammon Mama Marion Málaga

    # Maman MarionA est maigre





]
