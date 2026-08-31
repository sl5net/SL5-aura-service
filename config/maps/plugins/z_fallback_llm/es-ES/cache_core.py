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

# config/maps/plugins/z_fallback_llm/de-DE/cache_core.py

# caché_core.py

# importar re

# importar hashlib


import datetime
import hashlib
import random
import sqlite3

try:
    # 1. INTENTAR: Importación relativa (para python -m... llamada)



    from . import normalizer, utils

except ImportError:
    import normalizer  # noqa: F401
    import utils


# desde pathlib importar ruta

#
# utils.PLUGIN_DIR = Ruta(__archivo__).padre

# utils.MEMORY_FILE = utils.PLUGIN_DIR / "conversation_history.json"

# utils.BRIDGE_FILE = Ruta("/tmp/aura_clipboard.txt")

# utils.DB_FILE = utils.PLUGIN_DIR / "llm_cache.db"


def prompt_key_to_hash(normalized_prompt_key: str):
    prompt_hash = hashlib.sha256(normalized_prompt_key.encode('utf-8')).hexdigest()
    return prompt_hash


# def get_cached_response():

def get_cached_response(prompt_key_to_hash1: str):
    prompt_hash = prompt_key_to_hash(normalized_prompt_key=prompt_key_to_hash1)
    try:
        conn = sqlite3.connect(utils.DB_FILE, timeout=30)
        conn.execute("PRAGMA journal_mode=WAL")
        c = conn.cursor()

        c.execute("SELECT last_used FROM prompts WHERE hash=?", (prompt_hash,))
        row = c.fetchone()
        if not row:
            conn.close()
            return None, False

        try:
            last_used = datetime.datetime.fromisoformat(row[0])
            age = datetime.datetime.now() - last_used
            if age.days > utils.CACHE_TTL_DAYS:
                conn.close()
                return None, True
        except Exception:
            pass

        c.execute("SELECT id, response_text FROM responses WHERE prompt_hash=?", (prompt_hash,))
        rows = c.fetchall()
        if rows:
            chosen_row = random.choice(rows)
            c.execute("UPDATE responses SET usage_count = usage_count + 1 WHERE id = ?", (chosen_row[0],))
            now = datetime.datetime.now().isoformat()
            c.execute("UPDATE prompts SET last_used = ? WHERE hash = ?", (now, prompt_hash))
            conn.commit()
            conn.close()

            utils.SESSION_CACHE_HITS += 1
            lll = (utils.SESSION_CACHE_HITS / utils.SESSION_COUNT) if utils.SESSION_COUNT > 0 else 0
            session_sec_average = utils.SESSION_SEC_SUM / utils.SESSION_COUNT if utils.SESSION_COUNT > 0 else 0
            sum_per_cache_str = f"{lll:.1f}"
            utils.log_debug(f" {utils.SESSION_CACHE_HITS} Cache HITs | CacheHITs/Nr : {sum_per_cache_str}"
                    f" Zeit gespart: ~{session_sec_average * utils.SESSION_CACHE_HITS:.1f}s")
            utils.play_cache_hit_sound()
            return chosen_row[1], False

        conn.close()
        return None, False
    except Exception as e:
        utils.log_debug(f"Exception: {e}")
        return None, False

def cache_response(
    tag_keyword=None,
    response_text=None,
    clean_user_input=None,
    hash_of_normalized_key=None
):
    # utils.log_debug(f"-----------------------------------------------------------------")

    # utils.log_debug(

    # f"1: palabra_clave_etiqueta:{palabra_clave_etiqueta}, "

    # f"texto_respuesta:{cadena(texto_respuesta)[:15]}...., "

    # f"clean_user_input:{clean_user_input}, "

    # f"clave_normalizada:{hash_of_normalized_key}"

    # )

    if not tag_keyword:
        utils.log_debug("⚠️ WARNUNG: cache_response wurde OHNE tag_keyword aufgerufen (None/Leer)!")

    # utils.init_db() # Asegurarse de que la tabla DB exista


    now = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(utils.DB_FILE, timeout=30)
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('BEGIN IMMEDIATE')
        c = conn.cursor()

        # Valide que hash_input_str y Prompt_key_to_hash no sean Ninguno

        if tag_keyword is None or hash_of_normalized_key is None:
            utils.log_debug("❌ ERROR: tag_keyword is None or normalized_key is None!")
            conn.close()
            return

        # Entrada de tabla

        I1 = "INSERT OR REPLACE INTO prompts (hash, prompt_text, clean_input, keywords, last_used) VALUES (?, ?, ?, ?, ?)"
        c.execute(I1, (hash_of_normalized_key, tag_keyword, clean_user_input, tag_keyword, now))
        # utils.log_debug("A:I1")

        # utils.log_debug(

        # f"B: hash={hash_of_normalized_key}, Prompt_text={tag_keyword}, clean_input={clean_user_input}, palabras clave={tag_keyword}, last_used={ahora}")


        I2 = "INSERT INTO responses (prompt_hash, response_text, created_at, rating, usage_count) VALUES (?, ?, ?, ?, 1)"
        c.execute(I2, (hash_of_normalized_key, response_text, now, utils.DEFAULT_RATING))
        # utils.log_debug("C:I2")

        # utils.log_debug(

        # f"D: Prompt_hash={hash_of_normalized_key}, respuesta_texto={response_text}, creado_at={ahora}, calificación={utils.DEFAULT_RATING}")


        # Limpieza si hay demasiados

        c.execute("SELECT count(*) FROM responses WHERE prompt_hash=?", (hash_of_normalized_key,))
        count = c.fetchone()[0]
        if count > utils.MAX_VARIANTS:
            excess = count - utils.MAX_VARIANTS
            # utils.log_debug(f"exceso: {exceso} = recuento:{recuento} - utils.MAX_VARIANTS:{utils.MAX_VARIANTS}")

            c.execute(
                '''DELETE FROM responses WHERE id IN (
                    SELECT id FROM responses WHERE prompt_hash=? 
                    ORDER BY rating ASC, usage_count ASC, created_at ASC 
                    LIMIT ?
                )''',
                (hash_of_normalized_key, excess)
            )

        conn.commit()
        conn.close()
        utils.log_debug(f"✅ Cache saved to db💾. normalized_key: {hash_of_normalized_key[:8]} …")

    except Exception as e:
        utils.log_debug(f"❌ DB ERROR in def cache_response(...): {e}")





def update_prompt_stats(prompt_hash):
    try:
        conn = sqlite3.connect(utils.DB_FILE, timeout=30)
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('BEGIN IMMEDIATE')
        c = conn.cursor()
        now = datetime.datetime.now().isoformat()
        c.execute("UPDATE prompts SET last_used = ? WHERE hash = ?", (now, prompt_hash))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'cache_core.py:165 Exception: {e} => pass')
