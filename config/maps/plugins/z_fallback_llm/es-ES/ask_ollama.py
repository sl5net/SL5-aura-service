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

# config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py

# Ask_ollama.py

import datetime
import os

# importar antorcha


try:
    # 1. INTENTAR: Importación relativa (para python -m... llamada)

    from . import cache_core, normalizer, utils

except ImportError:
    # 2. FALLBACK: Importación sencilla (para cargadores de complementos)

    # IMPORTANTE: Esto sólo funciona si los archivos

    # normalizador.py, cache_core.py, utils.py

    # están todos en la misma carpeta que Ask_ollama.py.


    import cache_core
    import normalizer
    import utils

import hashlib
import json
import logging
import re

# inspección de importación
import sqlite3

# importar sistema operativo
import sys

# importar yake
import time
import urllib.request

# importar fecha y hora
# importar aleatoriamente
from pathlib import Path
from urllib.error import HTTPError, URLError

# de sentencia_transformers importar SentenceTransformer, utilidad



# https://ollama.com/download



# --- CONFIGURACIÓN ---

OLLAMA_API_URL = "http://localhost:11434/api/generate"

# GLOBAL_NORMALIZED_KEY = ""



SESSION_COUNT = 0

LOG_FILE = "/tmp/aura_ollama_debug.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURACIÓN DE AUDIO ---

create_bent_sine_wave_sound = True
try:
    project_root = Path(__file__).resolve().parents[5]
    if str(project_root) not in sys.path:
        sys.path.append(str(project_root))
except ImportError:
    pass


# def utils.log_debug2(mensaje: str):

# caller_info = "DESCONOCIDO:0"

# pila = inspeccionar.pila()

# si len(pila) > 1:

# try:

# nombre de archivo = os.path.nombrebase(pila[1].nombre de archivo)

# numero_linea = pila[1].lineno

# información_llamante = f"{nombre de archivo}:{número_línea}"

# excepto Excepción:

# pasaporte

#
# t = f"⏱️{secDurationSinceExecFunctionStart()}s"

#
# print(f"{t}:[DEBUG_LLM] {caller_info}: {mensaje}", archivo=sys.stderr)

# logging.info(f"{t}:{caller_info}: {mensaje}")



# def normalize_for_hashing(texto):

# devolver extreme_standardize_prompt_text(texto)

# # texto = texto.inferior()

# # texto = re.sub(r'\s+', ' ', texto).strip()

# # devolver texto



# Lista muy agresiva de palabras vacías en alemán (de la biblioteca nltk)

# Aquí puedes definir tu propia lista, incluso más larga.



# def extreme_standardize_prompt_text(texto):

# STOP_WORDS_DE_EXTREME global

#
# # Inicializar el lematizador alemán

# Stemmer = tallo alemán()

#
#
# #1. Todo en minúsculas

# texto = texto.inferior()

#
# #2. Reemplace TODOS los números, horas y símbolos de moneda con comodines

# texto = re.sub(r'\d+([.,]\d+)?', ' [NÚMERO] ', texto) # P.ej. '10', '10,5'

# texto = re.sub(r'[€$£%]', ' ', texto)

#
# #3. Eliminación radical de casi todos los caracteres especiales y signos de puntuación.

# texto = re.sub(r'[^a-zäöüß\s]', ' ', texto)

#
# #4. Reducir los espacios en blanco a un solo espacio y recortar

# texto = re.sub(r'\s+', ' ', texto).strip()

#
# #5. Tokenización (separación de palabras)

# palabras = texto.split()

#
# #6. Detener la eliminación y derivación de palabras

# palabras_provenientes = []

# para palabra en palabras:

# si la palabra no está en STOP_WORDS_DE_EXTREME:

# # Reducir la palabra a su raíz (steming)

# palabras_stemmed.append(stemmer.stem(palabra))

#
# #7. Reensamblar palabras en una cadena

# texto = ' '.join(palabras_derivadas)

#
# utils.log_debug(f"palabras clave<última línea<extreme_standardize_prompt_text: 🔎 {text.strip()} 🔍")

#
# devolver texto.strip()



# --- Prueba de ejemplo ---

# Pregunta 1: “¿Cuántas casas tenemos para elegir en el área?”

# Derivado: "podemos elegir el área de la casa"

# De raíz extrema: "wiel haus hab area wahl" (después de eliminar la palabra vacía)


# Pregunta 2: "La casa es cara, pero muy bonita".

# Extreme Stemmed: "casa cara hermosa"


# Pregunta 3: "¿Cuántas casas hay en el área?"

# Extreme Stemmed: "cuánta área de la casa"


# 1. Cargar el modelo (localmente, aproximadamente 80 MB, muy rápido)

# 'all-MiniLM-L6-v2' es el estándar de la industria para búsquedas locales rápidas

# modelo = SentenceTransformer('todo-MiniLM-L6-v2')


_model = None  # Globaler Cache für das Modell

def get_embedding_model():
    """
    Lazy loader for the embedding model.
    Only loads torch and the model into RAM when actually needed.
    """
    global _model
    if _model is None:
        utils.log_debug("🚀 Loading Embedding Model (Lazy Load)…")
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


# config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py:153


log = logging.getLogger("simulate_conversation")
GITHUB_BASE = "https://github.com/sl5net/SL5-aura-service/blob/master"

def get_github_url(file_path):
    """Erstellt den passenden GitHub-Link aus dem lokalen Pfad."""
    rel_path = ""
    if "STT/" in str(file_path):
        rel_path = str(file_path).split("STT/")[1]
    elif "SL5-aura-service/" in str(file_path):
        rel_path = str(file_path).split("SL5-aura-service/")[1]
    if rel_path:
        url = f"{GITHUB_BASE}/{rel_path}"
        log.debug(f"get_github_url: {file_path} -> {url}")
        return url
    log.warning(f"get_github_url: kein STT/ oder SL5-aura-service/ in Pfad: {file_path}")
    return None


