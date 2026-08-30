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

# config/maps/plugins/game/0ad/move_units/de-DE/FUZZY_MAP_pre.py

# https://regex101.com/

import re
from pathlib import Path as p

CONFIG_DIR = p(__file__).parent

import os as o
from pathlib import Path as p

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())

nach = r'(aller\w*\s+)?(après\s+)?'

# Règles de mouvement directionnel pour 0 après JC

FUZZY_MAP_pre = [

    # seulement


    # EXAMPLE: en haut

    ('kp8', fr'^{nach}(Non[^où]*|seulement|au-dessus de|haut)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # EXAMPLE: vers le bas

    ('kp2', fr'^\s*{nach}(s[Aie]d\w*|ci-dessous|vers le bas)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # EXAMPLE: À droite

    ('kp6', fr'^\s*{nach}(o\w*|droite|droite|droite)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # EXAMPLE: À gauche

    ('kp4', fr'^\s*{nach}(Ouest\w*|merde|gauche)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # EXAMPLE: au nord-est

    ('kp9', fr'^\s*{nach}(nord\w*|Au-dessus de droite|toi utilisé)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # EXAMPLE: au nord-ouest

    ('kp7', fr'^\s*{nach}(nord ouest\w*|donner gauche|Au-dessus de gauche)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # EXAMPLE: au sud-est

    ('kp3', fr'^\s*{nach}(s[Aie]faire\w*|Ci-dessous droite)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # et venteux Linz et à Linz

    # EXAMPLE: au sud-ouest

    ('kp1', fr'^\s*{nach}(s[Aie]dw\w*|ONU[td]\w*( dans)? (Linz|Vienne|venteux)|Ci-dessous gauche)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),


]
