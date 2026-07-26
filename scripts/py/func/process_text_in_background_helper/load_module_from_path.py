# scripts/py/func/process_text_in_background_helper/load_module_from_path.py
import os
from pathlib import Path
import importlib.util
import logging
def load_module_from_path(script_path, run_mode_override=None):

    path = Path(script_path)

    # scripts/py/func/process_text_in_background.py:88
    if run_mode_override:
        RUN_MODE = run_mode_override
    else:
        RUN_MODE = os.getenv('RUN_MODE')  # returns None or the value


    if RUN_MODE == "API_SERVICE" and path.parent.name.startswith('_'):
        print(
            f"a####### map_file_path={path.parent.parent.parent.parent.name} {path.parent.parent.parent.name} {path.parent.parent.name} {path.parent.name} {path.name} ++++++++++++++++++++++++")
        return None
    if RUN_MODE == "API_SERVICE" and path.parent.parent.name.startswith('_'):
        print(
            f"b####### map_file_path={path.parent.parent.parent.parent.name} {path.parent.parent.parent.name} {path.parent.parent.name} {path.parent.name} {path.name} ++++++++++++++++++++++++")
        return None
    if RUN_MODE == "API_SERVICE" and path.parent.parent.parent.name.startswith('_'):
        print(
            f"c####### map_file_path={path.parent.parent.parent.parent.name} {path.parent.parent.parent.name} {path.parent.parent.name} {path.parent.name} {path.name} ++++++++++++++++++++++++")
        return None    # Ignore folders that start with _

    print(
        f"####### map_file_path={path.parent.parent.parent.parent.name} {path.parent.parent.parent.name} {path.parent.parent.name} {path.parent.name} {path.name} ++++++++++++++++++++++++")

    spec = importlib.util.spec_from_file_location(path.stem, path)

    # <<< FIX 1: Add this check right here
    if spec is None:
        # Log this error to know which script failed
        logging.error(f"Could not create module spec for path: {script_path}")
        return None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


    return module
