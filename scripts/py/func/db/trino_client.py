# scripts/py/func/db/trino_client.py
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[4]))
import trino
from datetime import datetime, timezone
from scripts.py.func.determine_current_user import determine_current_user

TRINO_HOST = 'localhost'
TRINO_PORT = 8083
TRINO_CATALOG = 'memory'
TRINO_SCHEMA = 'aura'

def get_connection():
    current_user, _ = determine_current_user()
    return trino.dbapi.connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        user=current_user,
        catalog=TRINO_CATALOG,
        schema=TRINO_SCHEMA,
    )

def get_translation_state(interface='terminal', target_lang='en'):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT state FROM memory.aura.translation_state
        WHERE interface = '{interface}'
        AND target_lang = '{target_lang}'
    """)
    row = cur.fetchone()
    return row[0] if row else 'off'

def get_all_states():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM memory.aura.translation_state")
    return cur.fetchall()

def set_translation_state(interface='terminal', target_lang='en', state='off'):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    # memory connector has no UPDATE/DELETE -> rebuild table
    all_states = get_all_states()
    # update or add entry
    updated = False
    new_states = []
    for row in all_states:
        if row[0] == interface and row[1] == target_lang:
            new_states.append((interface, target_lang, state, now))
            updated = True
        else:
            new_states.append(tuple(row))
    if not updated:
        new_states.append((interface, target_lang, state, now))

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS memory.aura.translation_state")
    cur.fetchone()
    cur.execute("""
        CREATE TABLE memory.aura.translation_state (
            interface   VARCHAR,
            target_lang VARCHAR,
            state       VARCHAR,
            updated_at  VARCHAR
        )
    """)
    cur.fetchone()
    for row in new_states:
        cur.execute(f"""
            INSERT INTO memory.aura.translation_state VALUES
            ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}')
        """)
        cur.fetchone()
    return state

if __name__ == '__main__':
    print('terminal/en:', get_translation_state('terminal', 'en'))
    print('web/en:     ', get_translation_state('web', 'en'))
    set_translation_state('terminal', 'en', 'on')
    print('after set terminal/en on:', get_translation_state('terminal', 'en'))
    print('web/en still off:        ', get_translation_state('web', 'en'))
