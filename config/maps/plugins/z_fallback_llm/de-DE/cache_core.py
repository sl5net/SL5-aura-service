#import re
#import hashlib

import sqlite3
import hashlib
import random
import datetime

from .utils import *
from .normalizer import *



from pathlib import Path
#
# PLUGIN_DIR = Path(__file__).parent
# MEMORY_FILE = PLUGIN_DIR / "conversation_history.json"
# BRIDGE_FILE = Path("/tmp/aura_clipboard.txt")
# DB_FILE = PLUGIN_DIR / "llm_cache.db"


def get_cached_response():
    global SESSION_CACHE_HITS
    global GLOBAL_NORMALIZED_KEY
    init_db()

    normalized_prompt_key =     GLOBAL_NORMALIZED_KEY
    prompt_hash = hashlib.sha256(normalized_prompt_key.encode('utf-8')).hexdigest()


    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # 1. Variablen vorbereiten
        sql_query = "SELECT last_used FROM prompts WHERE hash=?"
        sql_params = (prompt_hash,)

        # normalized_prompt = normalize_for_hashing(hash_input_str)
        # log_debug(f"🔑{normalized_prompt} -> Hash: {prompt_hash}")


        # 2. Loggen (Was gleich passiert)
        # log_debug(f"🔍Select: {sql_query} | Params: {sql_params}")

        # 3. Ausführen (mit den Variablen)
        c.execute(sql_query, sql_params)

        # c.execute("SELECT last_used FROM prompts WHERE hash=?", (prompt_hash,))
        row = c.fetchone()
        if not row:
            conn.close()
            return None, False

        last_used_str = row[0]
        try:
            last_used = datetime.datetime.fromisoformat(last_used_str)
            age = datetime.datetime.now() - last_used
            if age.days > CACHE_TTL_DAYS:
                conn.close()
                return None, True
        except Exception: pass

        c.execute("SELECT id, response_text FROM responses WHERE prompt_hash=?", (prompt_hash,))
        rows = c.fetchall()
        if rows:
            # --- FEATURE DEAKTIVIERT: Active Variation ---
            # deaktiviert, want 100% Cache Hits.
            # Der Sinn dieses Features ("Active Variation") ist es, den "Papagei-Effekt" zu verhindern und das System menschlicher wirken zu lassen.
            # variant_count = len(rows)
            # if variant_count < 3 and random.random() < 0.2:
            #     # ACHTUNG: Hier ist eine 20% Chance auf ABSICHTLICHEN Cache-Miss!
            #     log_debug(f"♻️ Active Variation: {variant_count} Varianten. Generiere neu...")
            #     conn.close()
            #     return None, True # <--- Zwingt das System, neu zu generieren

            chosen_row = random.choice(rows)
            c.execute("UPDATE responses SET usage_count = usage_count + 1 WHERE id = ?", (chosen_row[0],))
            conn.commit()
            conn.close()
            SESSION_CACHE_HITS += 1
            # log_debug(f"✅ {SESSION_CACHE_HITS} Cache HITs | CacheHITs/Nr : {int((SESSION_CACHE_HITS+0.01)/SESSION_COUNT*10)/10}📈"
            #         f"Zeit gespart: ~{SESSION_CACHE_HITS * int(SESSION_SEC_SUM / (SESSION_COUNT - SESSION_CACHE_HITS) * 10) / 10}s")


            play_cache_hit_sound()
            update_prompt_stats(prompt_hash)
            return chosen_row[1], False
        conn.close()
        return None, False
    except Exception: return None, False

def update_prompt_stats(prompt_hash):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        now = datetime.datetime.now().isoformat()
        c.execute("UPDATE prompts SET last_used = ? WHERE hash = ?", (now, prompt_hash))
        conn.commit()
        conn.close()
    except Exception: pass
