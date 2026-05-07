# aura_cache.py
import sqlite3
import hashlib
import os
import platform
from pathlib import Path
from datetime import datetime

from scripts.py.func.config.dynamic_settings import DynamicSettings
settings = DynamicSettings()



README = '''
python3 -c "import sqlite3; conn = sqlite3.connect('/tmp/sl5_aura/aura_result_cache.db'); print('count:', conn.execute('SELECT count(*) FROM aura_result_cache').fetchone()[0]); conn.close()"

python3 -c "import sqlite3; conn = sqlite3.connect('/tmp/sl5_aura/aura_result_cache.db'); rows = conn.execute('SELECT rule_output, validity_type, validity_value FROM aura_result_cache').fetchall(); [print(r) for r in rows]; conn.close()"


By using AI Assist, you agree to Stack Overflow’s Terms of Service and Privacy Policy. Powered with the help of OpenAI. For help or feedback, contact us and reference this conversation ID: a207d660-c478-45d0-9dd5-e3a571675c73

'''

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

DB_DIR = PROJECT_ROOT / settings.path_unencrypted_cash

DB_PATH = DB_DIR / "_aura_result_cache.db"


_DB_CONNECTION = None

def get_db_connection():
    """Gibt eine persistente SQLite-Verbindung zurück."""
    global _DB_CONNECTION
    if _DB_CONNECTION is None:
        DB_DIR.mkdir(parents=True, exist_ok=True)
        _DB_CONNECTION = sqlite3.connect(str(DB_PATH), timeout=10, check_same_thread=False)
        _DB_CONNECTION.row_factory = sqlite3.Row
    return _DB_CONNECTION

def init_db():
    """Initialisiert das Schema, falls die Datei neu ist."""
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS aura_result_cache (
                cache_id TEXT PRIMARY KEY,
                rule_output TEXT NOT NULL,
                final_result TEXT NOT NULL,
                lang_code TEXT NOT NULL,
                map_path TEXT NOT NULL,
                validity_type INTEGER DEFAULT 0,
                validity_value TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_used DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_map_cleanup ON aura_result_cache (map_path, validity_type)")
        conn.commit()

def generate_cache_id(rule_output, lang_code, _active_window_title=''):
    """Erzeugt einen eindeutigen MD5-Key für Text, Sprache und Window-Titel."""
    raw_key = f"{lang_code}:{_active_window_title}:{rule_output}"
    return hashlib.md5(raw_key.encode('utf-8')).hexdigest()

def get_cached_result(rule_output, lang_code, map_path, rule_attrs, _active_window_title):
    """
    Prüft, ob ein gültiges Ergebnis im Cache liegt.
    Gibt den final_text zurück oder None.
    """
    # Variante 2: Explizites Cache-Verbot
    if rule_attrs.get('cache') is False:
        return None

    cache_id = generate_cache_id(rule_output, lang_code, _active_window_title)

    # Bestimme Gültigkeit (Variante 3 vs Default)
    manual_ts = rule_attrs.get('timestamp')
    if manual_ts:
        v_type = 1
        v_val = str(manual_ts)
    else:
        v_type = 0
        # Nutze mtime als Default (Variante 1)
        v_val = str(os.path.getmtime(map_path))

    with get_db_connection() as conn:
        cursor = conn.execute("""
            SELECT final_result FROM aura_result_cache
            WHERE cache_id = ?
              AND validity_type = ?
              AND validity_value = ?
        """, (cache_id, v_type, v_val))
        row = cursor.fetchone()

        if row:
            # Update last_used (für den Janitor)
            conn.execute("UPDATE aura_result_cache SET last_used = ? WHERE cache_id = ?",
                         (datetime.now(), cache_id))
            return row['final_result']

    return None

def set_cached_result(rule_output, final_result, lang_code, map_path, rule_attrs, _active_window_title):
    """Speichert ein neues LT-Ergebnis im Cache."""
    if rule_attrs.get('cache') is False:
        return

    cache_id = generate_cache_id(rule_output, lang_code, _active_window_title)

    manual_ts = rule_attrs.get('timestamp')
    v_type = 1 if manual_ts else 0
    v_val = str(manual_ts) if manual_ts else str(os.path.getmtime(map_path))

    with get_db_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO aura_result_cache
            (cache_id, rule_output, final_result, lang_code, map_path, validity_type, validity_value, last_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (cache_id, rule_output, final_result, lang_code, map_path, v_type, v_val, datetime.now()))
        conn.commit()


def cleanup_cache_on_reload(map_path, new_mtime):
    """Löscht veraltete mtime-basierte Einträge beim Neuladen einer Map."""
    with get_db_connection() as conn:
        conn.execute("""
            DELETE FROM aura_result_cache
            WHERE map_path = ? AND validity_type = 0 AND validity_value < ?
        """, (str(map_path), str(new_mtime)))
        conn.commit()

# Initialisierung beim ersten Import
init_db()
