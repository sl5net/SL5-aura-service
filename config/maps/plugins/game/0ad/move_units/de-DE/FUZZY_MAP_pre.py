# config/maps/plugins/game/0ad/move_units/de-DE/FUZZY_MAP_pre.py
# https://regex101.com/
import re # noqa: F401
from pathlib import Path as p # noqa: E702
CONFIG_DIR = p(__file__).parent

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702

FUZZY_MAP_pre = [

    # Directional movement rules for 0 A.D.
    ('kp8', r'^\s*(nach\s+)?norden\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    ('kp2', r'^\s*(nach\s+)?s[üu]den\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    ('kp6', r'^\s*(nach\s+)?osten\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    ('kp4', r'^\s*(nach\s+)?westen\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    ('kp9', r'^\s*(nach\s+)?nordosten\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    ('kp7', r'^\s*(nach\s+)?nordwesten\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    ('kp3', r'^\s*(nach\s+)?s[üu]dosten\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),
    ('kp1', r'^\s*(nach\s+)?s[üu]dwesten\s*$', 20, {'command_flags': re.IGNORECASE, 'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'], 'on_match_exec': [CONFIG_DIR / '..' / '..' / '0ad_actions.py'], 'execute_only': True}),

]
