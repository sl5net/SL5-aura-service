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

# config/maps/plugins/game/0ad/gather/de-DE/FUZZY_MAP_pre.py

import os as o
import re
from pathlib import Path as p

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())

# https://regex101.com/


CONFIG_DIR = p(__file__).parent

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())

baum = r'arbre|Pourquoi'

FUZZY_MAP_pre = [

    # EXAMPLE: bois

    ('gather wood',
     fr'^(rassembler\s*)?(bois|obtenir\w*|rouler|Rhön|Ouah|aujourdhui|calme|pont|ponts|{baum}|arbres|arbre|rouler|ranch|rouge|Ruiz|rots|nous)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
     }),

    # inégalé est ajouté à votre carte (331)

    # asldfkjasödlfsa dfanother testasdfsjdflksdöfsdj

    # sdddfgd festasdsdsadfsdf asdfasödkfjashfdasdfsadfsdfskates


    # football, voiture, football


    # EXAMPLE: fruit

    ('gather fruit',
     r'^\s*(il|b|baie\w*|Gehring|facture|bière|bébé|fruit|fruit|fruit[n]?|Pommes[n]?|Pomme|Poire[n]?|baies|carrière)\s*$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
         # 'cache' : Faux

     }),

    # \w+ \w*a\w+fr


    # EXAMPLE: viande

    ('gather meat',
     r'^(viande|chasse|chasse|\w+ \w*a\w+fr|\w+ \w+a\w+fr|vestes|Oui|Oui bien|son avoir|viande|météo|lequel Amen|monter|volé|\w+\s\boser|nous avait)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
     }),

    # EXAMPLE: pierre

    ('gather stone',
     r'^(rassembler\s*)?(pierre\w*|dedans|augmenter\w*|acier|ville|aiguillon|arrêt|commencer|commencer|écurie|dérange|se lève|différend|peine|rocher|rocher|carrière|pierre)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
         # 'cache' : Faux

     }),

    # Pour l'instant, la carte actuelle, Dance is, semble digne


    # EXAMPLE: métal

    ('gather metal',
     r'^(rassembler\s*)?(rencontré\w+|tapis\w+|métal|or|irrité|avec|citation|métal|célibataire|matcha|Gunther|éthan|Italie|avec métal|poison)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
     }),


]
