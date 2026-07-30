# config/maps/plugins/game/0ad/camera_navigation/de-DE/FUZZY_MAP_pre.py
# https://regex101.com/
import re # noqa: F401
from pathlib import Path as p # noqa: E702
CONFIG_DIR = p(__file__).parent

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702

from pathlib import Path
import re

CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # EXAMPLE: kamera nach norden
    ('camera_up', r'^\s*kamera\s+(nach\s+)?(norden|oben)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # EXAMPLE: kamera nach sueden
    # EXAMPLE: kamera nach süden
    ('camera_down', r'^\s*kamera\s+(nach\s+)?(s[üu]den|unten|runter)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # EXAMPLE: kamera nach westen
    ('camera_left', r'^\s*kamera\s+(nach\s+)?(westen|links)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

    # EXAMPLE: kamera nach osten
    ('camera_right', r'^\s*kamera\s+(nach\s+)?(osten|rechts)\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
]
