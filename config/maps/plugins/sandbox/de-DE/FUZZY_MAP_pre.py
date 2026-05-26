# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path; import os; PROJECT_ROOT = Path(os.environ["SL5NET_AURA_PROJECT_ROOT"]) # noqa: E702

# too<-from
FUZZY_MAP_pre = [
    ('nix', r'^(nix|laut|Programm geladen. Viel Spaß|mit guten)$'),

    (f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}), # noqa: E702

]
