"""
Aura — Trino memory-catalog initialiser
scripts/py/func/db/init_trino_db.py

Fixes applied vs previous version
──────────────────────────────────
1. log_msg() flushes on every call.
   In subprocess/pipe mode Python fully buffers stdout — without flush=True
   only the first write may appear in the log file during a run.

2. wait_for_trino_connection() executes SELECT 1 instead of conn.close().
   trino.dbapi.connect() is lazy: it never opens a socket.  conn.close() on
   a lazy handle is a no-op.  The old function always returned True on the
   first iteration regardless of whether Trino was alive.

3. init_schema() verifies the schema exists with SHOW SCHEMAS after DDL.
   Trino's JVM startup has two phases:
     • Docker port 8083 opens  ~2 s after container start
     • Memory-catalog plugin fully loads  ~15–45 s after container start
   During the gap, CREATE SCHEMA can return without a Python exception while
   the schema is written to a coordinator state that the plugin then resets as
   it finishes initialising.  The schema silently vanishes.  The SHOW SCHEMAS
   check catches this and raises a clear RuntimeError so the caller retries.

4. self_heal_init() is the correct entry-point for Streamlit.
   When the Admin UI receives TrinoUserError(SCHEMA_NOT_FOUND), Trino is
   provably alive — you got a typed response from it.  Calling init_all()
   (which includes a 90-second wait loop) blocks Streamlit's execution thread
   for up to 90 seconds.  self_heal_init() skips the wait entirely.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

import time
from datetime import datetime

from scripts.py.func.db.trino_client import get_connection   # adjust if path differs


# Am Anfang von self_heal_init() öffnen:
conn = get_connection(schema='default')

# (deine init-Aufrufe bleiben unverändert)

# Am Ende von self_heal_init() speichern & schließen:
conn.commit()
conn.close()



# ── Logging ───────────────────────────────────────────────────────────────────

def log_msg(msg: str) -> None:
    """
    Always-flushed log line.
    flush=True is mandatory: in subprocess / pipe mode Python fully buffers
    stdout and messages accumulate in RAM until the buffer fills or the
    process exits — only the very first write may reach the log file otherwise.
    """
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [init_trino_db] {msg}", flush=True)


# ── Connection health-check ───────────────────────────────────────────────────

def _ping_trino() -> bool:
    """
    Return True only if Trino responds to a real query.

    Why not just conn.close()?
    trino.dbapi.connect() is intentionally lazy — it never opens a socket.
    conn.close() on a lazy handle is a no-op and proves nothing about
    whether the server is reachable or ready.  SELECT 1 forces the full
    HTTP round-trip and validates that the coordinator is processing queries.
    """
    try:
        # conn = get_connection(schema='aura')
        cur  = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchall()     # drives the HTTP round-trip; raises on any error
        cur.close()
        conn.close()
        return True
    except Exception:
        return False


def wait_for_trino_connection(timeout: int = 90) -> bool:
    """
    Block until Trino responds to SELECT 1 or *timeout* seconds elapse.
    Each failure is logged immediately (flush=True) so progress is visible.
    """
    log_msg("Waiting for Trino to accept connections...")
    for i in range(timeout):
        if _ping_trino():
            log_msg(f"Trino is ready (elapsed: {i + 1}s)")
            return True
        log_msg(f"  still waiting... ({i + 1}/{timeout}s)")
        time.sleep(1)
    log_msg("ERROR: Trino did not respond within the timeout window.")
    return False


# ── DDL helpers ───────────────────────────────────────────────────────────────

def init_schema(conn) -> None:
    cur  = conn.cursor()
    cur.execute("CREATE SCHEMA IF NOT EXISTS memory.aura")
    cur.fetchall()    # consume result; required to drive DDL to completion
    cur.close()
    conn.close()

    # ── Verify the schema is now actually visible ──────────────────────────
    # conn2 = get_connection(schema='aura')
    cur2  = conn.cursor()
    cur2.execute("SHOW SCHEMAS FROM memory")
    visible = {row[0].lower() for row in cur2.fetchall()}

    if 'aura' not in visible:
        raise RuntimeError(
            "CREATE SCHEMA ran without a Python exception but 'aura' is not "
            "listed in SHOW SCHEMAS FROM memory.  Trino's memory-catalog "
            "plugin is still initialising its metadata store.  "
            "Wait a few seconds and call init_schema() again."
        )

    log_msg("Schema memory.aura: OK")


def init_features_table(conn) -> None:
    # conn = get_connection(schema='aura')
    cur  = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memory.aura.features (
            interface  VARCHAR,
            feature    VARCHAR,
            state      VARCHAR
        )
    """)
    cur.fetchall()
    cur.close()
    conn.close()
    log_msg("Table memory.aura.features: OK")


