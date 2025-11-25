# config/maps/plugins/z_fallback_llm/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path
CONFIG_DIR = Path(__file__).parent
FUZZY_MAP_pre = [
    # Catch-all rule: Matches everything (.*) as the last resort.
    # It captures the whole text in group 1 to pass it to the script.

    ('ask_ollama', r'^\s*(Aura|Aurora|laura|dora|Ära|hurra|prora|Computer)\s+(.*)$', 100,
        {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'ask_ollama_about_Aura.py']
        }
    )

]


# ask_ollama_has_memory_clipboard_06

# Sag: "Computer, was steht in der Zwischenablage?"
# Sag: "Computer, was steht in der Zwischenablage?"
# Sag: "Computer, was steht in der Zwischenablage?"
# Sag: "Computer, was steht in der Zwischenablage?"
# Sag: "Computer, was steht in der Zwischenablage?"
# Sag: "Computer, was steht in der Zwischenablage?"
# Sag: "Computer, was steht in der Zwischenablage?"
# Sag: "Computer, was steht in der Zwischenablage?"Die Zwischenablage ist leer und enthält keine Informationen. Sie können versuchen,

#Die Zwischenablage ist leer und enthält keine Informationen. Sie können versuchen, einen neuen Text zu kopieren und in die Zwischenablage einfügen oder einen anderen Browser zu verwenden.
#

"""
Frag Aura:

    "Computer, wie installiere ich das Projekt?"

    "Computer, welche Features hast du?"

    "Computer, was steht in der Readme?"



"""
