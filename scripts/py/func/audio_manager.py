# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# scripts/py/func/audio_manager.py
"""
Cross-platform microphone control utility.

This module provides functions to mute, unmute, toggle, and check the mute state
of the default system microphone on Windows, macOS, and Linux.

Core Functions:
- mute_microphone():   Explicitly mutes the microphone.
- unmute_microphone(): Explicitly unmutes the microphone.
- toggle_microphone_mute(): Toggles the microphone's current mute state.
- is_microphone_muted():  Returns True if the microphone is muted, False otherwise.

How to Use:
1.  **Installation:**
    -   For Windows support: `pip install pycaw comtypes`
    -   For Linux: Ensure 'pactl' (from libpulse/pulseaudio-utils) is installed.
    -   For macOS: No extra dependencies are needed.

2.  **Integration:**
    -   Import the desired function: `from .audio_manager import mute_microphone`
    -   Call it with a logger: `mute_microphone(logger)`
"""

import sys
import subprocess
import logging
import os

# Set up a basic logger for standalone testing or if no logger is passed
log = logging.getLogger(__name__)
if not log.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Platform-Specific Implementations ---

def _get_mute_state_windows(logger):
    if os.getenv('CI'):
        logger.info("CI env: Skipping hardware call.")
        return False

    try:
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        return volume.GetMute() == 1
    except Exception:
        logger.error("Failed to get Windows microphone mute state.", exc_info=True)
        return None

def _set_mute_state_windows(mute: bool, logger):
    logger.info(f"Setting Windows microphone mute state to: {mute}")

    if os.getenv('CI'):
        logger.info("CI env: Skipping hardware call.")
        return False

    try:
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMute(1 if mute else 0, None)
        logger.info(f"✅ Windows microphone mute state set to {mute}.")
        return True
    except Exception as e:
        logger.error(f"Failed to set Windows microphone mute state: {e}", exc_info=True)
        return False

def _get_mute_state_linux(logger):

    if os.getenv('CI'):
        logger.info("CI environment detected. Skipping pactl command for get_mute.")
        return False

    try:
        cmd = ['pactl', 'get-source-mute', '@DEFAULT_SOURCE@']
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        # pactl output is "Mute: yes" or "Mute: no"
        return "yes" in result.stdout.lower()
    except Exception:
        logger.error("Failed to get Linux microphone mute state.", exc_info=True)
        return None

def _set_mute_state_linux(mute: bool, logger):
    if os.getenv('CI'):
        logger.info("CI env: Skipping hardware call.")
        return False

    logger.info(f"Setting Linux microphone mute state to: {mute}")
    try:
        state = '1' if mute else '0'
        cmd = ['pactl', 'set-source-mute', '@DEFAULT_SOURCE@', state]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"✅ Linux microphone mute state set to {mute}.")
        return True
    except Exception as e:
        logger.error(f"Failed to set Linux microphone mute state: {e}", exc_info=True)
        return False

def _get_mute_state_macos(logger):
    if os.getenv('CI'):
        logger.info("CI env: Skipping hardware call.")
        return False

    try:
        cmd = "osascript -e 'input volume of (get volume settings)'"
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return int(result.stdout.strip()) == 0
    except Exception:
        logger.error("Failed to get macOS microphone mute state.", exc_info=True)
        return None

def _set_mute_state_macos(mute: bool, logger):
    logger.info(f"Setting macOS microphone mute state to: {mute}")
    if os.getenv('CI'):
        logger.info("CI env: Skipping hardware call.")
        return False


    try:
        if mute:
            cmd = "osascript -e 'set volume input volume 0'"
        else:
            # Unmute to a sensible default volume (75%) to avoid clipping
            cmd = "osascript -e 'set volume input volume 75'"
        subprocess.run(cmd, shell=True, check=True)
        logger.info(f"✅ macOS microphone mute state set to {mute}.")
        return True
    except Exception as e:
        logger.error(f"Failed to set macOS microphone mute state: {e}", exc_info=True)
        return False

