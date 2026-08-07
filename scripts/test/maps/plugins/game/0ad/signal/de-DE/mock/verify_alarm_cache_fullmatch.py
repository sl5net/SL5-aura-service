# PYTHONPATH=. .venv/bin/python scripts/test/maps/plugins/game/0ad/signal/de-DE/mock/verify_alarm_cache_fullmatch.py
import sqlite3
import logging
from pathlib import Path

import scripts.py.func.get_active_window_title as gawt
import scripts.py.func.process_text_in_background as ptib
gawt.get_active_window_title_safe = lambda: "0 A.D."
ptib.get_active_window_title_safe = lambda: "0 A.D."

from scripts.py.func.process_text_in_background import process_text_in_background

db_path = Path("data/_aura_result_cache.db")

print("Step 1: Clearing existing cache entries for 'alarm'...")
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    conn.execute("DELETE FROM aura_result_cache WHERE rule_output LIKE '%alarm%' OR final_result LIKE '%ö%'")
    conn.commit()
    conn.close()

print("\nStep 2: Processing text 'alarm'...")
logger = logging.getLogger("test_alarm")
output_dir = Path("tmp/debug_output")
output_dir.mkdir(parents=True, exist_ok=True)

res = process_text_in_background(
    logger=logger,
    LT_LANGUAGE="de-DE",
    raw_text="alarm",
    output_dir=output_dir,
    recording_time=0.0,
    active_lt_url=""
)
print(f"Execution result: {res}")

print("\nStep 3: Querying newly generated SQLite cache row...")
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM aura_result_cache WHERE rule_output LIKE '%alarm%' OR final_result LIKE '%ö%'").fetchall()
    for row in rows:
        print(dict(row))
    conn.close()

