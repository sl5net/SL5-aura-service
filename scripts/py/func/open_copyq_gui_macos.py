# scripts/py/func/open_copyq_gui_macos.py
import platform
import shutil
import subprocess
from pathlib import Path


def open_copyq_gui_macos(logger=None, open_commands: bool = True) -> bool:
    """
    Safely opens the CopyQ GUI window on macOS upon Aura startup.
    Optionally opens the Commands/Shortcuts configuration dialog (F6).
    Resets window geometry to prevent off-screen position bugs.
    Never raises exceptions to prevent any disturbance to Aura startup.
    """
    
    if platform.system() != "Darwin":
        return False

    copyq_bin = shutil.which("copyq")
    if not copyq_bin:
        app_bin = Path("/Applications/CopyQ.app/Contents/MacOS/copyq")
        if app_bin.is_file():
            copyq_bin = str(app_bin)

    if not copyq_bin:
        if logger:
            logger.warning("CopyQ binary not found on macOS; skipping GUI opening.")
        return False

    try:
        # Clear off-screen geometry coordinates to ensure window appears on-screen
        subprocess.run(
            [copyq_bin, "config", "geometry", ""],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )

        # Request showing the CopyQ main window via IPC
        res = subprocess.run(
            [copyq_bin, "show"],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )

        # Fallback to macOS open command if IPC show did not succeed

        if res.returncode != 0:
            subprocess.run(
                ["open", "-a", "CopyQ"],
                capture_output=True,
                text=True,
                timeout=3,
                check=False,
            )

        if open_commands:
            # Open the Commands dialog (F6) so the user can inspect and configure shortcuts
            subprocess.run(
                [copyq_bin, "eval", "addCommands([])"],
                capture_output=True,
                text=True,
                timeout=3,
                check=False,
            )
            if logger:
                logger.info("CopyQ commands dialog requested on macOS.")

        if logger:
            logger.info("CopyQ GUI window requested on macOS.")
        return True    
    
    except (subprocess.SubprocessError, OSError) as exc:
        if logger:
            logger.warning(f"Failed to open CopyQ GUI on macOS: {exc}")
        return False
