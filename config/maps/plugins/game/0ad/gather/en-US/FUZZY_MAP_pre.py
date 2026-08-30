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

baum = r'tree|Why'

FUZZY_MAP_pre = [

    # EXAMPLE: wood

    ('gather wood',
     fr'^(gather\s*)?(wood|get\w*|roll|rhön|wow|today|quiet|bridge|bridges|{baum}|trees|tree|roll|ranch|red|ruiz|burps|us)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
     }),

    # unmatched is added to your map (331)

    # asldfkjasödlfsa dfanother testasdfsjdflksdöfsdj

    # sdddfgd festasdsdsadfsdf asdfasödkfjashfdasdfsadfsdfskates


    # football car football


    # EXAMPLE: fruit

    ('gather fruit',
     r'^\s*(he|b|berry\w*|Gehring|bill|beer|baby|fruit|fruit|fruit[n]?|Apples[n]?|Apple|Pear[n]?|berries|quarry)\s*$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
         # 'cache': False

     }),

    # \w+ \w*a\w+en


    # EXAMPLE: meat

    ('gather meat',
     r'^(meat|hunting|hunting|\w+ \w*a\w+en|\w+ \w+a\w+en|jackets|Yes|Yes good|her have|meat|weather|which Amen|ride|stollen|\w+\s\dare|we had)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
     }),

    # EXAMPLE: stone

    ('gather stone',
     r'^(gather\s*)?(stone\w*|in it|rise\w*|steel|city|goad|stop|start|start|stable|disturbs|rises|dispute|penalty|rock|rock|quarry|stone)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
         # 'cache': False

     }),

    # As of now, the current card, Dance is, looks worthy


    # EXAMPLE: metal

    ('gather metal',
     r'^(gather\s*)?(met\w+|mat\w+|metal|gold|resentful|with|quote|metal|bachelor|matcha|Günther|ethan|Italy|with metal|poison)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
     }),


]
