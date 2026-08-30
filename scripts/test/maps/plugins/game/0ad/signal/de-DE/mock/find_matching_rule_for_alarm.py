import importlib.util
import os
import re

base_dir = "config/maps/plugins/game/0ad"
test_input = "alarm"
matches = []

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith("FUZZY_MAP_pre.py"):
            full_path = os.path.join(root, file)
            try:
                spec = importlib.util.spec_from_file_location("fuzzy_map_module", full_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                fuzzy_list = getattr(module, "FUZZY_MAP_pre", [])
                for idx, item in enumerate(fuzzy_list):
                    target = item[0]
                    pattern = item[1]
                    if re.search(pattern, test_input, re.IGNORECASE):
                        matches.append((full_path, idx, target, pattern))
            except Exception as e:
                print(f"Error loading {full_path}: {e}")

print(f"Total matching rules across ALL 0ad maps for '{test_input}': {len(matches)}")
for path, idx, target, pattern in matches:
    print(f"File: {path}")
    print(f"Rule #{idx}: target='{target}'")
    print(f"Pattern: {pattern}\n")
