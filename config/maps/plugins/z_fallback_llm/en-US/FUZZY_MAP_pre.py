# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/z_fallback_llm/de-DE/FUZZY_MAP_pre.py

from scripts.py.func.get_project_root import get_aura_project_root
import os
import re
import runpy
from pathlib import Path
CONFIG_DIR = Path(__file__).parent


# Add path to internals (requires SL5NET_AURA_PROJECT_ROOT)

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()


INTERNAL_PATH = SL5NET_AURA_PROJECT_ROOT / "config" / "maps" / "plugins" / "internals" / "de-DE"

acp = SL5NET_AURA_PROJECT_ROOT / "config" / "maps"/"plugins"/"internals"/"de-DE"/"aura_constants.py"
AURA_VARIANTS = runpy.run_path(acp)["AURA_VARIANTS"]


aura1 = AURA_VARIANTS

FUZZY_MAP_pre = [
    # Catch-all rule: Matches everything (.*) as the last resort.

    # It captures the whole text in group 1 to pass it to the script.


    # If you want to match part of the regex but NOT have it in the capturing group (which is useful for extracting), use the non-capturing group (?:...).

    # https://translate.google.com/translate?hl=en&sl=de&tl=en&u=https://ollama.com/download


    # https://translate.google.com/translate?hl=en&sl=de&tl=en&u=https://ollama.com/download

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: aura

""", r'^\s*(aura|Aurora|laura|Dora|era|hurrah|prora|computer)\s+(w\w{2,3}) (are|do)?(you)$', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave','double'],
        }
    ),

#


# 1. Simple greeting with name (Hello/Hi [Name])

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: Hello

""", r'^\s*(Hello|hi|hey|good day|Goodbye)\s+(aura|Aurora|computer)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE
        }
    ),

# 2. Presence or listening test (Are you there? Can you hear me?)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: Are you there

""", r'^\s*(are you there|hear you me|can you me hear|speak you with me)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
        }
    ),

# 3. Direct address by name only (Aura! / Computer?)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: aura

""", r'^\s*(aura|Aurora|laura|Dora|era|hurrah|prora|computer)\s*(\!|\.|\?|$)(\s+.*)?$', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave','double'],

        }
    ),

# 4. Generic identity or function question (What do you do? What are you?)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: what are you?

""", r'^\s*(What)\s+(are|do)\s+(you)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
        }
    ),

# 5. Imperative request (speak / speak / start)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: catch

""", r'^\s*(catch|start|start)\s+(to|just)?\s*(to speak|with me|a conversation)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],

        }
    ),

# Good morning I am Aura an offline system (voice to action).

    ("""
Guten Morgen. Ich bin Aura ein Offline-System (Sprache zu Aktion).
# EXAMPLE: Hello

""", r'^\s*(Hello|hi|hey|good (morning))\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
        }
    ),




# 6. Simple generic greeting (Hello/Good day)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: Hello

""", r'^\s*(Hello|hi|hey|good (day|evening|morning))\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
        }
    ),


    # EXAMPLE: aura

    ('ask_ollama', fr'^\s*{aura1}\s*\b(?:normal|slowly|Flow|flow|slow|Exactly|thorough)\b\s*(.*)$', 10,  # min_accuracy
        {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py'],
        'exclude_windows': ['element', 'firefox', 'chrome', 'brave','.*double.*commander.*','double commander'],
        }
    ),


    # https://translate.google.com/translate?hl=en&sl=de&tl=en&u=https://ollama.com/download

    # EXAMPLE: aura

    ('ask_ollama', r'^\s*(aura|Aurora|laura|Dora|era|hurrah|prora|computer)\s+(.*)$', 100, # min_accuracy
        {
            'command_flags': re.IGNORECASE,
            'on_match_exec': [CONFIG_DIR / 'ask_ollama.py'],
            'exclude_windows': [r'element',r'firefox', r'chrome', r'brave',r'doublecmd',r'double commander'],
        }
    ),

]


# ask_ollama_has_memory_clipboard_06




# Say, "Computer, what's on the clipboard?"

# Say, "Computer, what's on the clipboard?"

# Say, "Computer, what's on the clipboard?"

# Say, "Computer, what's on the clipboard?"

# Say, "Computer, what's on the clipboard?"

# Say, "Computer, what's on the clipboard?"

# Say, "Computer, what's on the clipboard?"

# Say, "Computer, what's on the clipboard?" The clipboard is empty and contains no information. You can try


# The clipboard is empty and contains no information. You can try copying and pasting new text to the clipboard or using another browser.

#

"""
Frag Aura:

"Computer, wie installiere ich das Projekt?"

"Computer, welche Features hast du?"

"Computer, was steht in der Readme?"

Der Text in der Redmi (vermutlich ein Notizbuch oder eine Projektliste) ist nicht mehr vorhanden. Es wurde während des letzten Workshops geleert und wird möglicherweise neu strukturiert, um es für die zukünftige Nutzung besser zugänglich zu machen.

"""
