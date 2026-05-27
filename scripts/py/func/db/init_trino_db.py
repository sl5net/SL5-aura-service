# scripts/py/func/db/init_trino_db.py
"""
Initializes Trino in-memory database with required schemas, tables and default values.
Called once at Aura engine startup.
"""
from pathlib import Path
import sys
import time
import subprocess
import datetime

sys.path.insert(0, str(Path(__file__).parents[4]))

from scripts.py.func.db.trino_client import get_connection

INTERFACES = ['speech', 'terminal', 'web']
FEATURES = ['translation']


def start_trino_if_needed():
    print("[init_trino_db] Checking Trino Docker container...")
    result = subprocess.run(
        ['docker', 'ps', '--filter', 'name=trino', '--format', '{{.Names}}'],
        capture_output=True, text=True
    )
    if 'trino' in result.stdout:
        print("[init_trino_db] Trino already running. OK")
        return True

    print("[init_trino_db] Trino not running, starting...")
    start = subprocess.run(
        ['docker', 'start', 'trino'],
        capture_output=True, text=True
    )
    if start.returncode != 0:
        print(f"[init_trino_db] ERROR starting Trino: {start.stderr}")
        return False

    print("[init_trino_db] Waiting for Trino to be ready...")
    for i in range(90):
        logs = subprocess.run(
            ['docker', 'logs', 'trino', '--tail', '500'],
            capture_output=True, text=True
        )
        if 'SERVER STARTED' in logs.stdout or 'SERVER STARTED' in logs.stderr:
            print(f"[init_trino_db] Trino ready after {i+1}s. OK")
            return True
        time.sleep(1)

    print("[init_trino_db] ERROR: Trino did not start in time.")
    return False


def init_schema():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE SCHEMA IF NOT EXISTS memory.aura")
    cur.fetchone()
    print("[init_trino_db] Schema memory.aura: OK")


def init_features_table():
    # now = __import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

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
    for interface in INTERFACES:
        for feature in FEATURES:
            cur.execute(f"""
                INSERT INTO memory.aura.features VALUES
                ('{interface}', '{feature}', 'off', '{now}')
            """)
            cur.fetchone()
    print(f"[init_trino_db] Table features OK: interfaces={INTERFACES} features={FEATURES}")


def init_translation_state_table():
    # now = __import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
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
    # No default rows — no entry means no translation active
    print("[init_trino_db] Table translation_state OK (empty by default)")


def init_all():
    print("[init_trino_db] Starting Trino DB initialization...")
    try:
        if not start_trino_if_needed():
            print("[init_trino_db] WARNING: Trino not available, skipping DB init.")
            return
        init_schema()
        init_features_table()
        init_translation_state_table()
        print("[init_trino_db] Done. ✅")
    except Exception as e:
        print(f"[init_trino_db] ERROR: {e}")
        raise


if __name__ == '__main__':
    init_all()
