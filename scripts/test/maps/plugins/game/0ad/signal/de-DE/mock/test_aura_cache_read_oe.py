import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.py.func.utils.aura_cache import get_cached_result

res = get_cached_result("alarm", "de-DE", "config/maps/plugins/game/0ad/signal/de-DE/FUZZY_MAP_pre.py", {}, "0 A.D.")

print(f"Cached result for 'alarm': {repr(res)}")
print(f"Type: {type(res)}")
if res:
    print(f"Length: {len(res)}")
    print(f"Bytes: {res.encode('utf-8')}")
