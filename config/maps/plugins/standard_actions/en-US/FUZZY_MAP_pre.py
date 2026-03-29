# config/maps/plugins/standard_actions/en-US/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path

CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [

    # EXAMPLE: good Morning
    ('good evening', r'good Morning', 95, # min_accuracy
 {'flags': re.IGNORECASE, 'skip_list': ['LT_SKIP_RATIO_THRESHOLD']} ),

]

