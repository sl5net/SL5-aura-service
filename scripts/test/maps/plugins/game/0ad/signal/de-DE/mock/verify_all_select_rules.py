import re
import importlib.util

file_path = "config/maps/plugins/game/0ad/select/de-DE/FUZZY_MAP_pre.py"
spec = importlib.util.spec_from_file_location("fuzzy_map", file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

test_input = "alarm"
matched_rules = []

for idx, item in enumerate(module.FUZZY_MAP_pre):
    target = item[0]
    pattern = item[1]
    if re.search(pattern, test_input, re.IGNORECASE):
        matched_rules.append((idx, target, pattern))

print(f"Total rules checked: {len(module.FUZZY_MAP_pre)}")
print(f"Matched rules for '{test_input}': {len(matched_rules)}")
for idx, target, pattern in matched_rules:
    print(f"Rule #{idx}: target='{target}', pattern='{pattern}'")