# --- Public API Functions ---

def is_microphone_muted(logger=None):
    """Checks if the default system microphone is currently muted."""
    active_logger = logger if logger else log
    if os.getenv('CI'):
        active_logger.info("CI env: Skipping hardware call.")
        return False

    if sys.platform == "win32":
        return _get_mute_state_windows(active_logger)
    elif sys.platform == "linux":
        return _get_mute_state_linux(active_logger)
    elif sys.platform == "darwin":
        return _get_mute_state_macos(active_logger)
    else:
        active_logger.warning(f"Unsupported OS: {sys.platform}")
        return None

def mute_microphone(logger=None):
    active_logger = logger if logger else log
    if os.getenv('CI'):
        active_logger.info("CI env: Skipping hardware call.")
        return False
    """Mutes the default system microphone."""


    try:
        if sys.platform == "win32":
            return _set_mute_state_windows(True, active_logger)
        elif sys.platform == "linux":
            return _set_mute_state_linux(True, active_logger)
        elif sys.platform == "darwin":
            return _set_mute_state_macos(True, active_logger)
        else:
            active_logger.warning(f"Unsupported OS: {sys.platform}")
            return False
    except Exception as e:
        # Log the specific error for debugging purposes. Using .error is best practice here.
        active_logger.error(f"An unexpected error occurred during unmute_microphone: {e}", exc_info=True)
        # Add a general info message to confirm the service is not stopping.
        active_logger.info("The audio control operation failed, but the service will continue to run.")
        # Return False to indicate the operation was not successful.
        return False

def unmute_microphone(logger=None):
    active_logger = logger if logger else log
    if os.getenv('CI'):
        logger.info("CI env: Skipping hardware call.")
        return False
    """
    Unmutes the default system microphone.
    This function is wrapped in a robust try-except block to prevent service crashes.
    """
    try:
        if sys.platform == "win32":
            return _set_mute_state_windows(False, active_logger)
        elif sys.platform == "linux":
            return _set_mute_state_linux(False, active_logger)
        elif sys.platform == "darwin":
            return _set_mute_state_macos(False, active_logger)
        else:
            active_logger.warning(f"Unsupported OS for unmute operation: {sys.platform}")
            return False

    except Exception as e:
        # Log the specific error for debugging purposes. Using .error is best practice here.
        active_logger.error(f"An unexpected error occurred during unmute_microphone: {e}", exc_info=True)
        # Add a general info message to confirm the service is not stopping.
        active_logger.info("The audio control operation failed, but the service will continue to run.")
        # Return False to indicate the operation was not successful.
        return False


def toggle_microphone_mute(logger=None):
    """Toggles the default system microphone mute state."""
    active_logger = logger if logger else log

    if os.getenv('CI'):
        logger.info("CI env: Skipping hardware call.")
        return False


    is_muted = is_microphone_muted(active_logger)
    if is_muted is None:
        active_logger.error("Could not determine microphone state, cannot toggle.")
        return False

    if is_muted:
        active_logger.info("Microphone is muted, will unmute.")
        return unmute_microphone(active_logger)
    else:
        active_logger.info("Microphone is active, will mute.")
        return mute_microphone(active_logger)

# --- Standalone Test Block ---
if __name__ == '__main__':
    log.info("--- Microphone Control Test ---")

    try:
        initial_state = "Muted" if is_microphone_muted() else "Active"
        log.info(f"Initial microphone state: {initial_state}")

        input("Press Enter to MUTE the microphone...")
        mute_microphone()

        input("Press Enter to UNMUTE the microphone...")
        unmute_microphone()

        input("Press Enter to TOGGLE the microphone...")
        toggle_microphone_mute()

        log.info("--- Test finished. Toggling back to initial state... ---")
        toggle_microphone_mute()
        final_state = "Muted" if is_microphone_muted() else "Active"
        log.info(f"Final microphone state: {final_state}")

    except KeyboardInterrupt:
        log.info("\nTest aborted by user.")
