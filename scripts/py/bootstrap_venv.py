import os
import sys
from pathlib import Path

# Robust detection of active virtual environment (PEP 405)
in_venv = (sys.prefix != sys.base_prefix) or ('VIRTUAL_ENV' in os.environ)

if not in_venv:
    # Try to locate a local virtual environment (.venv or venv)
    # This file is at project_root/scripts/py/bootstrap_venv.py, so project_root is 2 levels up
    project_root = Path(__file__).resolve().parents[2]
    python_executable = None
    for name in [".venv", "venv"]:
        candidate_path = project_root / name
        if candidate_path.is_dir():
            if os.name == 'nt':  # Windows
                binary = candidate_path / "Scripts" / "python.exe"
            else:  # Linux / macOS
                binary = candidate_path / "bin" / "python"
            if binary.is_file():
                python_executable = binary
                break

    if python_executable:
        # Re-execute the script using the virtual environment's python interpreter
        print(f"[AURA ENGINE] Auto-activating virtual environment at: {python_executable.parent.parent.name}")
        os.environ['VIRTUAL_ENV'] = str(python_executable.parent.parent)
        os.execv(str(python_executable), [str(python_executable)] + sys.argv)
        sys.exit(0)
    else:
        print(
            "\n [AURA ENGINE] FATAL: Python virtual environment not activated and none found locally!",
            file=sys.stderr
        )
        if os.name == 'nt':  # Windows
            print(
                " Please start Aura using the official Windows batch script:\n"
                "   start_aura.bat\n",
                file=sys.stderr
            )
        else:  # Linux / macOS
            print(
                " Please start Aura using the recommended startup script:\n"
                "   ./scripts/restart_venv_and_run-server.sh\n"
                " Or the alternative activation script:\n"
                "   ./scripts/activate-venv_and_run-server.sh\n",
                file=sys.stderr
            )
        sys.exit(1)
else:
    # Ensure VIRTUAL_ENV environment variable is populated for sub-processes or other parts of the app
    if 'VIRTUAL_ENV' not in os.environ:
        os.environ['VIRTUAL_ENV'] = sys.prefix

def bootstrap_hello():
    print('bootstrap_venv is implemeted')
