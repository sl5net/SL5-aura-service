# scripts/py/func/try_auto_install_package.py
import re
import sys
import subprocess
from pathlib import Path

def try_auto_install_package(package_name: str, logger) -> bool:
    """
    Dynamically installs a Python package using the current virtual environment's pip
    if and only if it is explicitly whitelisted in requirements-web.txt.
    """
    # Resolve the project root (3 levels up from scripts/py/func/)
    project_root = Path(__file__).resolve().parents[3]
    req_file = project_root / "requirements-web.txt"

    if not req_file.exists():
        logger.error(f"[auto-install] Error: requirements-web.txt not found at: {req_file}")
        return False

    # Parse requirements-web.txt and look for the package name (case-insensitive)
    try:
        with open(req_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        logger.error(f"[auto-install] Failed to read requirements-web.txt: {e}")
        return False

    target_spec = None
    for line in lines:
        # Strip comments and whitespace
        clean_line = line.strip().split('#')[0].strip()
        if not clean_line:
            continue

        # Extract the package name before any version specifiers (==, >=, <=, etc.)
        name_match = re.split(r'==|>=|<=|>', clean_line)[0].strip()
        if name_match.lower() == package_name.lower():
            target_spec = clean_line
            break

    if not target_spec:
        logger.warning(f"[auto-install] Package '{package_name}' is not listed/whitelisted in requirements-web.txt. Aborting installation.")
        return False

    logger.info(f"[auto-install] Whitelisted package '{package_name}' detected. Installing '{target_spec}' inside virtual environment...")

    # Run pip install using the active python interpreter to guarantee it lands in .venv
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", target_spec],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        logger.info(f"[auto-install] Package '{package_name}' installed successfully!")
        return True
    except Exception as e:
        logger.error(f"[auto-install] Failed to install package '{package_name}': {e}")

    return False

