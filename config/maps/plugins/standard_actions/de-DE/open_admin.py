# config/maps/plugins/standard_actions/de-DE/open_admin.py
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

    plugin_path = Path(__file__).resolve()
    # project_root = plugin_path.parents[6]

    tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
    project_root = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

    if os.name == 'nt':  # Windows
        streamlit_bin = project_root / ".venv" / "Scripts" / "streamlit.exe"
    else:  # Linux / Mac
        streamlit_bin = project_root / ".venv" / "bin" / "streamlit"

    script_path = project_root / "scripts" / "py" / "chat" / "streamlit-admin.py"

    if not is_port_open(port):
        subprocess.Popen(
            [str(streamlit_bin), "run", str(script_path), "--server.port", str(port)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
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
                # open (macOS)
                print(e)
                subprocess.Popen(["open", f"http://localhost:{port}"],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                 env=clean_env)
            except Exception as e:
                print(e)
                import webbrowser
                webbrowser.open(f"http://localhost:{port}")

    return "Ich habe das Aura Admin Dashboard für dich geöffnet."
