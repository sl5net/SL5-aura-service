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
import os
import array
import math

import threading
import subprocess
import logging

from config.dynamic_settings import settings




# perf(audio): optimize Windows interaction latency
# - Moved heavy imports (comtypes, pycaw, numpy, pygame) to global scope.
# (24.12.'25 18:34 Wed, https://github.com/sl5net/SL5-aura-service/commit/c95c4929f77c950ae59a7eb2ac38dc76b616d1e8 )

# Global imports for heavy libraries to prevent runtime latency
try:
    import numpy as np
except ImportError:
    np = None

try:
    import pygame
except ImportError:
    pygame = None

# Windows-specific performance imports
if os.name == 'nt':
    try:
        import winsound
        import comtypes
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        # Pre-initialize COM once at module level to eliminate the 1s delay
        try:
            comtypes.CoInitialize()
        except Exception:
            pass
    except ImportError:
        winsound = None
        logging.error("Windows audio dependencies (pycaw/comtypes) not found.")



















logger = logging.getLogger(__name__)


# Initialize the function as a placeholder for Windows to avoid NameError
def create_bent_sine_wave_sound(*args, **kwargs):  # noqa: F811
    """
    Placeholder function for Windows and environments where Pygame is not used.
    Prevents NameError when sound functions are called.
    """

    class DummySound:
        def play(self):
            pass

    return DummySound()


# scripts/py/func/audio_manager.py:54
def speak_fallback(text_to_speak, language_code):
    """
    - Linux: espeak
    - Windows: PowerShell (SAPI)
    - macOS: say
    """

    command = []
    platform_name = ""

    if sys.platform.startswith('linux'):
        platform_name = "🐧Linux (espeak)"
        espeak_voice = convert_lang_code_for_espeak(language_code)
        command = [
            'espeak',
            '-v', espeak_voice,
            '-a', str(settings.ESPEAK_FALLBACK_AMPLITUDE),
            text_to_speak
        ]
    elif sys.platform == 'win32':
        platform_name = "🪟Windows (PowerShell TTS)"
        clean_text = text_to_speak.replace("'", "''")
        ps_command = f"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{clean_text}')"
        command = ['powershell', '-Command', ps_command]
    elif sys.platform == 'darwin':  # macOS
        platform_name = "🍏macOS (say)"
        command = ['say', text_to_speak]
    else:
        logger.warning(f"no TTS-Fallback  '{sys.platform}' .")
        return

    def run_command():
        try:
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            logger.info(f"audio_manager 92 🔊 ({platform_name}) '{text_to_speak[:30]}...' ")
            # logger.info(f"audio_manager.py: 92 🔊 Fallback ({platform_name}) '{text_to_speak[:30]}...' ")
            # logger.info(f"audio_manager.py: 92 🔊 Fallback ({platform_name}) '{text_to_speak[:30]}...' ")
            # logger.info(f"audio_manager.py: 92 🔊 Fallback ({platform_name}) '{text_to_speak[:30]}...' ")
        except FileNotFoundError:
            logger.info(f"fallback fouled '{command[0]}' no found.")
        except Exception as e:
            logger.info(f" {e}")

    thread = threading.Thread(target=run_command)
    thread.daemon = True
    thread.start()


def convert_lang_code_for_espeak(long_code: str) -> str:
    if not isinstance(long_code, str):
        return 'en'
    # 'de-DE' -> 'de'
    # 'en_US' -> 'en'
    # 'pt-BR' -> 'pt'
    # 'de'    -> 'de'
    short_code = long_code.split('-')[0].split('_')[0].lower()
    return short_code


# Set up a basic logger for standalone testing or if no logger is passed
log = logging.getLogger(__name__)
if not log.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fallback for systems without winsound (e.g., Linux, macOS)
if (sys.platform != "win32"
    and (settings.soundUnMute > 0 or settings.soundMute > 0)) \
        and not os.getenv('CI'):
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2)


        # from comtypes import CLSCTX_ALL

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

        def create_bent_sine_wave_sound(  # noqa: F811
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

    # audio_manager.py:211
    def _get_mute_state_windows(logger):
        if os.getenv('CI'):
            logger.info("CI env: Skipping hardware call.")
            return False

        logger.info(f"219: Audio Manager PID: {os.getpid()}")
        try:
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)
            return volume.GetMute() == 1
        except Exception:
            logger.info("Failed to get Windows microphone mute state.", exc_info=True)
            return None

# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# audio_manager.py: _set_mute_state_windows function

import os


