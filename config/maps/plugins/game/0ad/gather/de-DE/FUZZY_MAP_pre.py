# config/maps/plugins/game/0ad/gather/de-DE/FUZZY_MAP_pre.py
import os as o
import re
from pathlib import Path as p

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())

# https://regex101.com/

CONFIG_DIR = p(__file__).parent

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())

baum = r'baum|warum'

FUZZY_MAP_pre = [

    # EXAMPLE: holz
    ('gather wood',
     fr'^(gather\s*)?(wood|hol\w*|roll|rhön|hui|heute|ruhig|bridge|bridges|{baum}|bäume|tree|rollen|ranch|rötz|ruiz|rülpst|uns)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
     }),

    # unmatched is added to your map  (331)
    # asldfkjasödlfsa dfnoch ein testasdfsjdflksdöfsdj
    #sdddfgd festasdsdsadfsdf asdfasödkfjashfdasdfsadfsdfschlittschuhläufer

    #fußballsauto fußball

    # EXAMPLE: früchte
    ('gather fruit',
     r'^\s*(er|b|beere\w*|gehring|bill|bier|baby|obst|fruit|früchte[n]?|Äpfel[n]?|Apfel|Birne[n]?|berries|quarry)\s*$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
         # 'cache': False
     }),

    # \w+ \w*a\w+en

    # EXAMPLE: fleisch
    ('gather meat',
     r'^(fleisch|jagd|jagen|\w+ \w*a\w+en|\w+ \w+a\w+en|jacken|ja|ja gut|ihr habt|meat|wetter|welche amen|ritt|stollen|\w+\s\wagen|wir hatten)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
     }),

    # EXAMPLE: stein
    ('gather stone',
     r'^(gather\s*)?(stein\w*|darin|steig\w*|stahl|stadt|stacheln|stopp|start|starten|stabil|stört|steigt|streit|strafe|rock|fels|quarry|stone)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
         # 'cache': False
     }),

    # Wie jetzt ist die aktuelle KarteTanz ist wirkt würdig

    # EXAMPLE: metal
    ('gather metal',
     r'^(gather\s*)?(met\w+|mat\w+|metall|gold|groll|mit|zitat|metal|bachelor|matcha|günther|ethan|italien|mit metall|gift)$',
     85,
     {
         'command_flags': re.IGNORECASE,
         'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
         'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'],
         'execute_only': True,
     }),


]