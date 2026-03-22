import re  # noqa: F401
from pathlib import Path

# ============================================================
# Koan 06: Wikipedia Search by Voice
# ============================================================
#
# LEARNING GOAL:
#   on_match_exec can query online APIs.
#   Here: Wikipedia search by voice command.
#
# TASK:
#   1. Activate the rule below.
#   2. Say: "What is London?"
#
# ERRORS? Check the log:
#   grep "wikipedia" log/aura_engine.log | tail -10
#
# OFFLINE OPTION:
#   See config/maps/plugins/standard_actions/wikipedia_local/
#
# NEXT STEP: Koan 07
# ============================================================

CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # ('What is London?', r'^what is (?P<topic>.+)\?$', 90, {
    #     'flags': re.IGNORECASE,
    #     'on_match_exec': [CONFIG_DIR / 'wiki_search.py']
    # }),
]
