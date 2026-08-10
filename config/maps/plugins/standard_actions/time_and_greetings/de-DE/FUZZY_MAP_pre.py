# config/maps/plugins/standard_actions/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401

from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702

CONFIG_DIR = p(__file__).parent

FUZZY_MAP_pre = [
    # EXAMPLE: anrede
    ('anrede', r'^(anrede|begrüßung|neue email|Neue E-Mail|Schreibe anrede\w*|Schreibe begrüßung)$', 95, {
        'flags': re.IGNORECASE,
        # Ruft unser neues Skript auf
        'on_match_exec': [CONFIG_DIR / '..' /  'greeting_generator.py']
    }),
]

