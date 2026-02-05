# scripts/py/func/checks/run_function_with_throttling.py
import time
import json
from pathlib import Path
from datetime import timedelta

# --- Throttling Constants (Fixed Cooldown) ---
# --- Constants for the Throttling Mechanism ---
# FIXED_COOLDOWN_TIME = 1800.0  # 30 minutes in seconds

INITIAL_WAIT_TIME = 120.0
MAX_WAIT_TIME = 900.0

# INITIAL_WAIT_TIME = 1.0
# MAX_WAIT_TIME = 1.0

# run_always_no_throttling_ignore_times = True
run_always_no_throttling_ignore_times = False

# # tags: time inite minute seconds

"""
Konstanter Name	Wert	Begründung
INITIAL_WAIT_TIME	120.0 (2 Minuten)	Wir setzen den Startwert höher als die Dauer des Tests (~58s), um den zweiten Lauf fast immer zu blockieren. Der Entwickler hat dann ca. 2 Minuten Pause.
MAX_WAIT_TIME	900.0 (15 Minuten)	Ein realistisches Maximum. Bei jedem Neustart des Service in dieser Zeit wird blockiert. Nach 15 Minuten ist die Chance hoch, dass eine neue Entwicklungsphase begonnen hat.
"""

# --- State File Configuration (must be a persistent location) ---
# We assume a base directory (e.g., the log folder, or in this case, TMP_DIR)
# where the state file will be stored.
STATE_FILE_NAME = "self_test_throttle_state.json"


def _load_throttle_state(state_file_path: Path):
    """
    Loads the last execution time and minimum wait time from a JSON file.
    Returns initial state if file is missing or corrupted.
    """
    default_state = {
        'last_call_time': 0.0,
        'min_wait_time': INITIAL_WAIT_TIME
    }

    if not state_file_path.exists():
        return default_state

    try:
        with open(state_file_path, 'r') as f:
            state = json.load(f)

            # Basic validation and type conversion
            state['last_call_time'] = float(state.get('last_call_time', 0.0))
            state['min_wait_time'] = float(state.get('min_wait_time', INITIAL_WAIT_TIME))

            # Ensure min_wait_time is at least the initial value (in case of manual file corruption)
            if state['min_wait_time'] < INITIAL_WAIT_TIME:
                state['min_wait_time'] = INITIAL_WAIT_TIME
            return state

    except (IOError, json.JSONDecodeError) as e:
        # File access error or corrupt JSON: use default state and log the issue
        print(f"Warning: Could not load or decode state file {state_file_path}. Resetting state. Error: {e}")
        return default_state


def _save_throttle_state(state_file_path: Path, state: dict):
    """
    Saves the current state (last call time and min wait time) to a JSON file.
    """
    try:
        # Ensure the parent directory exists
        state_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(state_file_path, 'w') as f:
            json.dump(state, f, indent=4)
    except IOError as e:
        print(f"Error: Could not save state file {state_file_path}: {e}")


def run_function_with_throttling(
    logger,
    state_dir: Path,
    core_logic_function,
    func_params: dict,
    state_file_name: str = "throttling_state.json"  # Default name is now generic
):
    """
    Wrapper function that implements persistent exponential backoff
    before executing the core logic function.

    Args:
        logger: The logger object.
        state_dir (Path): The directory for persistent state storage (e.g., TMP folder).
        core_logic_function: The actual function to execute (takes arguments from func_params).
        func_params (dict): A dictionary of arguments (key=name, value=value) to pass to core_logic_function.
        state_file_name (str): The unique filename for this function's state.

    Returns:
        bool: True if the core logic was executed, False if throttled.
    """

    # Nested helpers to avoid polluting the module namespace
    def _load_throttle_state(state_file_path: Path):
        # ... (implementation as before, using INITIAL_WAIT_TIME) ...
        default_state = {'last_call_time': 0.0, 'min_wait_time': INITIAL_WAIT_TIME}
        if not state_file_path.exists(): return default_state
        try:
            with open(state_file_path, 'r') as f:
                state = json.load(f)
                return {
                    'last_call_time': float(state.get('last_call_time', 0.0)),
                    'min_wait_time': max(INITIAL_WAIT_TIME, float(state.get('min_wait_time', INITIAL_WAIT_TIME)))
                }
        except (IOError, json.JSONDecodeError) as e:
            logger.warning(f"Failed to load state file {state_file_path}. Resetting state. Error: {e}")
            return default_state

    def _save_throttle_state(state_file_path: Path, state: dict):
        try:
            state_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(state_file_path, 'w') as f:
                json.dump(state, f, indent=4)
        except IOError as e:
            logger.error(f"Could not save state file {state_file_path}: {e}")

    # --- Throttling Logic Starts Here ---

    state_file_path = state_dir / state_file_name
    current_time = time.time()

    # 1. Load the persistent state
    state = _load_throttle_state(state_file_path)
    last_call_time = state['last_call_time']
    min_wait_time = state['min_wait_time']
    time_since_last_call = current_time - last_call_time

    # 2. Throttling Check
    if not run_always_no_throttling_ignore_times and time_since_last_call < min_wait_time:
        wait_remaining = min_wait_time - time_since_last_call

        wait_remaining_minutes = int(wait_remaining // 60)
        wait_remaining_seconds = int(wait_remaining % 60)

        logger.info(
            f"Function call blocked (scripts/py/func/checks/run_function_with_throttling.py, Throttling on {state_file_name}). "
            f"Required wait: {min_wait_time:.1f}s. "
            f"Wait {wait_remaining_minutes}m {wait_remaining_seconds}s more ({wait_remaining:.2f}s total)."
        )
        return False

    # --- 3. Execution Allowed ---

    logger.info(f"Function call allowed. Running core logic for {state_file_name}...")
    self_test_start_time = current_time

    # EXECUTE CORE LOGIC: Use func_params to call the function
    # Note: We must ensure 'logger' is available to the core logic if it needs it.
    try:
        # Pass all collected parameters to the core function
        core_logic_function(**func_params)
    except Exception as e:
        # If the core logic fails, we might still want to proceed with backoff,
        # but for a test, we might want to log the error and skip updating the state.
        logger.error(f"Core function {core_logic_function.__name__} failed during execution: {e}")
        return False # Execution failed, don't update backoff counter

    # Measure and log duration
    self_test_end_time = time.time()
    self_test_duration = self_test_end_time - self_test_start_time
    self_test_readable_duration = timedelta(seconds=self_test_duration)
    logger.info(f"⌚ Execution duration: {self_test_readable_duration}")

    # 4. Update and Save State (Exponential Backoff Logic)
    new_wait_time = min_wait_time * 2

    if new_wait_time > MAX_WAIT_TIME:
        state['min_wait_time'] = INITIAL_WAIT_TIME
        logger.info(f"Wait time reset to {INITIAL_WAIT_TIME:.1f}s.")
    else:
        state['min_wait_time'] = new_wait_time
        logger.info(f"Wait time doubled to {new_wait_time:.1f}s.")

    state['last_call_time'] = self_test_end_time
    _save_throttle_state(state_file_path, state)

    return True
