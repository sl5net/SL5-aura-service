# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path; import os; PROJECT_ROOT = Path(os.environ["SL5NET_AURA_PROJECT_ROOT"]) # noqa: E702

# too<-from
FUZZY_MAP_pre = [
    # Start-Regel: Triggert die Gruppe 'sandbox_test' bei "start sandbox"
    ('Sandbox:', r'^sta\w* .*box.*', 100, {'group_start': 'sandbox_test'}),

    # Innere Regel 1: Ersetzt "apfel" durch "birne" (wenn vorhanden)
    ('birne', r'apfel', 100, {}),

    # Innere Regel 2: Ersetzt "banane" (wenn vorhanden), sonst wird "banane" angehängt!
    ('banane', r'banane', 100, {}),

    # Passiver End-Marker für 'sandbox_test'
    (None, r'', 100, {'group_end': 'sandbox_test'}),
]

