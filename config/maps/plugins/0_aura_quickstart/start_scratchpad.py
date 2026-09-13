# config/maps/plugins/0_aura_quickstart/start_scratchpad.py
import os
import sys
import subprocess


def start_scratchpad():
    python = ".venv/bin/python3" # sys.executable  # ".venv/bin/python3"
    script = os.path.join("config", "maps", "plugins", "0_aura_quickstart", "open_scratchpad_action.py")
    # detached unter Unix
    subprocess.Popen(
        [python, script, "--no-block"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        close_fds=True,
        start_new_session=True,  # os.setsid()
    )

if __name__ == "__main__":
    start_scratchpad()
