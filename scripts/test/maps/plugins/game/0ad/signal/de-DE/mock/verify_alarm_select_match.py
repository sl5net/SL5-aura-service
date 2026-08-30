import importlib.util
import re

file_path = "config/maps/plugins/game/0ad/select/de-DE/FUZZY_MAP_pre.py"
spec = importlib.util.spec_from_file_location("fuzzy_map", file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

pattern = module.FUZZY_MAP_pre[0][1]
test_input = "alarm"
match = re.match(pattern, test_input, re.IGNORECASE)

print(f"File: {file_path}")
print(f"Pattern: {pattern}")
print(f"Input: {test_input}")
print(f"Is match: {bool(match)}")
