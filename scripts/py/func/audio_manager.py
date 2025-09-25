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
import array
import math


# Set up a basic logger for standalone testing or if no logger is passed
log = logging.getLogger(__name__)
if not log.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Fallback for systems without winsound (e.g., Linux, macOS)
if sys.platform != "win32":
    try:
        import pygame
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        # Pre-create a simple beep sound
        # beep_sound_high = pygame.mixer.Sound(b'\x00\xff\x00\xff' * 100)  # Simple high-pitched wave
        # beep_sound_low = pygame.mixer.Sound(b'\x00\x00\xff\xff' * 100)   # Simple low-pitched wave
        # def play_beep(frequency, duration_ms):
        #     # Pygame doesn't directly support frequency/duration for simple beeps like winsound.Beep.
        #     # This is a very rough approximation for demonstration.
        #     if frequency > 700: # Arbitrary high freq threshold
        #         beep_sound_high.play()
        #     else:
        #         beep_sound_low.play()
        #     pygame.time.wait(duration_ms)


        # def create_sine_wave_sound(frequency, duration_ms, volume=0.5, sample_rate=44100):
        #     """
        #     Generates a stereo sine wave sound.
        #     frequency: frequency in Hz
        #     duration_ms: duration in milliseconds
        #     volume: amplitude (0.0 to 1.0)
        #     sample_rate: samples per second
        #     """
        #     num_samples = int(sample_rate * (duration_ms / 1000.0))
        #     # Pygame's default for Sound is 16-bit signed, so values from -32768 to 32767
        #     max_amplitude = 32767 * volume
        #
        #     samples = array.array('h')  # 'h' for signed short (2 bytes)
        #
        #     for i in range(num_samples):
        #         # Calculate sine wave value
        #         value = max_amplitude * math.sin(2 * math.pi * frequency * (i / sample_rate))
        #         samples.append(int(value))
        #         samples.append(int(value))  # For stereo, append twice
        #
        #     return pygame.mixer.Sound(samples)


        def create_bent_sine_wave_sound(
                start_freq,
                end_freq,
                duration_ms,
                volume=0.4,
                sample_rate=44100
        ):
            """
            Generates a stereo sine wave sound with an optional pitch bend.
            - start_freq: starting frequency in Hz
            - end_freq: ending frequency in Hz (for pitch bend; same as start for flat tone)
            - duration_ms: duration in milliseconds
            - volume: amplitude (0.0 to 1.0)
            - sample_rate: samples per second
            """
            num_samples = int(sample_rate * (duration_ms / 1000.0))
            max_amplitude = 32767 * volume
            samples = array.array('h')

            for i in range(num_samples):
                # Linear interpolation for pitch bend
                t = i / num_samples
                freq = start_freq + (end_freq - start_freq) * t
                value = max_amplitude * math.sin(2 * math.pi * freq * (i / sample_rate))
                # Stereo: append same sample for both channels
                samples.append(int(value))
                samples.append(int(value))

            return pygame.mixer.Sound(buffer=samples)

    except ImportError:
        log.warning("pygame not found. Sound feedback will not work on non-Windows systems.")
        # def play_beep(frequency, duration_ms):
        #     pass # No sound feedback if pygame is not available
# else:
#     import winsound
    # def play_beep(frequency, duration_ms):
    #     winsound.Beep(frequency, duration_ms)


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

def mute_microphone(logger=None,onlySound=False):
    active_logger = logger if logger else log
    if os.getenv('CI'):
        active_logger.info("CI env: Skipping hardware call.")
        return False
    """Mutes the default system microphone."""

    active_logger.info(f"mute_microphone()")

    active_logger.info(f"Muted sound")

    # Muted sound (high-pitched tone)
    # play_beep(600, 400)  # 1000 Hz frequency, 100 ms duration

    # medium_pitch_sound = create_sine_wave_sound(500, 200, volume=0.4)  # 600 Hz for 3 seconds
    # medium_pitch_sound.play()
    # time.sleep(3.5)

    # "Mute" sound: quick down-bending tone
    mute_sound = create_bent_sine_wave_sound(
        start_freq=1200,  # Start higher
        end_freq=800,  # Bend down
        duration_ms=40,  # Quick
        volume=0.1
    )
    mute_sound.play()
    # pygame.mixer.quit()
    if onlySound:
        return None

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
        active_logger.info("CI env: Skipping hardware call.")
        return False
    """
    Unmutes the default system microphone.
    This function is wrapped in a robust try-except block to prevent service crashes.
    """

    # Unmuted sound (normal tone)
    # play_beep(500, 100)  # 500 Hz frequency, 100 ms duration

    # low_pitch_sound = create_sine_wave_sound(200, 200, volume=0.4)  # 200 Hz for 3 seconds
    # print("\nPlaying LOW pitch sound (200 Hz for 3 seconds)...")
    # low_pitch_sound.play()
    # pygame.mixer.quit()

    # medium_pitch_sound = create_sine_wave_sound(500, 200, volume=0.4)  # 600 Hz for 3 seconds
    # medium_pitch_sound.play()

    # "Unmute" sound: quick up-bending tone
    unmute_sound = create_bent_sine_wave_sound(
        start_freq=1500,  # Start lower
        end_freq=2000,  # Bend up
        duration_ms=110,
        volume=0.2
    )
    unmute_sound.play()
    # pygame.mixer.quit()

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
        active_logger.info("CI env: Skipping hardware call.")
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
