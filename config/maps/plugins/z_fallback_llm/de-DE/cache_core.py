# cache_core.py
#import re
#import hashlib

import sqlite3
import hashlib
import random
import datetime



from . import utils
from .normalizer import *



from pathlib import Path
#
# utils.PLUGIN_DIR = Path(__file__).parent
# utils.MEMORY_FILE = utils.PLUGIN_DIR / "conversation_history.json"
# utils.BRIDGE_FILE = Path("/tmp/aura_clipboard.txt")
# utils.DB_FILE = utils.PLUGIN_DIR / "llm_cache.db"

def prompt_key_to_hash(normalized_prompt_key: str):
    prompt_hash = hashlib.sha256(normalized_prompt_key.encode('utf-8')).hexdigest()
    return prompt_hash


# def get_cached_response():
def get_cached_response(prompt_key_to_hash1: str):

    utils.init_db()


    # normalized_prompt_key = prompt_key_to_hash # e.g. "STD|regeln

    # prompt_hash = hashlib.sha256(normalized_prompt_key.encode('utf-8')).hexdigest()
    prompt_hash = prompt_key_to_hash(normalized_prompt_key=prompt_key_to_hash1)
    # utils.log_debug(f"222222 prompt_hash: {prompt_hash}")
    # sys.exit()

    try:
        conn = sqlite3.connect(utils.DB_FILE)
        c = conn.cursor()

        # 1. Variablen vorbereiten
        sql_query = "SELECT last_used FROM prompts WHERE hash=?"
        sql_params = (prompt_hash,)

        # normalized_prompt = normalize_for_hashing(hash_input_str)
        # utils.log_debug(f"normalized_prompt_key:🔑{prompt_key_to_hash1} -> Hash: {prompt_hash}")


        # 2. Loggen (Was gleich passiert)
        # utils.log_debug(f"🔍Select: {sql_query} | Params: {sql_params}")

        # utils.log_debug('🎈')

        # 3. Ausführen (mit den Variablen)
        c.execute(sql_query, sql_params)

        # c.execute("SELECT last_used FROM prompts WHERE hash=?", (prompt_hash,))

        # utils.log_debug('🎈')
        row = c.fetchone()
        # utils.log_debug('🎈')
        if not row:
            conn.close()
            # utils.log_debug(f"{sql_query,sql_params}")
            # utils.log_debug(f"333333 return None, False")
            return None, False

        last_used_str = row[0]
        # utils.log_debug('🎈')
        try:
            last_used = datetime.datetime.fromisoformat(last_used_str)
            # utils.log_debug('🎈')
            age = datetime.datetime.now() - last_used
            # utils.log_debug('🎈')
            if age.days > utils.CACHE_TTL_DAYS:
                conn.close()
                utils.log_debug(f"return None, False")
                return None, True
        except Exception as e:
            utils.log_debug(f"Exception {e}")
            pass

        c.execute("SELECT id, response_text FROM responses WHERE prompt_hash=?", (prompt_hash,))
        # utils.log_debug('🎈')
        rows = c.fetchall()
        if rows:
            # --- FEATURE DEAKTIVIERT: Active Variation ---
            # deaktiviert, want 100% Cache Hits.
            # Der Sinn dieses Features ("Active Variation") ist es, den "Papagei-Effekt" zu verhindern und das System menschlicher wirken zu lassen.
            # variant_count = len(rows)
            # if variant_count < 3 and random.random() < 0.2:
            #     # ACHTUNG: Hier ist eine 20% Chance auf ABSICHTLICHEN Cache-Miss!
            #     utils.log_debug(f"♻️ Active Variation: {variant_count} Varianten. Generiere neu...")
            #     conn.close()
            #     return None, True # <--- Zwingt das System, neu zu generieren

            chosen_row = random.choice(rows)
            # utils.log_debug(f'🎈 SESSION_COUNT={SESSION_COUNT}')
            c.execute("UPDATE responses SET usage_count = usage_count + 1 WHERE id = ?", (chosen_row[0],))
            conn.commit()
            conn.close()
            utils.SESSION_CACHE_HITS += 1

            lll = (utils.SESSION_CACHE_HITS / utils.SESSION_COUNT) if utils.SESSION_COUNT > 0 else 0

            SESSION_SEC_Average = utils.SESSION_SEC_SUM / utils.SESSION_COUNT if utils.SESSION_COUNT > 0 else 0

            cache_hit_rate = lll if utils.SESSION_COUNT > 0 else 0
            utils.SUM_PER_CACHE_str = f"{cache_hit_rate:.1f}"
            utils.log_debug(f"✅ {utils.SESSION_CACHE_HITS} Cache HITs | CacheHITs/Nr : {utils.SUM_PER_CACHE_str}📈"
                    f"Zeit gespart: ~{SESSION_SEC_Average * utils.SESSION_CACHE_HITS:.1f}s")


            utils.play_cache_hit_sound()
            update_prompt_stats(prompt_hash)
            return chosen_row[1], False
        conn.close()
        utils.log_debug(f"return None, False")
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
    #     f"1: tag_keyword:{tag_keyword}, "
    #     f"response_text:{str(response_text)[:15]}..., "
    #     f"clean_user_input:{clean_user_input}, "
    #     f"normalized_key:{hash_of_normalized_key}"
    # )
    if not tag_keyword:
        utils.log_debug("⚠️ WARNUNG: cache_response wurde OHNE tag_keyword aufgerufen (None/Leer)!")

    utils.init_db()  # Ensure DB table exists

    now = datetime.datetime.now().isoformat()
    try:
        conn = sqlite3.connect(utils.DB_FILE)
        c = conn.cursor()

        # Validate that hash_input_str and prompt_key_to_hash are not None
        if tag_keyword is None or hash_of_normalized_key is None:
            utils.log_debug("❌ ERROR: tag_keyword is None or normalized_key is None!")
            conn.close()
            return

        # Tabelleneintrag
        I1 = "INSERT OR REPLACE INTO prompts (hash, prompt_text, clean_input, keywords, last_used) VALUES (?, ?, ?, ?, ?)"
        c.execute(I1, (hash_of_normalized_key, tag_keyword, clean_user_input, tag_keyword, now))
        # utils.log_debug("A: I1")
        # utils.log_debug(
        #     f"B: hash={hash_of_normalized_key}, prompt_text={tag_keyword}, clean_input={clean_user_input}, keywords={tag_keyword}, last_used={now}")

        I2 = "INSERT INTO responses (prompt_hash, response_text, created_at, rating, usage_count) VALUES (?, ?, ?, ?, 1)"
        c.execute(I2, (hash_of_normalized_key, response_text, now, utils.DEFAULT_RATING))
        # utils.log_debug("C: I2")
        # utils.log_debug(
        #     f"D: prompt_hash={hash_of_normalized_key}, response_text={response_text}, created_at={now}, rating={utils.DEFAULT_RATING}")

        # Cleanup falls zu viele
        c.execute("SELECT count(*) FROM responses WHERE prompt_hash=?", (hash_of_normalized_key,))
        count = c.fetchone()[0]
        if count > utils.MAX_VARIANTS:
            excess = count - utils.MAX_VARIANTS
            # utils.log_debug(f"excess: {excess} = count:{count} - utils.MAX_VARIANTS:{utils.MAX_VARIANTS}")
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
        utils.log_debug(f"✅ Cache saved to db💾. normalized_key: {hash_of_normalized_key[:8]} ...")

    except Exception as e:
        utils.log_debug(f"❌ DB ERROR in def cache_response(...): {e}")





def update_prompt_stats(prompt_hash):
    try:
        conn = sqlite3.connect(utils.DB_FILE)
        c = conn.cursor()
        now = datetime.datetime.now().isoformat()
        c.execute("UPDATE prompts SET last_used = ? WHERE hash = ?", (now, prompt_hash))
        conn.commit()
        conn.close()
    except Exception: pass