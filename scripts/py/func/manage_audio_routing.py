# py/func/manage_audio_routing.py:1
import subprocess
import sys


def get_desktop_monitor_source():
    # forks for Linux
    try:
        default_sink = subprocess.check_output(["pactl", "get-default-sink"]).decode().strip()
        sources = subprocess.check_output(["pactl", "list", "sources", "short"]).decode().splitlines()
        for source in sources:
            if default_sink in source and "monitor" in source:
                return source.split()[1]
    except Exception as e:
        print(f'Exception getting default sink: {e}')
        return None
    return None

abschalten = """
1.1.'26 00:13 Thu
virtuellen Umleitungen im System wieder abschalten:
pactl unload-module module-loopback
pactl unload-module module-null-sink


Wichtiger Hinweis: Das Entladen via pactl unload-module module-null-sink funktioniert oft nicht ohne ID. Ein sauberer Weg wäre, die Rückgabewerte (IDs) der load-module-Befehle zu speichern und diese gezielt zu entladen. Aber für einen ersten Test ist die dynamische desktop_source oben der wichtigste Schritt.
"""

# def manage_audio_routing(mode):
#     """
#     Automates the pactl commands based on the selected mode.
#     """
#     # Always attempt to clean up existing virtual modules first to avoid duplicates
#     subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
#     subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
#
#     if mode == 'MIC_AND_DESKTOP':
#         # 1. Create the virtual sink
#         subprocess.run(["pactl", "load-module", "module-null-sink", "sink_name=mic_and_desktop_Sink"], check=True)
#         # 2. Route Microphone to the virtual sink
#         subprocess.run(["pactl", "load-module", "module-loopback", "source=@DEFAULT_SOURCE@", "sink=mic_and_desktop_Sink"], check=True)
#         # 3. Route Desktop Audio (Monitor) to the virtual sink
#         # Note: Replace '60' with the dynamic detection or the confirmed ID for your desktop monitor
#         subprocess.run(["pactl", "load-module", "module-loopback", "source=60", "sink=mic_and_desktop_Sink"], check=True)

def is_mic_and_desktop_sink_active():
    try:
        output = subprocess.check_output(["pactl", "list", "sinks", "short"]).decode()
        return "mic_and_desktop_Sink" in output
    except Exception as e:
        print(f'Exception getting mic_and_desktop_Sink: {e}')
        return False


def manage_audio_routing(mode, logger=None):
    if sys.platform != "linux":
        if logger:
            logger.info(f"Audio routing skipped: pactl is not available on {sys.platform}")
        return
    if mode == 'MIC_AND_DESKTOP':
        if is_mic_and_desktop_sink_active():
            if logger: logger.debug("mic_and_desktop_Sink already active. Skipping setup.")
            return

    sink_name = "mic_and_desktop_Sink"
    logger.info(f"manage_audio_routing.py:66 | manage_audio_routing({mode} , ...) | sink={sink_name}")

    try:
        logger.info(f"manage_audio_routing.py:69 | manage_audio_routing({mode} , ...) | sink={sink_name}")
        # Always attempt to clean up existing virtual modules
        subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
        subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)

        if mode == 'MIC_AND_DESKTOP':

            logger.info(f"manage_audio_routing.py:76 | manage_audio_routing({mode} , ...) | sink={sink_name}")

            subprocess.run(["pactl", "load-module", "module-null-sink", f"sink_name={sink_name}"], check=True)
            subprocess.run(
                ["pactl", "load-module", "module-loopback", "source=@DEFAULT_SOURCE@", f"sink={sink_name}"],
                check=True)

            desktop_source = get_desktop_monitor_source()
            if desktop_source:
                subprocess.run(
                    ["pactl", "load-module", "module-loopback", f"source={desktop_source}", f"sink={sink_name}"],
                    check=True)
    except Exception as e:
        if logger: logger.error(f"Failed to manage audio routing on Linux: {e} | sink={sink_name}")