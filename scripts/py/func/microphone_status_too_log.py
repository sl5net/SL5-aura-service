# Improved microphone logger.for STT Aura
# scripts/py/func/microphone_status_too_log.py
import sounddevice as sd
import platform

# Assuming logger.is already configured
# logger.basicConfig(level=logger.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_microphone_status(logger):
    """
    Logs detailed information about available audio input devices and the default device.
    This helps diagnose microphone issues when no audio is detected.
    """
    logger.info("🎤 --- Microphone Status Check (triggered due to no audio detection) ---")
    try:
        devices = sd.query_devices()
        logger.info("🎤 All available input devices:")
        for idx, device in enumerate(devices):
            if device['max_input_channels'] > 0: # Only list devices with input capabilities
                logger.info(f"🎤   Device {idx}: '{device['name']}' (Channels: {device['max_input_channels']}, Host API: {sd.query_hostapis(device['hostapi'])['name']})")

        # Get and log default input device
        default_input_index = sd.default.device[0]
        default_input_device = sd.query_devices(default_input_index)
        logger.info(f"🎤 Default Input Device: '{default_input_device['name']}' (Index: {default_input_index}, Channels: {default_input_device['max_input_channels']})")
        logger.info(f"🎤 Host API for Default Device: {sd.query_hostapis(default_input_device['hostapi'])['name']}")

    except Exception as e:
        logger.error(f"🎤 An error occurred while checking microphone devices: {e}")
        logger.info("🎤 Please ensure 'sounddevice' is correctly installed and your system has active audio input devices.")

    is_linux = (platform.system() == "Linux")

    if is_linux:
        # find your mic
        logger.info("🎤 watch -n 0.5 'pactl list sources | grep -E \"Name:|Description:|Mute:|Source #\"")



    logger.info("🎤 --- End Microphone Status Check ---")

# Call this function when STT Aura detects no input
# For example:
# if no_audio_detected:
#     log_microphone_status()
