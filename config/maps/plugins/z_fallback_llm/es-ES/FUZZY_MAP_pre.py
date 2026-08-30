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


# Agregar ruta a los componentes internos (requiere SL5NET_AURA_PROJECT_ROOT)

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()


INTERNAL_PATH = SL5NET_AURA_PROJECT_ROOT / "config" / "maps" / "plugins" / "internals" / "de-DE"

acp = SL5NET_AURA_PROJECT_ROOT / "config" / "maps"/"plugins"/"internals"/"de-DE"/"aura_constants.py"
AURA_VARIANTS = runpy.run_path(acp)["AURA_VARIANTS"]


aura1 = AURA_VARIANTS

FUZZY_MAP_pre = [
    # Regla general: coincide con todo (.*) como último recurso.

    # Captura todo el texto del grupo 1 para pasarlo al guión.


    # Si desea hacer coincidir parte de la expresión regular pero NO tenerla en el grupo de captura (que es útil para extraer), use el grupo de no captura (?:...).

    # https://ollama.com/download


    # https://ollama.com/download

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: aura

""", r'^\s*(aura|Aurora|laura|dora|era|Hurra|prora|computadora)\s+(w\w{2,3}) (son|hacer)?(tú)$', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'elemento',r'firefox', r'cromo', r'corajudo','double'],
        }
    ),



# 1. Saludo simple con nombre (Hola/Hola [Nombre])

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: Hola

""", r'^\s*(Hola|Hola|ey|bien día|Adiós)\s+(aura|Aurora|computadora)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE
        }
    ),

# 2. Prueba de presencia o escucha (¿Estás ahí? ¿Puedes oírme?)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: Está ahí

""", r'^\s*(son tú allá|escuchar tú a mí|poder tú a mí escuchar|hablar tú con a mí)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'elemento',r'firefox', r'cromo', r'corajudo'],
        }
    ),

# 3. Dirección directa solo por nombre (¿Aura! / ¿Computadora?)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: aura

""", r'^\s*(aura|Aurora|laura|dora|era|Hurra|prora|computadora)\s*(\!|\.|\?|$)(\s+.*)?$', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'elemento',r'firefox', r'cromo', r'corajudo','double'],

        }
    ),

# 4. Pregunta genérica de identidad o función (¿A qué te dedicas? ¿Qué eres?)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: ¿qué vas a?

""", r'^\s*(Qué)\s+(son|hacer)\s+(tú)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'elemento',r'firefox', r'cromo', r'corajudo'],
        }
    ),

# 5. Petición imperativa (hablar/hablar/empezar)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: atrapar

""", r'^\s*(atrapar|comenzar|comenzar)\s+(a|justo)?\s*(a hablar|con a mí|a conversación)\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'elemento',r'firefox', r'cromo', r'corajudo'],

        }
    ),

# Buenos días soy Aura un sistema offline (voz a acción).

    ("""
Guten Morgen. Ich bin Aura ein Offline-System (Sprache zu Aktion).
# EXAMPLE: Hola

""", r'^\s*(Hola|Hola|ey|bien (mañana))\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'elemento',r'firefox', r'cromo', r'corajudo'],
        }
    ),




# 6. Saludo genérico simple (Hola/Buenos días)

    ("""
Ich bin Aura ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung.
Es gibt keine Accounts, Passwörter, Logins.
# EXAMPLE: Hola

""", r'^\s*(Hola|Hola|ey|bien (día|noche|mañana))\s*(\!|\.|\?|$)', 100,
        {
        'command_flags': re.IGNORECASE,
        'exclude_windows': [r'elemento',r'firefox', r'cromo', r'corajudo'],
        }
    ),


    # EXAMPLE: aura

    ('ask_ollama', fr'^\s*{aura1}\s*\b(?:normal|despacio|Fluir|fluir|lento|Exactamente|exhaustivo)\b\s*(.*)$', 10,  # min_accuracy
        {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py'],
        'exclude_windows': ['element', 'firefox', 'chrome', 'brave','.*double.*commander.*','double commander'],
        }
    ),


    # https://ollama.com/download

    # EXAMPLE: aura

    ('ask_ollama', r'^\s*(aura|Aurora|laura|dora|era|Hurra|prora|computadora)\s+(.*)$', 100, # min_accuracy
        {
            'command_flags': re.IGNORECASE,
            'on_match_exec': [CONFIG_DIR / 'ask_ollama.py'],
            'exclude_windows': [r'elemento',r'firefox', r'cromo', r'corajudo',r'doble cmd',r'doble comandante'],
        }
    ),

]


# Ask_ollama_has_memory_clipboard_06




# Diga: "Computadora, ¿qué hay en el portapapeles?"

# Diga: "Computadora, ¿qué hay en el portapapeles?"

# Diga: "Computadora, ¿qué hay en el portapapeles?"

# Diga: "Computadora, ¿qué hay en el portapapeles?"

# Diga: "Computadora, ¿qué hay en el portapapeles?"

# Diga: "Computadora, ¿qué hay en el portapapeles?"

# Diga: "Computadora, ¿qué hay en el portapapeles?"

# Diga: "Computadora, ¿qué hay en el portapapeles?" El portapapeles está vacío y no contiene información. puedes intentarlo


# El portapapeles está vacío y no contiene información. Puede intentar copiar y pegar texto nuevo en el portapapeles o utilizar un navegador diferente.


"""
Frag Aura:

"Computer, wie installiere ich das Projekt?"

"Computer, welche Features hast du?"

"Computer, was steht in der Readme?"

Der Text in der Redmi (vermutlich ein Notizbuch oder eine Projektliste) ist nicht mehr vorhanden. Es wurde während des letzten Workshops geleert und wird möglicherweise neu strukturiert, um es für die zukünftige Nutzung besser zugänglich zu machen.

"""
