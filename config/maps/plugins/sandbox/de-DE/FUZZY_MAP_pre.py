# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import os as o
import re  # noqa: F401
from pathlib import Path as p

with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())

# too<-from
FUZZY_MAP_pre = [
    ('ert', r'^(ert)$'),
    # (f'{str(__file__)}', r'^(.*)$', 10, {'on_match_exec': [SL5NET_AURA_PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
]
