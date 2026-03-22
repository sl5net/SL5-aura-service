import re  # noqa: F401
from pathlib import Path

# ============================================================
# Koan 05: Database Search by Voice – on_match_exec
# ============================================================
#
# LEARNING GOAL:
#   Rules can execute external Python scripts via on_match_exec.
#   Here: database search by voice command.
#
# TASK:
#   Say: "search in Ruth chapter 1 verse 1"
#
# EXPECTED RESULT:
#   Aura runs bible_search.py and outputs the verse.
#
# PREREQUISITE:
#   bible_search.py and GerElb1905.db are in the same folder.
#
# NEXT STEP: Koan 06
# ============================================================

CONFIG_DIR = Path(__file__).parent


FUZZY_MAP_pre = [
    # TODO: Activate the line below by removing the comment symbol '#'
    #('search in Ruth chapter 1 verse 1', fr'^.*$', 90, {'flags': re.IGNORECASE,'skip_list': ['fullMatchStop', 'LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']}),

    # EXAMPLE: search in [book] chapter [number] verse [number]
    ('bible search', r'^search in (?P<book>\w*[ ]?\w+) chapter (?P<chapter>\d+) [v]\w+ (?P<verse>\d+)$', 90, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'bible_search.py']
    }),

    # TODO: Can you invent other search patterns?
]
