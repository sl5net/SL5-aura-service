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

# config/maps/plugins/z_fallback_llm/de-DE/normalizer.py


import re

# desde idna.idnadata importar scripts


# importar hashlib



import sys
from pathlib import Path

CURRENT_FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT_DIR = CURRENT_FILE_DIR
# para _ en el rango(5):

# PROJECT_ROOT_DIR = PROJECT_ROOT_DIR.padre


# Agregue el directorio raíz a la ruta de Python

# sys.path.append(cadena(PROJECT_ROOT_DIR))


# try:

# desde scripts.py.func.audio_manager importar * # noqa: F403 F401

# excepto ImportError como e:

# print(f"Error: No se pudo importar 'audio_manager.py' como módulo: {e}")

# utils.log_debug(f"Error: No se pudo importar 'audio_manager' como módulo: {e}")


# config/maps/plugins/z_fallback_llm/de-DE/normalizer.py

def _load_heavy_deps():
    global get_suggestions, utils
    try:
        from . import utils
    except ImportError:
        try:
            import utils
        except ImportError as e:
            raise RuntimeError(f"utils konnte nicht importiert werden: {e}")

    try:
        from config.maps.plugins.standard_actions.get_suggestions import get_suggestions # noqa: F401
    except ImportError as e:
        print(f"Fehler: Konnte 'get_suggestions.py' nicht als Modul importieren: {e}")
        utils.log_debug(f"Fehler: Konnte 'get_suggestions.py' nicht als Modul importieren: {e}")
        sys.exit(1)

# TODO: mejorar sinónimo




# ----------------------------------------------------

# DEFINICIONES:

# 1. Los sinónimos (de función antigua)

# 2. La normalización extrema (de la última respuesta)

# ----------------------------------------------------


# (1) Los sinónimos que garantizan una alta tasa de coincidencia en el caché

COMMAND_SYNONYMS = {
    "erstelle": "neu", "erstellen": "neu", "generiere": "neu", "mach": "neu",
    "mache": "neu", "schreibe": "neu", "füge": "neu", "neue": "neu",

    "zeig": "info", "zeige": "info", "wo": "info", "wie": "info", "hilfe": "info", "erklär": "info",

    "lösche": "del", "entferne": "del", "vergiss": "del",

    # Los sinónimos contextuales son arriesgados pero buenos para las coincidencias

    "config": "konfig", "configuration": "konfig", "einstellungen": "konfig",
    "regex": "regel", "regeln": "regel", "pattern": "regel"
}





def create_ultimate_cache_key(text):
    # -----------------------------------------------

    # PASO 1: Reemplazo de sinónimos (¡El nuevo e importante paso!)

    # -----------------------------------------------

    text_lower = text.lower()
    words = text_lower.split()

    synonym_replaced_words = [COMMAND_SYNONYMS.get(word, word) for word in words]
    synonym_replaced_text = " ".join(synonym_replaced_words)

    # -----------------------------------------------

    # PASO 2: Normalización extrema (derivación y palabras vacías)

    # -----------------------------------------------

    # Aquí utilizamos la función extremadamente agresiva (extreme_standardize_prompt_text)

    # Nota: Esta función ahora debe contener las palabras "nuevo", "información", "del", "regla", etc.

    # ¡NO las elimine de la lista de palabras vacías porque provienen de sinónimos!


    final_cache_key = extreme_standardize_prompt_text(synonym_replaced_text)

    # Ejemplo:

    # Prompt = "generar una nueva regla"

    # S1: "nueva, una nueva regla"

    # S2: "nueva regla nueva" (después de eliminar la raíz y la palabra de parada)


    return final_cache_key

# ----------------------------------------------------

# ACCIÓN:

# Realice la migración de la base de datos con esto

# ¡Nueva función 'create_ultimate_cache_key'!

# ----------------------------------------------------




def extreme_standardize_prompt_text(text):
    _load_heavy_deps()  # ensure utils is loaded

    # Inicializar el lematizador alemán



    # 1. Todo en minúsculas

    text = text.lower()

    # 2. Reemplace TODOS los números, horas y símbolos de moneda con marcadores de posición

    # EXAMPLE: 123. 123

    text = re.sub(r'\d+([.,]\d+)?', ' [NUMBER] ', text)  # Z.B. '10', '10.5'
    # EXAMPLE: $

    text = re.sub(r'[€$£%]', ' ', text)

    # 3. Eliminación radical de casi todos los caracteres especiales y signos de puntuación.

    # EXAMPLE: a-zäöüß s

    text = re.sub(r'[^a-zäöüß\s]', ' ', text)

    # 4. Reduzca los espacios en blanco a un solo espacio y recorte

    # EXAMPLE: 

    text = re.sub(r'\s+', ' ', text).strip()

    # 5. Tokenización (separación de palabras)

    words = text.split()

    # 6. Detener la eliminación y derivación de palabras

    stemmed_words = []
    for word in words:
        if word not in utils.STOP_WORDS_DE_EXTREME and len(word) > 8:
            stemmed_words.append(utils.GLOBAL_STEMMER.stem(word))
            # palabras_stemmed.append(stemmer.stem(palabra))


    unique_and_sorted_words = sorted(list(set(stemmed_words)))

    # 7. Vuelva a ensamblar palabras en una cadena.

    text = ' '.join(unique_and_sorted_words)

    if not text:
        text = 'aura_empty_request'  # <-- Ein eindeutiger, kanonischer Fallback-Schlüssel

    # utils.log_debug(f"palabras clave<última línea<extreme_standardize_prompt_text: 🔎 {text.strip()} 🔍")




    return text.strip()

