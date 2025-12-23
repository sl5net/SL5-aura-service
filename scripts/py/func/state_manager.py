# scripts/py/func/state_manager.py
# state_manager.py
import os
import sys
from pathlib import Path


def get_lock_dir():
    tmp_base = Path("C:/tmp") if sys.platform.startswith('win') else Path("/tmp")
    return tmp_base / "sl5_aura" / "session" / "lock"


def should_trigger_startup(modname_str):
    # Use integer PID to avoid illegal characters in filenames
    print(f"{modname_str} should trigger startup")

    pid = os.getpid()
    lock_dir = get_lock_dir()

    # Ensure consistent naming without object-repr strings
    # <module 'config_maps_plugins_standard_actions_count_loud_de-DE_count_loud' from '_home_seeh_projects_py_STT_config_maps_plugins_standard_actions_count_loud_de-DE_count_loud_py'>_19449.lock
    safe_name = str(modname_str).replace(".", "_").replace("/", "_")
    # safe_name = str(modname_str).replace(".", "_").replace("/", "_").replace("\\", "_")
    session_file = lock_dir / f"{safe_name}_{pid}.lock"

    if session_file.exists():
        print(f"{session_file} exists, skipping")
        return False

    try:
        # session_file.parent.mkdir(parents=True, exist_ok=True)
        session_file.touch()
        print(f"{session_file} created")
        return True
    except Exception as e:
        print("Failed to trigger startup:", e)
        return False

