# config/maps/plugins/standard_actions/en-US/FUZZY_MAP_pre.py
import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702
#(f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}), # noqa: E702

from pathlib import Path

CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [

    # EXAMPLE: good Morning
    ('good evening', r'good Morning', 95, # min_accuracy
 {'flags': re.IGNORECASE, 'skip_list': ['LT_SKIP_RATIO_THRESHOLD']} ),

]

