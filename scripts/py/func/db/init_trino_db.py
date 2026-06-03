"""
scripts/py/func/db/init_trino_db.py
Initializes Trino in-memory database with required schemas, tables and default values.
"""
import os
from pathlib import Path
import sys
import time
import subprocess
import datetime
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass


sys.path.insert(0, str(Path(__file__).parents[4]))
from scripts.py.func.db.trino_client import (open_trino_connection
, TRINO_CATALOG, TRINO_SCHEMA)

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f'{PROJECT_ROOT}/log/{__name__}.log', mode='a', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


INTERFACES = ['speech', 'terminal', 'web']
FEATURES = ['translation']



async def schema_exists(catalog: str, schema: str) -> bool:
    """
    Confirm schema existence using SHOW SCHEMAS.
    scripts/py/func/db/init_trino_db.py:41
    """
    conn = await open_trino_connection()
    try:
        cur = await conn.cursor()
        # Execute the robust SHOW SCHEMAS query on the catalog (e.g. 'memory')
        await cur.execute(f"SHOW SCHEMAS FROM {catalog}")
        rows = await cur.fetchall()
        # Extract and lowercase all existing schema names in the catalog
        schemas = {row[0].lower() for row in rows}
        return schema.lower() in schemas
    finally:
        await conn.close()


# scripts/py/func/db/init_trino_db.py:51
def start_trino_if_needed() -> str | None:
    """
    Ensures Trino Docker container is running.
    Returns None on success, or an error message string on failure.
    """
    result = subprocess.run(
        ['docker', 'ps', '--filter', 'name=trino', '--format', '{{.Names}}'],
        capture_output=True, text=True
    )
    if 'trino' in result.stdout:
        logger.info("Trino container already running.")
        return None                                     # ← success

    logger.info("Trino not running, attempting docker start...")
    start = subprocess.run(
        ['docker', 'start', 'trino'],
        capture_output=True, text=True
    )
    if start.returncode != 0:
        return f"docker start exited {start.returncode}: {start.stderr.strip()}"  # ← failure

    logger.info("Trino container started.")
    return None                                         # ← success

async def wait_for_trino_connection(timeout=90):
    """Polls once per second until Trino JVM accepts connections."""
    import asyncio
    logger.info("Waiting for Trino JVM to accept connections...")
    for i in range(timeout):
        try:
            conn = await open_trino_connection()
            await conn.close()
            logger.info("Trino connection successful after %ds.", i + 1)
            return True
        except Exception:
            await asyncio.sleep(1)
    logger.error("Could not connect to Trino within %ds timeout.", timeout)
    return False

async def init_schema(conn, catalog: str = "memory", schema: str = "aura") -> tuple[bool, str]:
    """
    Ensure schema exists, return (success, message).
    """
    if not conn:
        conn = await open_trino_connection()
    try:
        cur = await conn.cursor()

        try:
            await cur.execute(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
            await conn.commit()
        except Exception as e:
            msg = f"Failed to execute CREATE SCHEMA: {e!s}"
            logger.error(msg)
            return False, msg

        try:
            exists = await schema_exists(catalog, schema)
        except Exception as e:
            msg = f"CREATE executed but verification failed: {e!s}"
            logger.error(msg)
            return False, msg

        if exists:                                          # ← now properly inside try
            msg = f"Schema {catalog}.{schema}: OK (verified)"
            logger.info(msg)
            return True, msg

        msg = f"Schema {catalog}.{schema}: NOT FOUND after CREATE"
        logger.error(msg)
        return False, msg

    finally:
        # await conn.close()                                        # ← always runs, even on early return
        logger.info("Trino JVM connection not closed. (Marker: 20260603_1652)")

async def init_features_table(conn=None):
    if not conn:
        conn = await open_trino_connection()
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    try:
        cur = await conn.cursor()

        await cur.execute("DROP TABLE IF EXISTS memory.aura.features")
        await cur.fetchone()        # consume result (Trino requirement)

        await cur.execute("""
            CREATE TABLE memory.aura.features (
                interface  VARCHAR,
                feature    VARCHAR,
                state      VARCHAR,
                updated_at VARCHAR
            )
        """)
        await cur.fetchone()        # consume result

        for interface in INTERFACES:
            for feature in FEATURES:
                await cur.execute(
                    "INSERT INTO memory.aura.features VALUES (?, ?, ?, ?)",
                    (interface, feature, 'off', now)
                )
                await cur.fetchone()    # consume result

        logger.info("Table features OK: interfaces=%s features=%s", INTERFACES, FEATURES)

        await conn.commit()

    finally:
        # await conn.close()
        logger.info('Trino JVM connection not closed.')

async def init_translation_state_table(conn=None):
    if not conn:
        conn = await open_trino_connection()
    try:
        cur = await conn.cursor()
        await cur.execute("DROP TABLE IF EXISTS memory.aura.translation_state")
        await cur.fetchone()
        await cur.execute("""
            CREATE TABLE memory.aura.translation_state (
                interface   VARCHAR,
                target_lang VARCHAR,
                updated_at  VARCHAR
            )
        """)
        await cur.fetchone()
        print("Table translation_state OK (empty by default)")
    finally:
        await conn.close()
# scripts/py/func/db/init_trino_db.py:181
def init_all_sync() -> None:
    """Synchronous entry point for Streamlit / non-async callers."""
    import asyncio
    time.sleep(1)
    for _ in range(60):
        try:
            asyncio.run(init_all())
            break
        except Exception:
            time.sleep(0.5)

async def init_all():
    logger.info("Starting Trino DB initialization...")
    try:
        err = start_trino_if_needed()
        if err:
            logger.warning("Skipping DB init — Docker start failed: %s", err)
            return

        # Here we actively wait until the port actually responds
        if not await wait_for_trino_connection(90):
            print("WARNING: Trino not reachable, skipping DB init.")
            logger.warning("WARNING: Trino not reachable, skipping DB init.")
            return

        # ok, msg = await init_schema(catalog=TRINO_CATALOG, schema=TRINO_SCHEMA)
        # A connection for everyone:
        conn = await open_trino_connection(schema='default')
        try:
            ok, msg = await init_schema(conn, TRINO_CATALOG, TRINO_SCHEMA)
            if not ok:
                raise RuntimeError(msg)
                # return
            await init_features_table(conn)
            await init_translation_state_table(conn)
        finally:
            # await conn.close()
            logger.info('Trino DB initialization complete.')


        if not ok:
            logger.error("Schema init failed, aborting: %s", msg)
            return

        await init_features_table()
        await init_translation_state_table()

        logger.info("DB init complete.")

    except Exception as e:
        logger.error("init_all failed: %s", e, exc_info=True)
        raise
    from scripts.py.func.db.aura_state import ensure_fuzzy_map_in_sync
    ensure_fuzzy_map_in_sync()


if __name__ == '__main__':
    # import trino
    # ensure_package('asyncio')
    # Python 3.4+ ships with the asyncio module as part of the standard library, so you normally access it with import asyncio without installing anything.
    # asyncio.run(init_all())
    init_all_sync()