def init_translation_state_table(conn) -> None:
    # conn = get_connection(schema='aura')
    cur  = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memory.aura.translation_state (
            interface  VARCHAR,
            state      VARCHAR
        )
    """)
    cur.fetchall()
    cur.close()
    conn.close()
    log_msg("Table memory.aura.translation_state: OK")


# ── Public entry-points ───────────────────────────────────────────────────────

def self_heal_init() -> None:
    """
    Streamlit self-heal entry-point.  Call this — NOT init_all() — from the
    Admin UI when it catches TrinoUserError(SCHEMA_NOT_FOUND / TABLE_NOT_FOUND).

    Rationale for skipping wait_for_trino_connection():
      Receiving a TrinoUserError proves Trino is alive and responding.
      wait_for_trino_connection() would block Streamlit's execution thread for
      up to 90 seconds while the browser shows a frozen page.  The schema and
      table DDL calls below will raise immediately with a connection error if
      Trino truly goes away between the original failure and this call —
      that exception propagates to the Streamlit error handler as expected.

    Retry logic for the schema-visibility race:
      init_schema() raises RuntimeError if SHOW SCHEMAS doesn't list 'aura'
      after CREATE SCHEMA.  We retry up to 5 times (5 s total) to handle the
      Trino JVM startup window before giving up.
    """
    log_msg("self_heal_init: starting targeted recovery...")

    # Retry the schema step — handles the memory-plugin startup race
    schema_created = False
    for attempt in range(1, 6):
        try:
            init_schema(conn)
            schema_created = True
            break
        except RuntimeError as e:
            log_msg(f"  schema attempt {attempt}/5 failed: {e}")
            time.sleep(1)

    if not schema_created:
        raise RuntimeError(
            "self_heal_init: could not verify schema 'aura' exists after "
            "5 attempts.  Trino may still be loading the memory-catalog plugin."
        )

    init_features_table(conn)
    init_translation_state_table(conn)
    log_msg("self_heal_init: complete")


def init_all() -> None:
    """
    Full boot-time initialisation.  Called from aura_engine.py on startup.
    Do NOT call this from Streamlit — use self_heal_init() instead.
    """
    log_msg("Starting Trino DB initialization...")

    if not wait_for_trino_connection():
        log_msg("FATAL: Trino did not become ready within the timeout. Aborting.")
        return

    conn = None
    for attempt in range(1, 6):
        try:
            # Open the single shared connection to the safe 'default' schema
            conn = get_connection(schema='default')
            init_schema(conn)
            break
        except Exception as e:
            log_msg(f"  schema attempt {attempt}/5: {e}")
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass
            time.sleep(2)
    else:
        log_msg("FATAL: Schema could not be verified after 5 attempts.")
        return

    # Execute the table creation on the exact same active connection
    try:
        time.sleep(2)  # Give Trino catalog a brief moment to stabilize
        init_features_table(conn)
        init_translation_state_table(conn)
        log_msg("All Trino DB init steps complete.")
    except Exception as e:
        log_msg(f"FATAL: Database initialization failed during table creation: {e}")
        raise
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    init_all()