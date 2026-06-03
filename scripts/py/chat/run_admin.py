#!/usr/bin/env python3
"""
Aura Admin — On-Demand Web Stack Launcher
scripts/py/chat/run_admin.py

Double-click entry point (via .desktop / .bat shortcut).
Starts FastAPI :8830 + Streamlit :8084 only when cold, then opens the browser.
No persistent background servers needed at boot — zero idle footprint.
"""
import socket, subprocess, sys, time, webbrowser
from pathlib import Path

# ── Resolve venv Python regardless of working directory ──────────────────────
ROOT   = Path(__file__).resolve().parents[3]   # …/sl5-aura/
PYTHON = ROOT / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
PYTHON = str(PYTHON) if PYTHON.exists() else sys.executable


def _alive(port: int) -> bool:
    """Return True if something is already listening on *port*."""
    s = socket.socket()
    try:
        return s.connect_ex(("127.0.0.1", port)) == 0
    finally:
        s.close()


def _wake(port: int, *cmd, pause: float = 2.0) -> None:
    """Spawn *cmd* in the background only when *port* is not yet open."""
    if not _alive(port):
        subprocess.Popen(list(map(str, cmd)), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(pause)   # give the process a moment to bind


# ── 1. FastAPI gateway (API routes, /admin redirect) ─────────────────────────
_wake(8830, PYTHON, ROOT / "scripts/py/service_api.py")

# ── 2. Streamlit admin UI ─────────────────────────────────────────────────────
_wake(
    8084, PYTHON, "-m", "streamlit", "run",
    ROOT / "scripts/py/chat/streamlit-admin.py",
    "--server.port=8084", "--server.headless=true",
    pause=4.0,   # Streamlit's import phase takes longer than FastAPI's
)

# ── 3. Wait until Streamlit accepts connections (hard cap: 20 s) ──────────────
deadline = time.time() + 20
while not _alive(8084) and time.time() < deadline:
    time.sleep(0.5)

# ── 4. Open browser ────────────────────────────────────────────────────────────
webbrowser.open("http://localhost:8084")
print("[AURA] Admin UI live → http://localhost:8084")
