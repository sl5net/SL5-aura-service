import sys
from pathlib import Path


from scripts.py.func.get_project_root import get_aura_project_root

SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()

import logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("trace_pipeline")

import scripts.py.func.get_active_window_title as gawt
import scripts.py.func.process_text_in_background as ptib

gawt.get_active_window_title_safe = lambda: "0 A.D."
ptib.get_active_window_title_safe = lambda: "0 A.D."

from scripts.py.func import global_state
global_state.LOGGING_ENABLED = True
global_state.DEV_MODE_all_processing = 1

from scripts.py.func.process_text_in_background import process_text_in_background

print("--- STARTING STEP-BY-STEP PIPELINE TRACE FOR 'alarm' ---")
output_dir = SL5NET_AURA_PROJECT_ROOT / "tmp" / "debug_output"
output_dir.mkdir(parents=True, exist_ok=True)

result = process_text_in_background(
    logger=logger,
    LT_LANGUAGE="de-DE",
    raw_text="alarm",
    output_dir=output_dir,
    recording_time=0.0,
    active_lt_url=""
)

print("\n--- STEP-BY-STEP PIPELINE TRACE COMPLETE ---")
print(f"Final Result: '{result}'")
