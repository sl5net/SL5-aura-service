# config/maps/koans_deutsch/00_koan_oma-modus/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path as p;import os as o # noqa: E702
with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702

#(f'{str(__file__)}', r'^(.*)$', 10,{'on_mat ch_exec':[SL5NET_AURA_PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}), # noqa: E702
                        

# too<-from
FUZZY_MAP_pre = [
    ('Kornfeld', r'^(Kornfeld|gerade fällt|goal)$'),
    #(f'{str(__file__)}', r'^(.*)$', 10, {'on_match_exec': [SL5NET_AURA_PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),

]
