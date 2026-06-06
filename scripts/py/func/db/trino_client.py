# scripts/py/func/db/trino_client.py
from pathlib import Path
import sys
import logging
sys.path.insert(0, str(Path(__file__).parents[4]))
from datetime import datetime, timezone
from scripts.py.func.determine_current_user import determine_current_user
from scripts.py.func.ensure_package import ensure_package

TRINO_HOST = 'localhost'
TRINO_PORT = 8083
TRINO_CATALOG = 'memory'
TRINO_SCHEMA = 'aura'

async def open_trino_connection(schema=TRINO_SCHEMA):
    aiotrino = ensure_package("aiotrino")
    current_user, _ = determine_current_user()
    return aiotrino.dbapi.connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        user=current_user,
        catalog=TRINO_CATALOG,
        schema=schema,
    )

# scripts/py/func/db/trino_client.py:25
def get_connection(schema=TRINO_SCHEMA):
    """For synchronous runtime callers (trino_client helpers, Streamlit)."""

    try:
        import trino
    except ModuleNotFoundError:
        from scripts.py.func.try_auto_install_package import try_auto_install_package
        try_auto_install_package('trino',logger=logging)
        import trino

    current_user, _ = determine_current_user()
    return trino.dbapi.connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        user=current_user,
        catalog=TRINO_CATALOG,
        schema=schema,
    )


# ─── FEATURES (on/off per interface) ────────────────────────────────────────

def get_all_feature_states():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM memory.aura.features")
    return cur.fetchall()


def get_feature_state(interface='speech', feature='translation'):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
    SELECT f.state 
    FROM memory.aura.features f
    INNER JOIN memory.aura.translation_state t 
      ON f.interface = t.interface
    WHERE f.interface = '{interface}'
      AND f.feature = '{feature}'
    """)
    row = cur.fetchone()
    return row[0] if row else 'off'


def set_feature_state(interface='speech', feature='translation', state='off'):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    all_rows = get_all_feature_states()
    updated = False
    new_rows = []
    for row in all_rows:
        if row[0] == interface and row[1] == feature:
            new_rows.append((interface, feature, state, now))
            updated = True
        else:
            new_rows.append(tuple(row))
    if not updated:
        new_rows.append((interface, feature, state, now))

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS memory.aura.features")
    cur.fetchone()
    cur.execute("""
        CREATE TABLE memory.aura.features (
            interface  VARCHAR,
            feature    VARCHAR,
            state      VARCHAR,
            updated_at VARCHAR
        )
    """)
    cur.fetchone()
    for row in new_rows:
        cur.execute(f"""
            INSERT INTO memory.aura.features VALUES
            ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}')
        """)
        cur.fetchone()
    return state


# ─── TRANSLATION STATE (target language per interface) ───────────────────────

def get_all_translation_states():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM memory.aura.translation_state")
    return cur.fetchall()


def get_target_lang(interface='speech'):
    """Returns the target language for this interface, or None if not set."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT target_lang FROM memory.aura.translation_state
        WHERE interface = '{interface}'
    """)
    row = cur.fetchone()
    return row[0] if row else None


def set_target_lang(interface='speech', target_lang='en'):
    """Sets the target language for this interface."""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    all_rows = get_all_translation_states()
    updated = False
    new_rows = []
    for row in all_rows:
        if row[0] == interface:
            new_rows.append((interface, target_lang, now))
            updated = True
        else:
            new_rows.append(tuple(row))
    if not updated:
        new_rows.append((interface, target_lang, now))

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS memory.aura.translation_state")
    cur.fetchone()
    cur.execute("""
        CREATE TABLE memory.aura.translation_state (
            interface   VARCHAR,
            target_lang VARCHAR,
            updated_at  VARCHAR
        )
    """)
    cur.fetchone()
    for row in new_rows:
        cur.execute(f"""
            INSERT INTO memory.aura.translation_state VALUES
            ('{row[0]}', '{row[1]}', '{row[2]}')
        """)
        cur.fetchone()
    return target_lang


if __name__ == '__main__':
    print("=== features ===")
    print("speech/translation:", get_feature_state('speech', 'translation'))
    set_feature_state('speech', 'translation', 'on')
    print("after set on:", get_feature_state('speech', 'translation'))
    print("web still off:", get_feature_state('web', 'translation'))

    print("=== translation_state ===")
    print("speech target_lang:", get_target_lang('speech'))
    set_target_lang('speech', 'en')
    print("after set en:", get_target_lang('speech'))
    print("web target_lang:", get_target_lang('web'))
