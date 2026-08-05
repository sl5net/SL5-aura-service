# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702
baue = r'(\s*(\w+au\w+|\waue|bauer\w|bauens|build|bei|anbau\w*|aber|bürohilfe|paul|paulus|warum|warhols|power|our|build|\w+ild)\s*)'
CONFIG_DIR = p(__file__).parent
_common_meta = {
    'command_flags': re.IGNORECASE,
    'skip_list': ['LanguageTool'],
}
FUZZY_MAP_pre = [
    ('a', r'^test1$'),
    ('b', r'^test2$', 15, _common_meta),
    ('n', fr'^{baue}?(s(ch)?m\w*|forge)\s*$', 15, _common_meta),
    
    ('n', r'^(s(ch)?m\w*|forge)$', 15, _common_meta),
]
