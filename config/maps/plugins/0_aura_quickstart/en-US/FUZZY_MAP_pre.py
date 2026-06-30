# config/maps/plugins/0_aura_quickstart/en-US/FUZZY_MAP_pre.py
# TIP: Just type a word below this line (e.g., banana) and save.
import os
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
# Using your robust root detection
tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())



FUZZY_MAP_pre = [
    # TIP: Just type a word below this line (e.g., banana) and save.

    # --- Learning Mode Toggle ---
    # EXAMPLE: auralearning mode on
    ('Learning mode...', r'^aura.*learning mode (on|off|start|stop)$', 100, {
        'on_match_exec': [CONFIG_DIR / 'toggle_learning.py']
    }),
    # EXAMPLE: zyxü

    ('zyxü', r'^(zyxü)$', 10),

    # --- Training Plugin (Toggled by the script above) ---
    # (f'{str(__file__)}', r'^(.*)$', 10, {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
]
