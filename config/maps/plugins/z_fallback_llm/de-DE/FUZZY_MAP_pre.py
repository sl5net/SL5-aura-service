# config/maps/plugins/z_fallback_llm/de-DE/FUZZY_MAP_pre.py
import os
import re
import runpy
from pathlib import Path
CONFIG_DIR = Path(__file__).parent


# Pfad zu den Internals hinzufügen (erfordert PROJECT_ROOT)
tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())


INTERNAL_PATH = PROJECT_ROOT / "config" / "maps" / "plugins" / "internals" / "de-DE"

acp = PROJECT_ROOT / "config" / "maps"/"plugins"/"internals"/"de-DE"/"aura_constants.py"
AURA_VARIANTS = runpy.run_path(acp)["AURA_VARIANTS"]


aura1 = AURA_VARIANTS

FUZZY_MAP_pre = [
    # Catch-all rule: Matches everything (.*) as the last resort.
    # It captures the whole text in group 1 to pass it to the script.

    # Wenn Sie einen Teil des Regex matchen, aber NICHT in der Capturing Group haben möchten (was nützlich für das Extrahieren ist), verwenden Sie die Non-Capturing Group (?:...).
    # https://ollama.com/download

    # https://ollama.com/download
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: Aura
""", r'^\s*(Aura|Aurora|laura|dora|Ära|hurra|prora|Computer)\s+(w\w{2,3}) (bist|machst)?(du)$', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave','double'],
        }
    ),

#


# 1. Einfache Begrüßung mit Namen (Hallo/Hi [Name])
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: hallo
""", r'^\s*(hallo|hi|hey|guten tag|servus)\s+(Aura|Aurora|Computer)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE
        }
    ),

# 2. Präsenz- oder Hörtest (Bist du da? Hörst du mich?)
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: bist du da
""", r'^\s*(bist du da|hörst du mich|kannst du mich hören|sprichst du mit mir)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
        }
    ),

# 3. Direkte Anrede nur mit dem Namen (Aura! / Computer?)
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: Aura
""", r'^\s*(Aura|Aurora|laura|dora|Ära|hurra|prora|Computer)\s*(\!|\.|\?|$)(\s+.*)?$', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave','double'],

        }
    ),

# 4. Generische Frage zur Identität oder Funktion (Was machst du? Was bist du?)
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: was bist
""", r'^\s*(was)\s+(bist|machst)\s+(du)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
        }
    ),

# 5. Imperative Aufforderung (Rede / Sprich / Fang an)
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: fang
""", r'^\s*(fang|starte|beginn)\s+(an|mal)?\s*(zu sprechen|mit mir|ein gespräch)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],

        }
    ),

#Guten Morgen. Ich bin Aura ein Offline-System (Sprache zu Aktion).
    ("""
Guten Morgen. Ich bin Aura ein Offline-System (Sprache zu Aktion).
# EXAMPLE: hallo
""", r'^\s*(hallo|hi|hey|guten (morgen))\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
        }
    ),




# 6. Einfache generische Begrüßung (Hallo / Guten Tag)
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: hallo
""", r'^\s*(hallo|hi|hey|guten (tag|abend|morgen))\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
        }
    ),


    # EXAMPLE: Aura
    ('ask_ollama', fr'^\s*{aura1}\s*\b(?:normal|slow|Flow|flow|langsam|genau|gründlich)\b\s*(.*)$', 10,  # min_accuracy
        {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py'],
        'exclude_windows': ['element', 'firefox', 'chrome', 'brave','.*double.*commander.*','double commander'],
        }
    ),


    # https://ollama.com/download
    # EXAMPLE: Aura
    ('ask_ollama', r'^\s*(Aura|Aurora|laura|dora|Ära|hurra|prora|Computer)\s+(.*)$', 100, # min_accuracy
        {
            'command_flags': re.IGNORECASE,
            'on_match_exec': [CONFIG_DIR / 'ask_ollama.py'],
            'exclude_windows': [r'element',r'firefox', r'chrome', r'brave',r'doublecmd',r'double commander'],
        }
    ),

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

Der Text in der Redmi (vermutlich ein Notizbuch oder eine Projektliste) ist nicht mehr vorhanden. Es wurde während des letzten Workshops geleert und wird möglicherweise neu strukturiert, um es für die zukünftige Nutzung besser zugänglich zu machen.

"""
