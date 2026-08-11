# tools/tests/test_direct_integration.py
import sys
import os
import logging
from pathlib import Path

# Setup logging to console (stdout)
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

sys.path.insert(0, str(SL5NET_AURA_PROJECT_ROOT))

# Import the core engine processor
from scripts.py.func.process_text_in_background import process_text_in_background

def run_test():
    print("--- Starting Direct Single-Process Integration Test ---")
    test_input = "Sandbank"
    print(f"Sending test input: '{test_input}'")

    # Run process directly in this process
    result = process_text_in_background(test_input)
    print(f"Result returned by engine: '{result}'")
    print("--- Test Finished ---")

if __name__ == "__main__":
    run_test()
