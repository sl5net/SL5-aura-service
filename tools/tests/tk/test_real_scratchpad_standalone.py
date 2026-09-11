# tools/test/tk/test_real_scratchpad_standalone.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.py.func.scratchpad.scratchpad_manager import open_scratchpad

open_scratchpad("http://127.0.0.1:8082", "de-DE", initial_text="Test")

import time
while True:
    time.sleep(1)
