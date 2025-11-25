# config/maps/plugins/z_fallback_llm/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path
CONFIG_DIR = Path(__file__).parent
FUZZY_MAP_pre = [
    # Catch-all rule: Matches everything (.*) as the last resort.
    # It captures the whole text in group 1 to pass it to the script.

    ('ask_ollama', r'^\s*(Aura|Aurora|laura|dora|Ära|hurra|prora)\s+(.*)$', 100,
        {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py']
        }
    )

]