def _set_mute_state_windows(mute: bool, logger):
    logger.info(f"235: Audio Manager PID: {os.getpid()}")
    
    """
    Set the microphone mute state on Windows using pycaw/comtypes.
    Local imports ensure cross-platform compatibility.
    Properly initializes COM for the calling thread, supports CI environments.
    Logs all errors via logger.
    """
    logger.info(f"Setting Windows microphone mute state to: {mute}")

    if os.getenv('CI'):
        logger.info("CI env: Skipping hardware call.")
        return False

    try:
        # import ctypes
        # Import from pycaw only inside this function

        # Explicitly initialize COM in the current thread.
        try:
            comtypes.CoInitialize()
        except (OSError, AttributeError):
            # May already be initialized -- skip if so.
            pass

        # Constants
        # eCapture = 1  # Audio endpoint for capture (microphone)
        # eCommunications = 2  # Role for communications devices

        # Use AudioUtilities to get audio devices
        devices = AudioUtilities.GetMicrophone()
        if not devices:
            logger.info("No microphone device found.")
            return False

        device = devices[0]
        interface = device.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMute(1 if mute else 0, None)
        logger.info(f"Microphone mute state set to {mute}")
        return True

    except Exception as e:
        logger.info(f"Failed to set Windows microphone mute state: {e}")
        return False


def _set_mute_state_linux(mute: bool, logger):
    if os.getenv('CI'):
        logger.info("CI env: Skipping hardware call.")
        return False
    logger.info(f"294: Audio Manager PID: {os.getpid()}")

    logger.info(f"Setting Linux microphone mute state to: {mute}")
    try:
        state = '1' if mute else '0'
        cmd = ['pactl', 'set-source-mute', '@DEFAULT_SOURCE@', state]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"✅ Linux microphone mute state set to {mute}.")
        return True
    except Exception as e:
        logger.info(f"Failed to set Linux microphone mute state: {e}", exc_info=True)
        return False


def _get_mute_state_macos(logger):
    if os.getenv('CI'):
        logger.info("CI env: Skipping hardware call.")
        return False
    logger.info(f"312: Audio Manager PID: {os.getpid()}")
    try:
        cmd = "osascript -e 'input volume of (get volume settings)'"
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return int(result.stdout.strip()) == 0
    except Exception:
        logger.info("Failed to get macOS microphone mute state.", exc_info=True)
        return None

def _get_mute_state_linux(logger):

    if os.getenv('CI'):
        logger.info("CI environment detected. Skipping pactl command for get_mute.")
        return False

    logger.info(f"327: Audio Manager PID: {os.getpid()}")

    try:
        cmd = ['pactl', 'get-source-mute', '@DEFAULT_SOURCE@']
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        # pactl output is "Mute: yes" or "Mute: no"
        return "yes" in result.stdout.lower()
    except Exception:
        logger.error("Failed to get Linux microphone mute state.", exc_info=True)
        return None

def _set_mute_state_macos(mute: bool, logger):
    logger.info(f"Setting macOS microphone mute state to: {mute}")
    if os.getenv('CI'):
        logger.info("CI env: Skipping hardware call.")
        return False

    logger.info(f"344: Audio Manager PID: {os.getpid()}")

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
        logger.info(f"Failed to set macOS microphone mute state: {e}", exc_info=True)
        return False


# --- Public API Functions ---

def is_microphone_muted(logger=None):
    """Checks if the default system microphone is currently muted."""
    active_logger = logger if logger else log

    if os.getenv('CI'):
        active_logger.info("CI env: Skipping hardware call.")
        return False

    logger.info(f"370: Audio Manager PID: {os.getpid()}")

    if sys.platform == "win32":
        return _get_mute_state_windows(active_logger)
    elif sys.platform == "linux":
        return _get_mute_state_linux(active_logger)
    elif sys.platform == "darwin":
        return _get_mute_state_macos(active_logger)
    else:
        active_logger.warning(f"Unsupported OS: {sys.platform}")
        return None