def save_to_aura_db(question, answer, file_path, use_semantics=False):
    """
    Version 1.2.0: Saves dialogue pairs including a semantic vector embedding.
    Enables the 'Self-Learning' loop for the interactive chat.
    """
    prompt_hash = hashlib.md5(question.encode('utf-8')).hexdigest()
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    clean_input = question.lower().replace("?", "").strip()

    embedding_blob = None
    if use_semantics: # Nur für den interaktiven Chat aktivieren
        import pickle
        model = get_embedding_model()
        embedding = model.encode(question)
        embedding_blob = pickle.dumps(embedding)

    github_link = get_github_url(file_path)

    try:
        # conexión = sqlite3.connect(DB_PATH)

        conn = sqlite3.connect(utils.DB_FILE, timeout=90)
        conn.execute("PRAGMA journal_mode=WAL;")

        cursor = conn.cursor()

        # 1. Guardar en 'mensajes' (ahora incluye INTEGRACIÓN)

        cursor.execute("""
            INSERT OR IGNORE INTO prompts (hash, prompt_text, last_used, clean_input, keywords, embedding)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (prompt_hash, question, now, clean_input, "radio_deep_dive", embedding_blob))

        # 2. Guardar en 'respuestas'

        cursor.execute("""
            INSERT INTO responses (prompt_hash, response_text, created_at, usage_count, comment)
            VALUES (?, ?, ?, ?, ?)
        """, (prompt_hash, answer, now, 0, github_link))

        # 3. Actualizar la tabla de seguimiento

        current_mtime = os.path.getmtime(file_path)
        cursor.execute("""
            INSERT OR REPLACE INTO radio_processed_files (file_path, last_mtime, last_generated)
            VALUES (?, ?, ?)
        """, (str(file_path), current_mtime, now))

        conn.commit()
        conn.close()
        # utils.log_debug(f"✅ Guardado (incluido vector): {pregunta[:30]}…")

    except Exception as e:
        print(f"Database Error: {e}")


def get_semantic_match(user_text):
    # 1. Codifique la entrada del usuario una vez


    from sentence_transformers import util
    model = get_embedding_model()
    user_embedding = model.encode(user_text, convert_to_tensor=True)
    try:
        conn = sqlite3.connect(utils.DB_FILE, timeout=90)
        c = conn.cursor()
        # 2. Obtener incrustaciones PRECALCULADAS (BLOB)

        c.execute("SELECT hash, embedding FROM prompts WHERE embedding IS NOT NULL")
        rows = c.fetchall()
        best_hash, max_sim = None, 0.0

        SEMANTIC_THRESHOLD = 0.7  # Live-Betrieb
        # UMBRAL SEMÁNTICO = -1,0 # La prueba siempre coincide


        for db_hash, blob in rows:
            # 3. Cargue el vector desde BLOB (¡aquí no hay model.encode!)

            import pickle

            import torch
            db_embedding = torch.from_numpy(pickle.loads(blob)).to(user_embedding.device)
            # db_embedding = model.encode(texto_usuario, convert_to_tensor=True)


            similarity = util.cos_sim(user_embedding, db_embedding).item()

            if similarity > max_sim:
                max_sim, best_hash = similarity, db_hash
        if best_hash and max_sim > SEMANTIC_THRESHOLD:
            c.execute("SELECT response_text FROM responses WHERE prompt_hash=? LIMIT 1", (best_hash,))
            res = c.fetchone()

            conn.close()

            if res:
                utils.play_cache_hit_sound()
                return res[0]
        return None
    except Exception as e:
        utils.log_debug(f"Semantic Error: {e}")
        return None


# def get_semantic_match_22222(texto_usuario):

# """

# Realiza una búsqueda semántica de la mejor respuesta coincidente.

# Utiliza similitud de coseno para encontrar coincidencias incluso sin superposiciones exactas de palabras clave.

# """

# # utils.init_db()

#
# # Convertir la entrada del usuario en una incrustación vectorial

# user_embedding = model.encode(texto_usuario, convert_to_tensor=True)

#
# try:

# conexión = sqlite3.connect(utils.DB_FILE)

# c = conexión.cursor()

# # Obtener incrustaciones precalculadas de la base de datos

# c.execute ("SELECCIONAR hash, texto_indicación DESDE indicaciones")

# filas = c.fetchall()

#
# utils.log_debug(f"DEBUG: La búsqueda semántica cargó {len(rows)} incrustaciones desde {utils.DB_FILE}")

#
# best_hash = Ninguno

# max_similitud = 0.0

# umbral = 0,3

# umbral = -1,0

#
# para fila en filas:

# db_hash, db_text = fila[0], fila[1]

#
# # Calcular similitud semántica

# db_embedding = model.encode(db_text, convert_to_tensor=True)

# similitud = util.cos_sim(user_embedding, db_embedding).item()

#
# si similitud > max_similitud:

# max_similitud = similitud

# mejor_hash = db_hash

#
# si best_hash y max_similarity > umbral:

# utils.log_debug(f"🧠 ¡Coincidencia semántica! Puntuación: {max_similarity:.2f}")

#
# utils.log_debug(f"🚀 ¡Se encontró una coincidencia instantánea! (Hash: {best_hash[:8]})")

#
# c.ejecutar(

# "SELECCIONE texto_respuesta DE las respuestas DONDE símbolo_hash=? ORDENAR POR calificación DESC, creado_en DESC LÍMITE 1",

# (mejor_hash,))

# resp_row = c.fetchone()

# conexión.cerrar()

#
# si resp_row:

# utils.play_cache_hit_sound()

# # return f"[MODO INMEDIATO]: {resp_row[0]}"

# devolver f"{resp_row[0]}"

#
# devolver texto_db

#
# regresar Ninguno

# excepto excepción como e:

# utils.log_debug(f"Error semántico: {e}")

# regresar Ninguno


# --- COINCIDENCIA EN MODO INSTANTÁNEO ---

def get_instant_match(user_text):
    """
    Sucht in der DB nach Keywords, die dem User-Text am ähnlichsten sind.
    Nutzt Python Set-Intersection (Schnittmenge) statt LLM.
    """
    # utils.init_db()


    # 1. Divida el texto del usuario en palabras (normalización simple)

    # EXAMPLE: xs

    user_words = set(re.sub(r'[^\w\s]', '', user_text.lower()).split())
    # Elimine las palabras irrelevantes para una mejor coincidencia (opcional pero útil)

    stop_words = {"computer", "aura", "bitte", "danke", "und", "oder", "wie", "was", "ist", "der", "die", "das",
                  "sofort", "schnell", "instant"}
    user_relevant = user_words - stop_words

    if not user_relevant:
        return None

    # utils.log_debug(f"🚀 MODO INSTANTÁNEO: Buscando coincidencia para {user_relevant}...")


    try:
        conn = sqlite3.connect(utils.DB_FILE)
        c = conn.cursor()

        # Cargue todas las indicaciones que tengan palabras clave

        c.execute("SELECT hash, keywords FROM prompts WHERE keywords IS NOT NULL")
        rows = c.fetchall()

        best_hash = None
        best_score = 0

        for row in rows:
            db_hash = row[0]
            db_keywords_str = row[1]
            if not db_keywords_str: continue

            db_keywords = set(db_keywords_str.split())

            # Contar coincidencias (Intersección)

            matches = user_relevant.intersection(db_keywords)
            score = len(matches)

            if score > best_score:
                best_score = score
                best_hash = db_hash

        # Decisión: Necesitamos al menos 1 palabra significativa como acierto.

        if best_score >= 1:
            utils.log_debug(f"🚀 Instant Match gefunden! Score: {best_score} (Hash: {best_hash[:8]})")

            # Sube una respuesta a este hash (prefiere las bien calificadas)

            c.execute(
                "SELECT response_text FROM responses WHERE prompt_hash=? ORDER BY rating DESC, created_at DESC LIMIT 1",
                (best_hash,))
            resp_row = c.fetchone()
            conn.close()

            if resp_row:
                utils.play_cache_hit_sound()
                # return f"[MODO INMEDIATO]: {resp_row[0]}"

                return f"{resp_row[0]}"
        else:
            utils.log_debug("🚀 Kein ausreichender Match im Instant Modus.")
            conn.close()

        return None

    except Exception as e:
        utils.log_debug(f"Instant Mode Error: {e}")
        return None


# Ask_ollama.py



# def get_professional_keywords(texto):

# devolver extreme_standardize_prompt_text(texto)

#
# """

# Enfoque híbrido: primero filtre la basura y luego determine las palabras clave.

# """

# #1. Lista de palabras vacías para comandos de voz

# # ignorar_palabras = {

# # "aura", "computadora", "pc", "sistema", "hola", "oye", "por favor", "gracias",

# # "crear", "hacer", "hacer", "hacer", "generar", "mostrar", "mostrar",

# # "un", "una", "una", "el", "el", "ese", "y", "o", "con",

# # "reglas", "regla", "texto", "cadena" # A menudo palabras de relleno en su contexto

# # }

#
#
# sinónimos = {

# # comandos

# "crear": "nuevo", "crear": "nuevo", "generar": "nuevo", "hacer": "nuevo",

# "hacer": "nuevo", "escribir": "nuevo", "añadir": "nuevo", "nuevo": "nuevo",

# # Información

# "mostrar": "información", "mostrar": "información", "dónde": "información", "cómo": "información", "ayuda": "información", "explicar": "información",

# # Borrar

# "eliminar": "del", "eliminar": "del", "olvidar": "del",

# # Contexto

# "config": "config", "configuración": "config", "configuración": "config",

# "regex": "regla", "reglas": "regla", "patrón": "regla"

# }

#
# ignorar_palabras = {

# "aura", "computadora", "pc", "sistema", "hola", "hola", "hola",

# "por favor", "gracias", "tiempo", "sólo", "rápido", "en breve",

# "un", "una", "una", "una", "una",

# "el", "el", "ese", "dem", "den",

# "y", "o", "con", "de", "en", "en", "a", "para", "en", "para",

# "es", "son", "era", "haría", "puede", "tú", "yo", "y", "yo"

# }

#
# try:

# # Texto limpio

# palabras = re.findall(r'\w+', text.lower())

#
# tokens_finales = []

# para w en palabras:

# #1. ¿Ignorar?

# si w en ignorar_palabras:

# continuar

#
# #2. ¿Reemplazar sinónimo?

# si w en sinónimos:

# final_tokens.append(sinónimos[w])

# demás:

# #3. mantén tu palabra

# tokens_finales.append(w)

#
# si no son tokens_finales:

# devolver ""

#
# # 4. Ordenar: "Luz encendida" y "En luz" se vuelven idénticos ("en luz")

# # final_kws = ordenado(lista(conjunto(final_tokens)))

# # devolver " ".join(final_kws)

#
#
#
#
#
# palabras_relevantes = [w para w en final_tokens si w no está en ignore_words y len(w) > 2]

# clean_text = " ".join(palabras_relevantes)

#
# si no texto_limpio:

# return "" # Sin palabras clave (mejor que basura)

#
# # Prueba YAKE en el texto limpio

# importar yake

# kw_extractor = yake.KeywordExtractor(lan="de", n=1, dedupLim=0.9, arriba=3)

# palabras clave = kw_extractor.extract_keywords(texto_limpio)

#
# # Devolver lista ordenada

# final_kws = ordenado([k[0].lower() para k en palabras clave])

# devolver " ".join(final_kws)

#
# excepto ImportError:

# # Respaldo sin YAKE

# devolver " ".join(ordenado(lista(conjunto(palabras_relevantes))))

# excepto Excepción:

# devolver ""



# --- AYUDANTE ---

def clean_text_for_typing(text):
    # EXAMPLE: incógnita. - VAR äöüÄÖÜß

    allowed_chars = r'[^\w\s\.,!\?\-\(\)\[\]\{\}<>äöüÄÖÜß:;\'"\/\\@\+\=\~\#\%]'
    text = re.sub(allowed_chars, '', text)
    # EXAMPLE: Ninguno

    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_readme_content():
    try:
        readme_path = Path(__file__).parent / "README_AI-delang.md"
        if readme_path.exists():
            return readme_path.read_text(encoding='utf-8').strip()[:6000]

        hint = (
            "README_AI-delang.md nicht gefunden.\n"
            "Bitte erstelle sie mit einer großen AI (z.B. Claude/GPT) und folgendem Prompt:\n\n"
            "---\n"
            "Lies die Datei README.md dieses Projekts und erstelle daraus eine kompakte\n"
            "Version für ein lokales Ollama-Modell (llama3.2, 3B Parameter).\n"
            "Anforderungen:\n"
            "- Max 2000 Zeichen\n"
            "- Kein Markdown, nur Fließtext\n"
            "- Fakten: Python, Regeln als Tupel in FUZZY_MAP_pre.py,\n"
            "  Pipeline: Vosk → PUNCTUATION_MAP → FUZZY_MAP_pre → LanguageTool → FUZZY_MAP\n"
            "- Trigger: /tmp/sl5_record.trigger\n"
            "- Kein GUI, kein JSON, kein YAML\n"
            "- Sprache: Deutsch, technisch, direkt\n"
            "Speichern als README_AI-delang.md\n"
            f"Speichern als: {readme_path}"
            "---"
        )
        print(hint)
        log.info(hint)

        return None
    except Exception as e:
        return None
        utils.log_debug(f"get readme Error: {e}")



def get_clipboard_content():
    if not utils.BRIDGE_FILE.exists(): return None
    try:
        content = utils.BRIDGE_FILE.read_text(encoding='utf-8').strip()
        if content:
            return content
        return None
    except Exception:
        return None


def load_history():
    if not utils.MEMORY_FILE.exists(): return []
    try:
        with open(utils.MEMORY_FILE, 'r', codificación='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_to_history(user_text, ai_text):
    history = load_history()
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": ai_text})
    if len(history) > utils.MAX_HISTORY_ENTRIES * 2:
        history = history[-(utils.MAX_HISTORY_ENTRIES * 2):]
    try:
        with open(utils.MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def secDauerSeitExecFunctionStart(reset=False):
    # Si reset=True O la función se ejecuta por primera vez: establezca la hora

    if reset or not hasattr(secDauerSeitExecFunctionStart, "start_time"):
        secDauerSeitExecFunctionStart.start_time = time.time()
        return 0.00

    # Calcular diferencia

    duration = time.time() - secDauerSeitExecFunctionStart.start_time
    return round(duration, 2)


def check_static_guardrails(text_raw):
    """
    Fängt Fragen ab, die auf falschen Annahmen basieren,
    bevor sie teure AI-Zeit verschwenden.
    """
    text = text_raw.lower()

    user_keywords_stict = ["benutzer", "user", "account", "konto", "login", "anmelden", "registrieren", "whatsapp"]
    # Si ocurre "Usuario" Y una "Acción" -> Bloquear.

    if any(k in text for k in user_keywords_stict):
        return (
            "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
            "Es gibt keine Accounts, Passwörter, Logins . "
            "Du bist der einzige Nutzer (Besitzer des Geräts)."
        )

    forbidden_terms = ["account erstellen", "passwort ändern", "login", "neuer benutzer"]
    if any(term in text.lower() for term in forbidden_terms):
        return (
            "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
            "Es gibt keine Accounts, Passwörter und Logins . "
            "Du bist der einzige Nutzer (Besitzer des Geräts)."
        )

    # 1. Gestión de usuarios (no existe)

    user_keywords = ["benutzer", "account", "konto", "login", "anmelden", "registrieren", "whatsapp"]
    user_actions = ["entfernen", "löschen", "erstellen", "hinzufügen", "ändern", "wechseln", "neu"]

    # Si ocurre "Usuario" Y una "Acción" -> Bloquear.

    if any(k in text for k in user_keywords) and any(a in text for a in user_actions):
        return (
            "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
            "Es gibt keine Accounts oder Passwörter, Logins. "
            "Du bist der einzige Nutzer (Besitzer des Geräts)."
        )

    # 2. Desencadenar malentendidos en los archivos

    # Cuando se le solicita configuración EN el archivo de activación

    # if "trigger" en texto y ("konfigurier" en texto o "schreib" in text or "inhalt" in text or "make update" in text):
    #     return (
    #         "Die Datei '.sl5_record.trigger' es uno puro archivo de control (Palanca). "
    #         "Erstellen = Aufnahme Start/Stop. "
    #         "Konfigurationen gehören ausschließlich nach 'config/'."
    #     )

    return None


def execute(match_data):
    print("\n--- DEBUG START 28.4.'26 21:31 Tue ---")

    # play_cache_hit_sound()


    secDauerSeitExecFunctionStart(reset=True)  # <--- Startschuss!

    utils.SESSION_COUNT += 1

    global GLOBAL_NORMALIZED_KEY

    # 1. CALCULAR LA CLAVE CANÓNICA UNA VEZ


    try:
        match_obj = match_data['regex_match_obj']

        # --- ARRANQUE DE INICIO ---

        # En lugar de comprobar match_obj.lastindex (que falta en el simulacro),

        # simplemente verifiquemos la longitud de la tupla groups().

        # Esto funciona en Python re Y en objetos simulados.

        groups = match_obj.groups()

        # user_input_raw = (match_obj.group(2) si len(grupos) >= 2 más

        # match_obj.group(1) si len(grupos) >= 1 más

        # match_obj.group(0)).strip()


        # siempre toma el último grupo

        user_input_raw = groups[-1].strip() if groups else match_obj.group(0).strip()
        user_input_raw = user_input_raw.lower()

        utils.log_debug(f"⏱️{secDauerSeitExecFunctionStart()}s")
        utils.log_debug(f"Input: {user_input_raw}:'{user_input_raw}'")

        if not user_input_raw: return "Nichts gehört."

        GLOBAL_NORMALIZED_KEY = normalizer.create_ultimate_cache_key(user_input_raw)
        hash_of_normalized_key = cache_core.prompt_key_to_hash(GLOBAL_NORMALIZED_KEY)

        # utils.log_debug(f"GLOBAL_NORMALIZED_KEY: {GLOBAL_NORMALIZED_KEY}")

        # utils.log_debug(f"hash_of_normalized_key: {hash_of_normalized_key}")


        keywords_str = GLOBAL_NORMALIZED_KEY

        # Capta tonterías inmediatamente (0,00s)

        static_reply = check_static_guardrails(user_input_raw)
        if static_reply:
            utils.log_debug(f"🛡️ Guardrail ausgelöst: '{user_input_raw}'")
            return static_reply

        if "vergiss alles" in user_input_raw.lower():
            if utils.MEMORY_FILE.exists():
                try:
                    utils.MEMORY_FILE.unlink()
                except Exception:
                    pass
            return "Gedächtnis gelöscht."

        # --- VERIFICACIÓN DEL MODO INSTANTÁNEO ---

        # Si el usuario dice "inmediatamente", "rápidamente" o "al instante",

        # SÓLO buscamos en la base de datos la mejor concordancia de palabras clave.

        instant_triggers = ["sofort", "schnell", "instant"]
        if any(w in user_input_raw.lower() for w in instant_triggers):
            utils.log_debug("Mode: INSTANT REQUEST")
            instant_response = get_instant_match(user_input_raw)

            if instant_response:
                return instant_response
            else:
                return "Dazu habe ich noch keine schnelle Antwort gespeichert."

        # --- PERFIL DE AURA TECH (Fundamentos y hechos) ---

        # --- PERFIL DE AURA TECH (Fundamentos y hechos) ---

        AURA_TECH_PROFILE_2911252235Sat = (  # noqa: F841
            "Du bist SL5 Aura. Antworte auf Deutsch. Sei extrem kurz.\n"

            "ANWEISUNG FÜR DICH:\n"
            "Unterscheide selbstständig:\n"
            "1. WISSENSFRAGE (Wo/Was/Wie) -> Nur den Fakt nennen (1 Satz).\n"
            "2. HANDLUNG (Erstelle/Schreibe) -> Nur Dateiname und Code-Block.\n\n"

            "BEISPIELE (Nutze diesen Stil):\n"
            "User: 'Wo sind die Configs?'\n"
            "Aura: Die Konfigurationen liegen im Ordner 'config/maps/'.\n\n"

            "User: 'Wie starte ich die Aufnahme?'\n"
            "Aura: Durch Erstellen der Datei '/tmp/sl5_record.trigger'.\n\n"

            "SYSTEM-FAKTEN (Strict Grounding):\n"
            "About: Privacy-first voice assistant framework. Core is offline. Scripts allow hybrid usage.\n"
            "1. Tech Stack: Python (87%), Shell (9%), PowerShell (2%), Vosk (Offline-Modelle ~4GB), LanguageTool. KEIN Java/C++, KEINE .exe, KEIN PDF-Support.\n"
            "2. Interface: 100% 'Headless' Hintergrund-Dienst. Interaktion NUR via Mikrofon (Input) & Terminal-Logs (Output). ES GIBT KEINE 'OBERFLÄCHE', KEINE GUI, KEIN Web-UI.\n"
            "3. Logik & Config: KEIN JSON/YAML! Regeln sind reine Python-Dateien (z.B. 'FUZZY_MAP_pre.py') mit Regex-Listen.\n"
            "   - In config/ befinden sich alle KONFIGURATION .\n"
            "   Beispiele: `^.*$` (Catch-All), `^.+$` (Nicht leer) oder spezifisch `^meinBefehl$`. (KEIN Button, reiner Code!)\n"
            "   - Syntax WICHTIG: Nutze Python 're' Syntax. Für Alternativen (ODER) nutze zwingend '|' ohne Leerzeichen!\n"
            "     FALSCH: `(Hans Max Luis)` -> RICHTIG: `(Hans|Max|Luis)`\n"
            "     FALSCH: `[Licht Lampe]`   -> RICHTIG: `(Licht|Lampe)`\n"
            "   - Lade-Reihenfolge: Plugin-ORDNER werden alphabetisch geladen (A-Z).\n"
            "   - Pipeline: Regeln laufen Top-Down. Text wird durchgereicht & verändert. Mehrere Regeln können nacheinander greifen (kumulativ).\n"
            "   - Stopp (Full-Match): Die Pipeline stoppt, wenn ein Regex von Anfang (`^`) bis Ende (`$`) matcht. Da Voice-Input einzeilig ist, sind Anker wichtig.\n"
            "   - In config/ befinden sich alle KONFIGURATIONEN.\n"
            "   Beispiele: `^.*$` (Catch-All), `^.+$` (Nicht leer). \n"
            # EXAMPLE: Canciller

            "   Beispiel Regel-Tupel: ('Angela Merkel', r'^(Canciller|angie)$', 100, {'flags': re.IGNORECASE})\n"
            "4. Plugins & Erweiterbarkeit: Jede Regex kann 'on_match_exec' nutzen. Plugins erhalten Daten, verarbeiten sie kreativ und geben Text zurück.\n"
            "   - Beispiele: Offline-Wikipedia, SQLite-Booksearch, Ollama AI (Lokal).\n"
            "   - Ausnahme: Das 'Translate'-Plugin nutzt Online-APIs (mit lokalem Cache), benötigt also Internet.\n"
            "5. Security & Tools: \n"
            "   - Dateisuche: NUR via 'git ls-files | fzf'.\n"
            "   - Findet Aura eine versteckte '. Dateiname .py'(Punkt am Anfang), nutzt es deren Passwort zum Entpacken von _ einName .zip (OPTIONAL, nicht vorhanden).\n"
            "6. OS: Linux, Windows, macOS. (Kein Smartphone).\n"
            "7. Installation: Dauert ca. 10-20 Minuten (Download großer Sprachmodelle, >4GB). Updates sind schnell, Erst-Installation NICHT.\n"
            "   - App-Update: Via 'git pull' (Sekunden).\n"
            "   - Modell-Update: Lösche den entsprechenden Ordner in 'models/' und starte das Setup-Skript erneut. (Dauert 10-20 Min, >4GB Download).\n"
            "8. Externe Trigger (CopyQ, AutoKey, AHK): Steuerung erfolgt NUR durch Erstellen einer leeren Datei (File-Watch). KEINE API, KEINE Config!\n"
            "   - Pfad Linux/Mac: `/tmp/sl5_record.trigger`\n"
            "   - Pfad Windows: `c:\\tmp\\sl5_record.trigger`\n"
            "   - Funktion: Datei erstellen = Aufnahme/Verarbeitung starten.\n"
            "9. Verhalten: Erfinde KEINE visuellen Elemente. Fasse dich EXTREM kurz (Max 15 Wörter)."

            "BEISPIEL-DIALOGE (Lerne die Unterscheidung!):\n"
            "User: 'Wo finde ich die Konfiguration?'\n"
            "Aura: Die Konfigurationen liegen im Ordner 'config/'.\n\n"

            "User: 'Welche Datei startet die Aufnahme in Linux?'\n"
            "Aura: Das Erstellen der Datei '/tmp/sl5_record.trigger' comienza el Grabación  en linux .\n\n"

            "BEISPIEL-INTERAKTION (Folge diesem Format strikt!):\n"
            "User: 'Erstelle Regeln für Licht.'\n"
            "Aura: Erstelle 'licht_control.py' in 'config/maps/':\n"
        )

        AURA_TECH_PROFILE_2911252311Sat_8sec_superFast = (  # noqa: F841
            "Du bist SL5 Aura, ein Offline-Sprachassistent.\n"
            "Deine Aufgabe: Technischer Support. Antworte EXTREM kurz.\n\n"

            "STRIKTE REGELN:\n"
            "1. Aura nutzt NUR Python-Dateien (.py) und Tupel.\n"
            "2. Wenn der User nach YAML, JSON oder Importen fragt: IGNORIERE ES.\n"
            "3. Schreibe KEINEN Programm-Logik-Code (Kein 'with open', kein 'import', kein 'def').\n"

            "- KEIN 'Meta-Talk' (Kein: 'Du hast gefragt...', Kein: 'Hier ist der Code').\n"
            "- KEINE Höflichkeitsfloskeln.\n"
            "- Wenn Code gefragt ist: ZUERST Dateiname (snake_case.py), DANN Code-Block.\n"
            "- Wenn Info gefragt ist: Nur den Fakt nennen (Max 1 Satz).\n\n"

            "SYSTEM-WISSEN:\n"
            "1. Config-Ort: 'config/maps/' (Reine Python-Dateien).\n"
            "2. Logik: Regex Listen (Top-Down Pipeline). Nutze Python 're'.\n"
            "3. Trigger: Datei '/tmp/sl5_record.trigger' comienza Grabación.\n"
            "4. Suche: Nur 'git ls-files'. Keine DB.\n"
            "5. Umgebung: Headless (Keine GUI). Offline (Kein 'requests' Modul nutzen!).\n\n"

            "MUSTER-ANTWORTEN (Kopiere diesen Stil strikt):\n\n"

            "User: Wo liegen die Konfigurationen?\n"
            "Aura: Die Konfigurationen befinden sich als Python-Dateien im Ordner 'config/maps/'.\n\n"

            "User: Wie starte ich die Aufnahme?\n"
            "Aura: Durch Erstellen der Datei '/tmp/sl5_record.trigger'.\n\n"

            "User: Erstelle eine Regel für Bundeskanzlerin.\n"
            # EXAMPLE: Canciller

            "   Beispiel Regel-Tupel: ('Angela Merkel', r'^(Canciller|angie)$', 100, {'flags': re.IGNORECASE})\n"
            "User: Erstelle eine Regel für Full-Match.\n"
            "   Beispiele: `^.*$` (Catch-All), `^.+$` (Nicht leer). \n"
            "```"
        )

        AURA_TECH_PROFILE = (
            "Du bist SL5 Aura, der Offline-Voice-Assistant. Antworte EXTREM kurz.\n\n"

            "WICHTIGSTE REGELN:\n"
            "1. KEIN 'Meta-Talk' (Keine Einleitungen, kein 'Hier ist der Code').\n"
            "2. Wenn du etwas nicht weißt oder es nicht zu Aura gehört: Sage 'Dazu habe ich keine Infos.' (Nicht leer bleiben!).\n"
            "3. Bei BEFEHLEN (Erstelle Regel): Antworte NUR mit dem Dateinamen und dem Regel-Tupel.\n\n"

            "SYSTEM-WISSEN:\n"
            "- Config: 'config/maps/' (Python-Dateien).\n"
            "- Logik: Regex Listen als Tupel.\n"
            "- Pipeline: Regeln laufen Top-Down. Text wird durchgereicht & verändert. Mehrere Regeln können nacheinander greifen (kumulativ).\n"
            "- Vosk (Audio) > Maps (PUNCTUATION_MAP.py)  > Maps (...pre.py) > LanguageTool (Opt.) > Maps (...post.py) > Output (Text & TTS).\n"
            "- Plugins & Erweiterbarkeit: Jede Regex kann 'on_match_exec' nutzen. Plugins erhalten Daten, verarbeiten sie kreativ und geben Text zurück.\n"

            "- Umgebung: Headless (Keine GUI). Offline.\n\n"

            "MUSTER-ANTWORTEN (Kopiere diesen Stil):\n\n"

            "User: Wo sind die Configs?\n"
            "Aura: Die Konfigurationen liegen im Ordner 'config/maps/'.\n\n"

            "User: Erstelle eine PUNCTUATION-Regel für Stern.\n"
            "```python\n"
            "# PUNCTUATION-Tupel: (Suchwort, neues Wort)\n"
            "'stern': '*'\n"
            "```\n\n"

            "User: Erstelle eine Regex-Regel für Kanzlerin.\n"
            "Aura: kanzlerin_map.py\n"
            "```python\n"
            "# Regel-Tupel: (Ersetzung, Regex, Priorität, Flags)\n"
            # EXAMPLE: Canciller

            "('Angela Merkel', r'^(Canciller|angie)$', 100, {'flags': re.IGNORECASE})\n"
            "```\n\n"

            "User: Erstelle eine Catch-All Regel.\n"
            "Aura: FUZZY_MAP_pre.py\n"
            "('immer Ergebnis', r'^.*$')\n"
            "```python\n"
            # EXAMPLE: Ninguno

            "('Ersetzung', r'^.*$')\n"
            "User: Erstelle Regel mit Plugin Wiki.\n"
            "Aura: wiki_plugin.py\n"
            "```python\n"
            # EXAMPLE: wiki

            "('Ersetzung', r'^wiki (.*)$', 50, {'on_match_exec': 'plugins.wiki_search'})\n"

        )

        AURA_TECH_PROFILE_3011250003Sun = (  # noqa: F841
            "Du bist SL5 Aura, der Offline-Voice-Assistant. Antworte kurz & präzise.\n\n"

            "WICHTIGSTE REGELN:\n"
            "1. KEIN 'Meta-Talk'. Antworte direkt mit der Lösung.\n"
            "2. Wenn User nach Regeln fragen: Gib IMMER ein Python-Beispiel (Dateiname + Code).\n"
            "3. DATEINAMEN: Passend zum Thema (z.B. 'config/maps/pdf/de-DE/FUZZY_MAP_pre.py').\n"
            "4. WICHTIG: Regex matcht auf GESPROCHENEN TEXT, nicht auf Dateien!\n"
            # EXAMPLE: archivo de mapas de configuración py

            "   - Falsch: r'configuración/mapas/archivo.py'\n"
            # EXAMPLE: abrir archivo

            "   - Richtig: r'abierto archivo (.*)'\n\n"

            "SYSTEM-WISSEN:\n"
            "- Config: 'config/maps/' (Python-Dateien).\n"
            # EXAMPLE: expresión regular

            "- Logik: Tupel `('Ergebnis-Text', r'expresión regular', Prio, Flags)`.\n"
            "- Pipeline: Regeln laufen Top-Down. Text wird durchgereicht & verändert. Mehrere Regeln können nacheinander greifen (kumulativ).\n"
            "- Vosk (Audio) > Maps (FUZZY_MAP_pre.py) > LanguageTool (Opt.) > Maps (FUZZY_MAP.py) > Output (Text & TTS).\n"


            "- Plugins & Erweiterbarkeit: Jede Regex kann 'on_match_exec' nutzen. Plugins erhalten Daten, verarbeiten sie kreativ und geben Text zurück.\n"

            "- Trigger: '/tmp/sl5_record.trigger' (Comienza/Interrumpido Grabación).\n"
            "- Umgebung: Headless, Offline.\n\n"


            "MUSTER-ANTWORTEN (Kopiere diesen Stil):\n\n"

            "User: Wo sind die Regeln?\n"
            "Aura: In 'config/maps/' als Python-Dateien.\n\n"

            "User: Wo sind die Configs?\n"
            "Aura: Die Konfigurationen liegen im Ordner 'config/maps/'.\n\n"

            "User: Erstelle eine Regel für Kanzlerin.\n"
            "Aura: kanzlerin_map.py\n"
            "```python\n"
            "# Regel-Tupel: (Name, Regex, Priorität, Flags)\n"
            # EXAMPLE: Canciller

            "('Angela Merkel', r'^(Canciller|angie)$', 100, {'flags': re.IGNORECASE})\n"
            "```\n\n"

            "User: Erstelle eine Catch-All Regel.\n"
            "Aura: config/maps/system/de-DE/FUZZY_MAP_pre.py\n"
            "```python\n"
            # EXAMPLE: Ninguno

            "('Kein Treffer', r'^.*$', 10, {})\n"
            "```\n\n"

            "User: Erstelle Regel mit Plugin Wiki.\n"
            "Aura: wiki_plugin.py\n"
            "```python\n"
            # EXAMPLE: wiki

            "('Wiki', r'^wiki (.*)$', 50, {'on_match_exec': 'plugins.wiki_search'})\n"
            "```"
        )

        AURA_NORMAL_PROFILE = (
            "Du bist SL5 Aura, der Offline-Voice-Assistant. Antworte normal ausführlich und hilfreich. "
            "Deine Antworten dürfen freundlicher sein und mehr Kontext liefern, aber bleibe präzise. "
            "Du bist NICHT an die EXTREM-Kürze des Tech-Modus gebunden.\n\n"

            "REGELN:\n"
            "1. Sei hilfreich und informativ. Liefere eine komplette Antwort.\n"
            "2. Wenn der Benutzer eine Konfiguration oder Regel erstellen will, antworte wie im Tech-Profil (Dateiname und Code-Block), aber füge eine kurze Erklärung hinzu.\n"
            "3. Bei allgemeinen Fragen antworte in ganzen Sätzen und einem angenehmen Ton.\n\n"

            "SYSTEM-WISSEN:\n"
            "- Du hast Zugriff auf Config und Code-Logik. Siehe Tech-Profil für Details.\n"

            "MUSTER-ANTWORTEN:\n"
            "User: Was ist ein Haus?\n"
            "Aura: Ein Haus ist ein dauerhaftes, überdachtes Bauwerk, das als Unterkunft oder Schutz dient.\n\n"

            "User: Erstelle eine PUNCTUATION-Regel für Stern.\n"
            "Aura: Gerne, hier ist die Regel für Stern:\n"
            "```python\n"
            "# PUNCTUATION-Tupel: (Suchwort, neues Wort)\n"
            "'stern': '*'\n"
            "```\n"
        )


        full_match_text = match_obj.group(0).lower()
        slow_triggers = ["slow", "langsam", "genau", "gründlich", "normal"]
        # is_slow_request = cualquiera(w en user_input_raw.lower() para w en slow_triggers)

        is_slow_request = any(w in full_match_text for w in slow_triggers)

        if is_slow_request:
            utils.log_debug("Mode: SLOW/DETAILED")
            system_role = AURA_NORMAL_PROFILE  # Der ausführliche Prompt
            ollama_params = {
                "temperature": 0.3,
                "mirostat": 2,
                "num_predict": 512
            }
            bypass_cache = True  # Im Slow-Mode immer frisch generieren
        else:
            system_role = AURA_TECH_PROFILE  # Der extrem kurze Prompt
            ollama_params = {
                "temperature": 0.1,
                "num_predict": 100
            }
            bypass_cache = False  # Normaler Modus nutzt den semantischen Cache

        print("\n--- DEBUG START 28.4.'26 21:31 Tue ---")
        print(f"Raw Input: '{user_input_raw}'")
        print(f"Is Slow Triggered: {is_slow_request}")
        print(f"Selected Profile: {'NORMAL' if is_slow_request else 'TECH'}")






















        trigger_clipboard = ["zwischenablage", "clipboard", "kopierten text", "zusammenfassung"]
        trigger_readme = ["hilfe", "dokumentation", "readme", "read me", "wie funktioniert", "was kannst du"]
        no_cache_keywords = ["witz", "spruch", "zufall", "random"]

        context_data = ""
        mode_prefix = "STD"  # Standard Mode
        system_role = f"{AURA_TECH_PROFILE}"
        use_history = True
        input_lower = user_input_raw.lower()
        bypass_cache = bypass_cache

        # --- DETECCIÓN DE MODA Y CARGA DE CONTEXTO ---

        # Aquí sólo determinamos: ¿Qué modo está activo? ¿Qué contexto está cargado?


        # utils.log_debug(f"Entrada: {user_input_raw}:'{user_input_raw}'")

        # utils.log_debug(f"Entrada: {input_lower}:'{input_lower}'")


        if any(w in input_lower for w in no_cache_keywords):
            bypass_cache = True
            utils.log_debug("Cache BYPASS: Zufallswort erkannt.")

        # 1. VERIFICACIÓN DEL PORTAPAPELES

        elif any(w in input_lower for w in trigger_clipboard):
            utils.log_debug("Mode: CLIPBOARD")
            content = get_clipboard_content()
            if content:
                content_preview = content[:50] + str(len(content))
                # El hash del contenido pasa a formar parte del prefijo -> cambios de contenido = cambios de caché

                clip_hash = hashlib.md5(content_preview.encode()).hexdigest()
                mode_prefix = f"CLIP_{clip_hash}"

                context_data = f"\nDATEN ZWISCHENABLAGE:\n'''{content[:8000]}'''\n"
                system_role = "Du bist ein Assistent. Analysiere die Daten."
                use_history = False
                bypass_cache = True

            else:
                return "Zwischenablage ist leer."

        # 2. VERIFICACIÓN LÉAME

        elif any(w in input_lower for w in trigger_readme):
            utils.log_debug("Mode: README")
            readme_content = get_readme_content()
            if readme_content:
                # El hash del archivo Léame pasa a formar parte del prefijo -> cambios en la documentación = cambios en la caché

                readme_hash = hashlib.md5(readme_content.encode()).hexdigest()
                mode_prefix = f"README_{readme_hash}"

                context_data = f"\nPROJEKT DOKUMENTATION:\n'''{readme_content}'''\n"
                system_role = (f"Support-Bot für 'SL5 Aura'. Fakten:\n{AURA_TECH_PROFILE}\nErfinde nichts.")
                use_history = False
            else:
                return "Readme nicht gefunden."

        # 3. PREDETERMINADO (el respaldo es "STD" como se inicializó anteriormente)


        # --- CÁLCULO DE HASH ---


        # 1. SIEMPRE genere palabras clave inmediatamente (para clave de caché Y almacenamiento de base de datos)

        # ¡Esto hace que el caché sea "difuso" -> "Crear regla" y "Crear regla" terminen en el mismo caché!


        # utils.log_debug(f"Palabras clave<ejecutar 🔎 {keywords_str} 🔍")


        # Alternativa: si no se encontraron palabras clave (por ejemplo, solo palabras de relleno), utilice el texto sin formato.

        if not keywords_str:
            base_for_hash = user_input_raw
        else:
            base_for_hash = keywords_str

        # 2. Construya la cadena hash

        if "CLIP" in mode_prefix or "README" in mode_prefix:
            # Con Portapapeles/Léame el contenido (prefijo) debe ser parte del hash

            hash_input_string = f"{mode_prefix}|{base_for_hash}"
        else:
            # En el modo estándar, solo cuenta el conjunto de palabras clave

            # Pregunta: "Aura qué tarde" -> Clave: "ETS|tarde"

            # Pregunta: "¿Qué hora es" -> Clave: "HORAS|tarde" -> ¡HIT!

            hash_input_string = f"STD|{base_for_hash}"

        # utils.log_debug(f"🔑 base_for_hash: '{base_for_hash}'")

        # utils.log_debug(f"🔑 hash_input_string: '{hash_input_string}'")


        # Aviso completo para la IA (permanece como estaba, por contexto)

        full_prompt_for_generation = f"{system_role}\n{context_data}\nUser: {user_input_raw}\nAura:"
        if use_history:
            hist = load_history()
            full_prompt_for_generation = f"{system_role}\nVerlauf: {json.dumps(hist)}\n{context_data}\nUser: {user_input_raw}\nAura:"

        # --- COMPROBACIÓN DE CACHÉ ---


        if not bypass_cache:
            # ¡Ahora buscamos con la palabra clave hash!

            # utils.log_debug(f"11111 hash_input_string: '{hash_input_string}'") # 'STD|aura_empty_request'

            # utils.log_debug(f"11111 GLOBAL_NORMALIZED_KEY: '{GLOBAL_NORMALIZED_KEY}'") # 'aura_empty_request'

            cached_resp, expired = cache_core.get_cached_response(GLOBAL_NORMALIZED_KEY)

            if cached_resp:
                utils.log_debug(f"cached_resp: {cached_resp}")
                if use_history:
                    save_to_history(user_input_raw, cached_resp)
                    # objetivo = utils.DB_FILE

                    # save_to_aura_db(user_input_raw, cached_resp, destino)


                utils.SUM_PER_CACHE = utils.SESSION_CACHE_HITS / utils.SESSION_COUNT if utils.SESSION_COUNT > 0 else 0
                sum_per_cache_str = f"{utils.SUM_PER_CACHE:.1f} {'📉' if utils.SUM_PER_CACHE < utils.SUM_PER_CACHE else '📈'}"
                utils.SESSION_SEC_SUM += secDauerSeitExecFunctionStart()
                utils.SUM_PER_CACHE = utils.SUM_PER_CACHE

                return cached_resp

            # 2. NUEVO: respaldo semántico (si falta la coincidencia exacta o ha caducado)

            semantic_resp = get_semantic_match(user_input_raw)
            if semantic_resp:
                utils.log_debug("🎯 Semantic Cache Hit!")
                utils.SESSION_CACHE_HITS += 1
                return semantic_resp


            if expired:
                utils.log_debug("♻️ Cache Entry EXPIRED.")

            # --- GENERACIÓN DE IA (OLLAMA API) ---

        # utils.log_debug("Caché MISS. Enviando solicitud de API a Ollama...")


        payload = {
            "model": "llama3.2",
            "prompt": full_prompt_for_generation,
            "stream": False,
            "keep_alive": 0,
            "options": {
                "temperature": 0.1,
                **ollama_params,
                "top_k": 20,
                "num_predict": 100,
                "stop": ["User:", "Verlauf:", "System:", "Aura:"]
            }
        }

        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(OLLAMA_API_URL, data=data, headers={'Content-Type': 'application/json'})

            # El tiempo de espera aumentó a 120 segundos por seguridad.

            with urllib.request.urlopen(req, timeout=90) as response:
                api_response = json.loads(response.read().decode('utf-8'))

            utils.SUM_PER_CACHE = (utils.SESSION_CACHE_HITS / utils.SESSION_COUNT) if utils.SESSION_COUNT > 0 else 0
            sum_per_cache_str = f"{utils.SUM_PER_CACHE:.1f} {'📉' if utils.SUM_PER_CACHE < utils.SUM_PER_CACHE else '📈'}"
            utils.SESSION_SEC_SUM += secDauerSeitExecFunctionStart()

            session_sec_average = utils.SESSION_SEC_SUM / utils.SESSION_COUNT if utils.SESSION_COUNT > 0 else 0

            utils.log_debug(
                f"Nr. {utils.SESSION_COUNT} | CACHE_HITS:{utils.SESSION_CACHE_HITS} 📊 CacheHITs/Nr.: {sum_per_cache_str} | "
                f"⌚ Gespart: ~{session_sec_average * utils.SESSION_CACHE_HITS:.1f}s")

            raw_text = api_response.get("response", "")

            utils.log_debug(f"DEBUG: Unzensierte KI-Antwort: '{raw_text[:200]}...'")


            answer_for_all_fallback = (
                "Aura Status: Offline-System, Single-User (Keine Logins/Accounts).\n"
                "Pfade: Configs in 'config/', Regeln in 'config/maps/'.\n\n"

                "FORMAT 1: Einfache Ersetzung (z.B. PUNCTUATION_MAP)\n"
                "Synatx: 'Wort': 'Ersatz'\n"
                "Beispiel: 'stern': '*'\n\n"

                "FORMAT 2: Logik-Regeln (z.B. FUZZY_MAP)\n"
                "Syntax: (Name, Regex, Prio, Flags)\n"
                # EXAMPLE: Canciller

                "Beispiel: ('Merkel', r'^(Canciller|angie)$', 100, {'flags': re.IGNORECASE})\n"
                # EXAMPLE: wiki

                "Beispiel: ('Wiki', r'^wiki (.*)$', 50, {'on_match_exec': 'wiki_search'})\n\n"

                "Doku: https://SL5.de/Aura"
            )

            if not raw_text:
                response = answer_for_all_fallback

            response = clean_text_for_typing(raw_text)

            response.replace('sl5_config.py', ' settings_local.py ')
            response.replace(' sl5_record_trigger.py ', ' /tmp/sl5_record.trigger ')

            response = response.replace('JSON', 'Python')
            response = response.replace('YAML', 'Python')
            response = response.replace('json', 'Python')
            response = response.replace('Aurah ', 'Aura ')
            response = response.replace('config/maps/Ordner', 'config/maps Ordner')

            # No tengo ninguna información sobre eso.

            if 'Dazu habe ich keine Info' in response or 'sl5_record_trigger.py' in response:
                response = answer_for_all_fallback

            if (False  # noqa: E129
                or "r'/tmp" in response # noqa: E127
                or 'user_map.py' in response # noqa: E127
                or 'user_regeln.py' in response): # noqa: E127 E129
                response = answer_for_all_fallback # noqa: E127

            if 'Fehler:' in response or '.json' in response:
                response = answer_for_all_fallback

            # --- GUARDAR (Solo cuando no está en modo bypass) ---

            if not bypass_cache:
                target = utils.DB_FILE

                # Necesitamos asegurarnos de que save_to_aura_db no falle,

                # si 'destino' no es un archivo real.

                try:
                    # save_to_aura_db(user_input_raw, respuesta, destino)

                    save_to_aura_db(user_input_raw, response, target, use_semantics=True)
                except Exception as e:
                    utils.log_debug(f"Speichern in DB fehlgeschlagen: {e}")

                # Alimenta también el caché clásico.

                cache_core.cache_response(
                    tag_keyword=hash_input_string,
                    response_text=response,
                    clean_user_input=user_input_raw,
                    hash_of_normalized_key=hash_of_normalized_key,
                )

            # --- HISTORIAL (Siempre al final, si está activado) ---

            if use_history:
                save_to_history(user_input_raw, response)

            return response

        # --- TRATAMIENTO DE ERRORES ---

        except HTTPError as e:
            # Aquí interceptamos la "Respuesta del servidor: 500".

            if e.code == 500:
                utils.log_debug("❌ OLLAMA SERVER ERROR (500). Ignoriere Fehlertext für User.")
                # Si NO desea que el usuario vea el error:

                return "Ich habe kurz den Faden verloren. Kannst du das wiederholen?"
            else:
                utils.log_debug(f"API HTTP Error: {e.code}")
                return f"Server Fehler: {e.code}"

        except URLError as e:
            # Si Ollama no se ejecuta en absoluto (Conexión rechazada)

            utils.log_debug(f"API Connection Error: {e.reason}")
            return "Fehler: Keine Verbindung zu Ollama."

        except Exception as e:
            # Todos los demás errores

            utils.log_debug(f"API General Error: {e}")
            # devolver "Ocurrió algo".

            return (
                "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
                "Es gibt keine Logins, Accounts. "
                "Du bist der einzige Nutzer (Besitzer des Geräts). "
                "Bitte lese Details in der Dokumentation: https://SL5.de/Aura"
            )






    # config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py:1252

    except Exception as e:
        utils.log_debug(f"API Error: {e}")
        return f"Interner Fehler: {e!s} (2026-0506-0626)"







