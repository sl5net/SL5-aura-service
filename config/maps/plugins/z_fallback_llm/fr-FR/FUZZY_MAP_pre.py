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

import os
import re
import runpy
from pathlib import Path

from scripts.py.func.get_project_root import get_aura_project_root

CONFIG_DIR = Path(__file__).parent


# Ajouter un chemin vers les composants internes (nécessite SL5NET_AURA_PROJECT_ROOT)

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()


INTERNAL_PATH = SL5NET_AURA_PROJECT_ROOT / "config" / "maps" / "plugins" / "internals" / "de-DE"

acp = SL5NET_AURA_PROJECT_ROOT / "config" / "maps"/"plugins"/"internals"/"de-DE"/"aura_constants.py"
AURA_VARIANTS = runpy.run_path(acp)["AURA_VARIANTS"]


aura1 = AURA_VARIANTS

FUZZY_MAP_pre = [
    # Règle fourre-tout : correspond à tout (.*) en dernier recours.

    # Il capture l'intégralité du texte du groupe 1 pour le transmettre au script.


    # Si vous souhaitez faire correspondre une partie de l'expression régulière mais ne PAS l'avoir dans le groupe de capture (ce qui est utile pour l'extraction), utilisez le groupe de non-capture (?:...).

    # https://ollama.com/download


    # https://ollama.com/download

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: aura

""", r'^\s*(aura|Aurore|laure|Dora|ère|Hourra|prora|ordinateur)\s+(w\w{2,3}) (sont|faire)?(toi)$', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'élément',r'Firefox', r'chrome', r'courageux','double', r'nemo', r'thunar', r'caja'],
        }
    ),



# 1. Salutation simple avec nom (Bonjour/Salut [Nom])

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: Bonjour

""", r'^\s*(Bonjour|Salut|Hé|bien jour|Au revoir)\s+(aura|Aurore|ordinateur)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE
        }
    ),

# 2. Test de présence ou d'écoute (Es-tu là ? M'entends-tu ?)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: Es-tu là

""", r'^\s*(sont toi là|entendre toi moi|peut toi moi entendre|parler toi avec moi)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'élément',r'Firefox', r'chrome', r'courageux'],
        }
    ),

# 3. Adresse directe par nom uniquement (Aura ! / Ordinateur ?)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: aura

""", r'^\s*(aura|Aurore|laure|Dora|ère|Hourra|prora|ordinateur)\s*(\!|\.|\?|$)(\s+.*)?$', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'élément',r'Firefox', r'chrome', r'courageux','double', r'nemo', r'thunar', r'caja'],

        }
    ),

# 4. Question générique d’identité ou de fonction (Que faites-vous ? Qu’êtes-vous ?)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: qu'est-ce que tu es?

""", r'^\s*(Quoi)\s+(sont|faire)\s+(toi)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'élément',r'Firefox', r'chrome', r'courageux'],
        }
    ),

# 5. Demande impérative (parler / parler / démarrer)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: attraper

""", r'^\s*(attraper|commencer|commencer)\s+(à|juste)?\s*(à parler|avec moi|un conversation)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'élément',r'Firefox', r'chrome', r'courageux'],

        }
    ),

# Bonjour, je suis Aura, un système hors ligne (voix à action).

    ("""
Guten Morgen. Ich bin Aura ein Offline-System (Sprache zu Aktion).
# EXAMPLE: Bonjour

""", r'^\s*(Bonjour|Salut|Hé|bien (matin))\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'élément',r'Firefox', r'chrome', r'courageux'],
        }
    ),




# 6. Salutation générique simple (Bonjour/Bonne journée)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: Bonjour

""", r'^\s*(Bonjour|Salut|Hé|bien (jour|soirée|matin))\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'élément',r'Firefox', r'chrome', r'courageux'],
        }
    ),


    # EXAMPLE: aura

    ('ask_ollama', fr'^\s*{aura1}\s*\b(?:normale|lentement|Couler|couler|lent|Exactement|complet)\b\s*(.*)$', 10,  # min_accuracy
        {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py'],
        'exclude_windows': ['element', 'firefox', 'chrome', 'brave','.*double.*commander.*','double commander', r'nemo', r'thunar', r'caja'],
        }
    ),


    # https://ollama.com/download

    # EXAMPLE: aura

    ('ask_ollama', r'^\s*(aura|Aurore|laure|Dora|ère|Hourra|prora|ordinateur)\s+(.*)$', 100, # min_accuracy
        {
            'command_flags': re.IGNORECASE,
            'on_match_exec': [CONFIG_DIR / 'ask_ollama.py'],
            'exclude_windows': [r'élément',r'Firefox', r'chrome', r'courageux',r'double cmd',r'double commandant', r'nemo', r'thunar', r'caja'],
        }
    ),

]


# Ask_ollama_has_memory_clipboard_06




# Dites : "Ordinateur, qu'y a-t-il dans le presse-papiers ?"

# Dites : "Ordinateur, qu'y a-t-il dans le presse-papiers ?"

# Dites : "Ordinateur, qu'y a-t-il dans le presse-papiers ?"

# Dites : "Ordinateur, qu'y a-t-il dans le presse-papiers ?"

# Dites : "Ordinateur, qu'y a-t-il dans le presse-papiers ?"

# Dites : "Ordinateur, qu'y a-t-il dans le presse-papiers ?"

# Dites : "Ordinateur, qu'y a-t-il dans le presse-papiers ?"

# Dites : "Ordinateur, qu'y a-t-il dans le presse-papiers ?" Le presse-papiers est vide et ne contient aucune information. Tu peux essayer


# Le presse-papiers est vide et ne contient aucune information. Vous pouvez essayer de copier et coller le nouveau texte dans le presse-papiers ou en utilisant un autre navigateur.


"""
Frag Aura:

"Computer, wie installiere ich das Projekt?"

"Computer, welche Features hast du?"

"Computer, was steht in der Readme?"

Der Text in der Redmi (vermutlich ein Notizbuch oder eine Projektliste) ist nicht mehr vorhanden. Es wurde während des letzten Workshops geleert und wird möglicherweise neu strukturiert, um es für die zukünftige Nutzung besser zugänglich zu machen.

"""