# scripts/py/func/audio_manager.py:370
def _play_bent_sine_wave_or_beep(start_freq, end_freq, duration_ms, volume, logger=None):
    """
    Ultra-robust sound playback with multi-stage fallbacks:
    1. Stereo Pygame (2 channels)
    2. Mono Pygame (1 channel)
    3. Windows System Beep (winsound)
    """
    import sys

    # Safety: Extremely low volume multiplier to prevent loudness issues
    final_volume = volume
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)

    # 1. Generate smooth phase-integrated waveform (Chirp)
    freqs = np.linspace(start_freq, end_freq, n_samples)
    dt = 2.0 / sample_rate
    phases = 2 * np.pi * np.cumsum(freqs) * dt
    waveform = np.sin(phases) * 32767 * final_volume

    # 2. Apply Soft-Envelope (Fade-in/out) to prevent clicking
    fade_len = min(int(sample_rate * 0.01), n_samples // 5)
    envelope = np.ones(n_samples)
    if fade_len > 0:
        envelope[:fade_len] = np.linspace(0, 1, fade_len)
        envelope[-fade_len:] = np.linspace(1, 0, fade_len)
    soft_waveform = (waveform * envelope).astype(np.int16)

    # Fallback Chain Logic
    for channels in [2, 1]:
        try:
            # Check if mixer needs (re)init
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(frequency=sample_rate, size=-16, channels=channels)

            # Prepare data shape for channels
            if channels == 2:
                final_data = np.column_stack([soft_waveform, soft_waveform])
            else:
                final_data = soft_waveform # 1D is fine for mono in modern pygame

            sound = pygame.sndarray.make_sound(final_data)
            sound.play()
            pygame.time.wait(duration_ms + 10)
            pygame.mixer.quit()
            return True # Success!

        except Exception as e:
            if logger:
                logger.info(f"Pygame failed (channels={channels}): {e}")
            try:
                pygame.mixer.quit()
            except Exception as e2:
                if logger: logger.info(f"424: {e2}")
                pass
            continue # Try next channel setting or exit to winsound

    # FINAL FALLBACK: Never forget the Beep!
    if sys.platform.startswith("win"):
        try:
            winsound.Beep(int(start_freq), int(duration_ms))
            if logger: logger.info("Fallback to winsound.Beep successful.")
            return True
        except Exception as e2:
            if logger: logger.info(f"winsound.Beep failed: {e2}")

    return False





def sound_program_loaded():
    if not getattr(settings, 'soundProgramLoaded', False):
        return
    _play_bent_sine_wave_or_beep(
        start_freq=400,
        end_freq=800,
        duration_ms=150,
        volume=0.1
    )


def sound_mute(active_logger):
    if not getattr(settings, 'soundMute', False):
        return

    active_logger.info(f"475: Audio Manager PID: {os.getpid()}")

    _play_bent_sine_wave_or_beep(
        start_freq=800,
        end_freq=400,
        duration_ms=55,
        volume=0.1,
        logger=active_logger
    )


def sound_unmute(active_logger):
    if not getattr(settings, 'soundUnMute', False):
        return

    logger.info(f"490: Audio Manager PID: {os.getpid()}")

    _play_bent_sine_wave_or_beep(
        start_freq=800,
        end_freq=1120,
        duration_ms=100,
        volume=0.2,
        logger=active_logger
    )


def mute_microphone(logger=None, onlySound=False):
    active_logger = logger if logger else log
    if os.getenv('CI'):
        active_logger.info("CI env: Skipping hardware call.")
        return False
    """Mutes the default system microphone."""

    active_logger.info(f"508: Audio Manager PID: {os.getpid()}")

    active_logger.info(f"mute_microphone()")

    active_logger.info(f"Muted sound")

    # Muted sound (high-pitched tone)
    # play_beep(600, 400)  # 1000 Hz frequency, 100 ms duration

    # medium_pitch_sound = create_sine_wave_sound(500, 200, volume=0.4)  # 600 Hz for 3 seconds
    # medium_pitch_sound.play()
    # time.sleep(3.5)

    # "Mute" sound: quick down-bending tone

    sound_mute(active_logger)

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
        # Log the specific error for debugging purposes. Using .info is best practice here.
        active_logger.info(f"An unexpected error occurred during unmute_microphone: {e}", exc_info=True)
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

    sound_unmute(active_logger)

    # pygame.mixer.quit()

    """
    Unmutes the default system microphone.
    Handles platform-specific implementations.
    """
    active_logger = logger if logger is not None else logging.getLogger(__name__)

    active_logger.info(f"553: Audio Manager PID: {os.getpid()}")


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
        # Log the specific error for debugging purposes. Using .info is best practice here.
        active_logger.info(f"An unexpected error occurred during unmute_microphone: {e}", exc_info=True)
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

    logger.info(f"609: Audio Manager PID: {os.getpid()}")

    is_muted = is_microphone_muted(active_logger)
    if is_muted is None:
        active_logger.info("Could not determine microphone state, cannot toggle.")
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










