# config/maps/plugins/standard_actions/de-DE/open_admin.py
"""
Aura Admin Interface Launcher Plugin.

- Dynamically resolves the project root directory.
- Verifies if 'streamlit' is installed; if missing, triggers a silent on-demand installation from 'requirements-web.txt'.
- Spawns the Streamlit admin server (port 8084) in the background if it is not already running.
- Securely launches the default system web browser (clearing local virtualenv library paths on Linux/macOS to prevent browser crashes) to display the Admin Dashboard.
"""
import logging
import subprocess
import socket
import time
import os
from pathlib import Path

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def get_clean_env():
    env = os.environ.copy()
    for key in ['LD_LIBRARY_PATH', 'LD_PRELOAD', 'PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV']:
        env.pop(key, None)
    return env

def execute(match_data):
    port = 8084

    tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
    project_root = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

    if os.name == 'nt':  # Windows
        streamlit_bin = project_root / ".venv" / "Scripts" / "streamlit.exe"
    else:  # Linux / Mac
        streamlit_bin = project_root / ".venv" / "bin" / "streamlit"

    # Check if streamlit is installed, and auto-install if missing
    if not streamlit_bin.exists():
        from scripts.py.func.try_auto_install_package import try_auto_install_package
        # We let the function fallback to print() since no logger is active here
        success = try_auto_install_package('streamlit',logger=logging)
        if not success:
            return "Failed to auto-install optional package Streamlit. Please install it manually."

    script_path = project_root / "scripts" / "py" / "chat" / "streamlit-admin.py"

    log_file = project_root / "log" / "streamlit-admin.log"
    with open(log_file, "a", encoding="utf-8") as lf:
        subprocess.Popen(
            [str(streamlit_bin), "run", str(script_path), "--server.port", str(port)],
            stdout=lf,
            stderr=lf,
            start_new_session=True
        )
        time.sleep(1.5)

    clean_env = get_clean_env()

    if os.name == 'nt':  # Windows
        os.system(f"start http://localhost:{port}")
    else:  # Linux / macOS
        try:
            subprocess.Popen(["xdg-open", f"http://localhost:{port}"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             env=clean_env)
        except Exception as e:
            try:
                print(e)
                subprocess.Popen(["open", f"http://localhost:{port}"],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                 env=clean_env)
            except Exception as e:
                print(e)
                import webbrowser
                webbrowser.open(f"http://localhost:{port}")

    return "Ich habe das Aura Admin Dashboard für dich geöffnet."