# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# File: scripts/py/func/press_trigger_button.py

import time

# --- Configuration ---
DEBOUNCE_SECONDS = 0.2  # 200ms cooldown

# --- State ---
# This variable stores the timestamp of the last accepted button press.
# It is internal to this module and not meant to be accessed from outside.
_last_valid_press_time = 0

def press_trigger_button():
    """
    Simulates a press of the trigger button.

    This function implements a "debounce" mechanism. It checks if enough time
    has passed since the last valid press. This prevents a single user
    action (that might create multiple system events) from being registered
    as multiple button presses.

    Returns:
        bool: True if the press was accepted (a valid "click").
              False if the press was rejected (ignored due to debouncing).
    """
    global _last_valid_press_time
    current_time = time.time()

    if (current_time - _last_valid_press_time) < DEBOUNCE_SECONDS:
        # The press happened too soon after the last one. Ignore it.
        return False

    # The press is valid. Update the timestamp and confirm.
    _last_valid_press_time = current_time
    return True
