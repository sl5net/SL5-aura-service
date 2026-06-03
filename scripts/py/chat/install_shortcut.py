#!/usr/bin/env python3
"""
Aura Admin — Desktop Shortcut Installer
scripts/py/chat/install_shortcut.py

Run once after initial setup.  Creates a launchable icon on the user's
Desktop that starts the entire web stack on-demand.

Supports:
  Linux   → ~/.desktop/aura-admin.desktop  (XDG standard)
  Windows → ~/Desktop/Aura Admin.bat

Usage:
  python scripts/py/chat/install_shortcut.py
"""
import stat
import sys
from pathlib import Path

ROOT     = Path(__file__).resolve().parents[3]          # …/sl5-aura/
PYTHON   = ROOT / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
PYTHON   = PYTHON if PYTHON.exists() else Path(sys.executable)
LAUNCHER = ROOT / "scripts/py/chat/run_admin.py"
ICON     = ROOT / "assets" / "aura-icon.png"            # adapt path if needed
DESKTOP  = Path.home() / "Desktop"


# ─────────────────────────────────────────────────────────────────────────────
def _install_linux() -> None:
    content = (
        "[Desktop Entry]\n"
        "Version=1.0\n"
        "Type=Application\n"
        "Name=Aura Admin\n"
        "Comment=Launch Sl5 Aura Admin UI on-demand (zero idle cost)\n"
        f"Exec={PYTHON} {LAUNCHER}\n"
        f"Icon={ICON}\n"
        "Terminal=false\n"
        "StartupNotify=true\n"
        "Categories=Utility;\n"
    )
    target = DESKTOP / "aura-admin.desktop"
    target.write_text(content)
    # Mark executable so the file manager can launch it without a dialog
    target.chmod(target.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print(f"[AURA] Linux shortcut installed → {target}")
    print("       If your file manager shows a warning, right-click → Allow Launching.")


def _install_windows() -> None:
    # .bat hides the terminal flash by using START /B; the Python process
    # itself calls webbrowser.open() so no console window is needed.
    content = (
        "@echo off\n"
        "title Aura Admin — starting...\n"
        f'start /B "" "{PYTHON}" "{LAUNCHER}"\n'
    )
    target = DESKTOP / "Aura Admin.bat"
    target.write_text(content)
    print(f"[AURA] Windows shortcut installed → {target}")
    print("       Tip: right-click → Create shortcut → pin to taskbar for a proper icon.")


def _install_unsupported() -> None:
    print("[AURA] Unsupported platform.  Create a shortcut manually pointing to:")
    print(f"       {PYTHON}  {LAUNCHER}")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    DESKTOP.mkdir(parents=True, exist_ok=True)

    if sys.platform.startswith("linux"):
        _install_linux()
    elif sys.platform == "win32":
        _install_windows()
    else:
        _install_unsupported()
