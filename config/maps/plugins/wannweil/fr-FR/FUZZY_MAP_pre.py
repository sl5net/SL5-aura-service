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

# config/maps/plugins/wannweil/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702



from pathlib import Path

# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', r'regex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'command_flags': re.IGNORECASE} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.


# La Bratwurst serait interne


    # EXAMPLE: Partager des églises

    ('Kirchentellinsfurt', r'\b(églises\s*diviser|Kirchentellinsfurt|tintement tient)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: L'hôtel de ville

    # ('https://www.kirchentellinsfurt.de/de/kontakt', r'\b(L'hôtel de ville|contact)\b\s*\b(églises\s*diviser|Kirchentellinsfurt)\b', 82, # min_accuracy
    # {'command_flags': re.IGNORECASE}),
    #
    # # EXAMPLE: la mairie continue de tinter
    #
    # ('https://www.kirchentellinsfurt.de/de/kontakt', r'\b(la mairie tintement tient)\b', 82, # min_accuracy
    # {'command_flags': re.IGNORECASE}),


# zieglersche https://www.zieglersche.de/altenhilfe.html pflegheim


# La mairie continue de tinter

# Le bruit du bois dur tintant


    # EXAMPLE: qui est un chiot

    ('Wannweil', r'\b(OMS\s*Chiot)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: qui est un chiot

    ('Wannweil', r'\b(OMS\s*Chiot)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),
    # EXAMPLE: Quand parce que

    ('Wannweil', r'^\s*(Quand parce que|Annweiler|Quand\s*parce que|Quand\s*Quand\s*parce que|Quand\s*était\s*Monsieur|Quand\s*était\s*il|À\s*parce que|Quand\s*pleurer\w*|Quand\s*vin|Van\s*parce que|Quand Quoi)\s*$', 70, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: Sébastien coureur

    ('Sebastian Lauffer', r'\bSebastian (Läufer|laufer|Laura|lauf|lauf war)\b', 82, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # EXAMPLE: chiffre

    ('Sigune Lauffer', r'\b(Figur|Sekunde|zugrunde|sigourney|sheego|Sie gute|gun|Ski gute|c gute|Schick ohne|sheikh ohne|gleich ohne|shi gunilla|spione)'
                       # EXAMPLE: coureur

                       r' (coureur|coureur|Lauffer|courir|courir|courir|Laure|courir était|dessus attendez|dans tas|arrêt|nez)\b', 82, {'command_flags': re.IGNORECASE, 'skip_list': ['LanguageTool']}),


    # EXAMPLE: thisRegexWillNeverMatch123ABC

    ('TestFuzzyNiemalsMatchen', r'\b(cette expression régulière ne correspondra jamais123abc)\b', 75, # min_accuracy
    {'command_flags': re.IGNORECASE}),

    # ('TestFuzzyAlways', r'\b(thisRegexWillAlwaysMatch)\b', 1, # min_accuracy{'command_flags' : re.IGNORECASE}),



    # EXAMPLE: Esprits paradigmatiques

    ('pragmatic minds GmbH 2019', r'\b(paradigme Esprits)\b', 75, # min_accuracy
    {'command_flags': re.IGNORECASE}),



]

