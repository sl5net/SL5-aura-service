# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path; import os; PROJECT_ROOT = Path(os.environ["SL5NET_AURA_PROJECT_ROOT"]) # noqa: E702

# too<-from
FUZZY_MAP_pre = [
    ('nix', r'^(nix|fußball|hurra lernen modus ausschalten|Learn-modus rule not found. |lernen lernmodus einschalten|ok)$'),
]
