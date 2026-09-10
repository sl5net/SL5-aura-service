import math
import time
from PIL import Image, ImageDraw
import pystray


def create_tray_image(state: str = "idle", size: int = 32) -> Image.Image:
    """
    Generate solid RGB image for reliable rendering on X11 tray backends.
    """
    if state == "recording":
        # Solid vivid red
        return Image.new("RGB", (size, size), (230, 35, 35))
    # Solid vivid green for idle test
    return Image.new("RGB", (size, size), (35, 180, 35))


def main():
    print("Starting tray icon test…")
    idle_icon = create_tray_image("idle")
    recording_icon = create_tray_image("recording")

    icon = pystray.Icon("aura_test", idle_icon, "AURA Voice Assistant")
    icon.run_detached()

    print("State 1: IDLE (Pentagon shown in system tray). Waiting 3 seconds…")
    time.sleep(3)

    print("State 2: RECORDING (Red dot shown in system tray). Waiting 3 seconds…")
    icon.icon = recording_icon
    time.sleep(3)

    print("Stopping tray icon…")
    icon.stop()
    print("Test finished successfully.")


if __name__ == "__main__":
    main()
