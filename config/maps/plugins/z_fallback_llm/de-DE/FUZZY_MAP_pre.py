# config/maps/plugins/z_fallback_llm/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path
CONFIG_DIR = Path(__file__).parent
FUZZY_MAP_pre = [
    # Catch-all rule: Matches everything (.*) as the last resort.
    # It captures the whole text in group 1 to pass it to the script.


    # https://ollama.com/download
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
""", r'^\s*(Aura|Aurora|laura|dora|Ära|hurra|prora|Computer)\s+(w\w{2,3}) (bist|machst)?(du)$', 100,
        {
        'flags': re.IGNORECASE
        }
    ),

#


# 1. Einfache Begrüßung mit Namen (Hallo/Hi [Name])
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
""", r'^\s*(hallo|hi|hey|guten tag|servus)\s+(Aura|Aurora|Computer)\s*(\!|\.|\?|$)', 100,
        {
        'flags': re.IGNORECASE
        }
    ),

# 2. Präsenz- oder Hörtest (Bist du da? Hörst du mich?)
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
""", r'^\s*(bist du da|hörst du mich|kannst du mich hören|sprichst du mit mir)\s*(\!|\.|\?|$)', 100,
        {
        'flags': re.IGNORECASE
        }
    ),

# 3. Direkte Anrede nur mit dem Namen (Aura! / Computer?)
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
""", r'^\s*(Aura|Aurora|laura|dora|Ära|hurra|prora|Computer)\s*(\!|\.|\?|$)(\s+.*)?$', 100,
        {
        'flags': re.IGNORECASE
        }
    ),

# 4. Generische Frage zur Identität oder Funktion (Was machst du? Was bist du?)
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
""", r'^\s*(was)\s+(bist|machst)\s+(du)\s*(\!|\.|\?|$)', 100,
        {
        'flags': re.IGNORECASE
        }
    ),

# 5. Imperative Aufforderung (Rede / Sprich / Fang an)
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
""", r'^\s*(fang|starte|beginn)\s+(an|mal)?\s*(zu sprechen|mit mir|ein gespräch)\s*(\!|\.|\?|$)', 100,
        {
        'flags': re.IGNORECASE
        }
    ),

# 6. Einfache generische Begrüßung (Hallo / Guten Tag)
    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
""", r'^\s*(hallo|hi|hey|guten (tag|abend|morgen))\s*(\!|\.|\?|$)', 100,
        {
        'flags': re.IGNORECASE
        }
    ),



    # # https://ollama.com/download
    ('ask_ollama', r'^\s*(Aura|Aurora|laura|dora|Ära|hurra|prora|Computer)\s+(.*)$', 100,
        {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py']
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

Der Text in der Redmi (vermutlich ein Notizbuch oder eine Projektliste) ist nicht mehr vorhanden. Es wurde während des letzten Workshops geleert und wird möglicherweise neu strukturiert, um es für die zukünftige Nutzung besser zugänglich zu machen.

"""
