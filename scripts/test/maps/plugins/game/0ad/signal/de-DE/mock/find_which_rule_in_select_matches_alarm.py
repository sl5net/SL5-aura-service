# .venv/bin/python scripts/py/find_which_rule_in_select_matches_alarm.py

import re
import importlib.util

file_path = "config/maps/plugins/game/0ad/select/de-DE/FUZZY_MAP_pre.py"
spec = importlib.util.spec_from_file_location("select_map", file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

test_input = "alarm"
print(f"Scanning {len(module.FUZZY_MAP_pre)} rules in {file_path} for input '{test_input}'...\n")

for idx, rule in enumerate(module.FUZZY_MAP_pre):
    target = rule[0]
    pattern = rule[1]

    match_search = re.search(pattern, test_input, re.IGNORECASE)
    match_exact = re.match(pattern, test_input, re.IGNORECASE)

    if match_search or match_exact:
        print(f"MATCH FOUND at Rule index {idx}:")
        print(f"  Target: '{target}'")
        print(f"  Pattern: {pattern}")
        print(f"  Match obj: {match_search or match_exact}\n")

