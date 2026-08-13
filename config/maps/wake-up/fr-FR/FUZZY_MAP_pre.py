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

# config/maps/wake-up/de-DE/FUZZY_MAP_pre.py

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


#

CONFIG_DIR = Path(__file__).parent

# aura = r'\s*\b(busch|ordinateur|aura|auri|voss|voß|vosk|volk|vor sk|first|frost|froscon|free esc| Frist|feuer)\b\s*'

# je m'endors pratiquement, comment ça se passe ?

# endormez-en un gratuitement maintenant



# wakeword = r'{nonsense_word}(kaktus|kaktos|caca|kraft|récemment|taktus|capitaine|voss|frost|table pliante|pratique|panier|comme un voyage).*'


# config/maps/wake-up/de-DE/FUZZY_MAP_pre.py:24

nonsense_start_word = r'(?:(un|un|un)\s*)?'
wakeword = r'{nonsense_word}(télescope|se produit|Tedesco|violoncelliste|tennis|touristique|crédit).*'


# STT Actif. Drapeau muet supprimé. Ce qui a, crache


#

FUZZY_MAP_pre = [

    # bonne journée, allume le cactus qui se réveille 🌵

    # Je me réveille avec un télescope 🌵


    # EXAMPLE: wakeword n'écoute pas

    ('voss_start', fr'^({wakeword} écouter pas avec|{wakeword}éveillé sur|{wakeword}sur|{wakeword}réveillez-vous|{wakeword}garde|{wakeword}évaluer|{wakeword}allumer|{wakeword}actif|gel cassé craquelin|Avant accident sur|gratuit carré sur|gel absurdité sur|bien jour le réveillez-vous|{nonsense_start_word}télescope semaine de|b\s*\w*\s*\bcactus réveillez-vous)$', 89,
     {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    # 1 frapper les têtes 2 le redresser 2 pratique

    # je me suis récemment endormi

    # tu te voyais t'endormir

    #

    # EXAMPLE: endormez-vous avec des interprétations phonétiques erronées 🌵

    ('voss_stop', fr'^(?:{wakeword}|gratuit|têtes|entendu)\s*(?:frapper|sendormir|glisser|y compris\w*fr|fermé|Arrêt|temple|ciao).*$', 89,
     {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    # un 🌵

    # EXAMPLE: arrêt du mot de réveil

    ('voss_stop', fr'^(?:{wakeword}Arrêt\w*|{nonsense_start_word}{wakeword}{nonsense_start_word}temple\w*|{wakeword}aller temple\w*|bien nuit|{wakeword}ciao|{wakeword}nen)$', 89,
     {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),

    # tu en as entendu un s'endormir

    # e

    # EXAMPLE: nonsense_start_word t'a entendu t'endormir

    ('voss_stop', fr'^{nonsense_start_word}\s*(entendu sendormir|voir pourrait sendormir)$', 89,
     {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),
    # 18:40:16,502 - INFO - 📢📢📢 ######################## mis gratuitement #######################################

    # stramg j'ai dit kakrus et ça se désiste gratuitement...

    # EXAMPLE: fermé gratuitement

    ('voss_stop', r'^(gratuit) (fermé|ensemble)$', 89,
    {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'set_vosk_active.py']
    }),



]
#
# Le jury était éveillé, le jury était éveillé

# Le jury se réveilleohComputerwocheLe jury se réveille

# PoingsGivre éveilléSTT Actif. Indicateur muet supprimé.


