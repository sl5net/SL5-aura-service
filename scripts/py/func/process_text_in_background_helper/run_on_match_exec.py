# scripts/py/func/process_text_in_background_helper/run_on_match_exec.py
from .load_module_from_path import load_module_from_path


def run_on_match_exec(on_match_exec_list, match_data, logger=None):
    """Execute all registered on_match_exec scripts with the raw match_data."""
    last_result = None
    for script_path in on_match_exec_list:
        module = load_module_from_path(script_path)
        if logger:
            logger.info(f"Executing on_match_exec: '{script_path}'")
        if hasattr(module, 'execute'):
            last_result = module.execute(match_data)
    return last_result
