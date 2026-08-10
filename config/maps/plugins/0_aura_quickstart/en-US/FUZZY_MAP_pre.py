# config/maps/plugins/0_aura_quickstart/en-US/FUZZY_MAP_pre.py
# TIP: Just type a word below this line (e.g., banana) and save.
from scripts.py.func.get_project_root import get_aura_project_root
import os
import re
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
# Using your robust root detection
tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()



FUZZY_MAP_pre = [
    # TIP: Just type a word below this line (e.g., banana) and save.

    # --- Learning Mode Toggle ---
    # EXAMPLE: auralearning mode on
    ('Learning mode...', r'^aura.*learning mode (on|off|start|stop)$', 100, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_learning.py']
    }),
    # EXAMPLE: zyxü

    ('zyxü', r'^(zyxü)$', 10),

    # --- Training Plugin (Toggled by the script above) ---
    
]
