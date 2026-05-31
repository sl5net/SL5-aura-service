#!/usr/bin/env python3
"""
Aura Admin — On-Demand Web Stack Launcher
scripts/py/chat/run_admin.py

Double-click entry point (via .desktop / .bat shortcut).
Starts FastAPI :8830 + Streamlit :8084 only when cold, then opens the browser.
No persistent background servers needed at boot — zero idle footprint.
"""
import socket
import subprocess
import sys
import time
import webbrowser
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

# scripts/py/chat/run_admin.py:27
# scripts/py/chat/run_admin.py:27
def _wake(port: int, *cmd, pause: float = 2.0) -> None:
    """Spawn *cmd* in the background only when *port* is not yet open."""
    if not _alive(port):
        from pathlib import Path as p;import os as o # noqa: E702
        with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:project_root=p(f.read().strip()) # noqa: E702

        log_file = project_root / "log" / "streamlit-admin.log"
        with open(log_file, "a", encoding="utf-8") as lf:
            # Change stdout=subprocess.DEVNULL to stdout=lf to capture all logs
            subprocess.Popen(list(map(str, cmd)), stdout=lf, stderr=lf)
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
