#!/usr/bin/env python3
# scripts/py/set_secrets_to_DEFAULT_CONTENT.py
from pathlib import Path
import tempfile
import os

SECRETS_PATH = Path(".secrets")
DEFAULT_CONTENT = """
API_KEY=demo
SERVICE_API_KEY=demo
"""

def demo_secrets():
    ensure_secrets_file(SECRETS_PATH, DEFAULT_CONTENT.strip())

def ensure_secrets_file(path: Path, content: str) -> None:



    if path.exists():
        # print(f"{path} already exist (existiert bereits). nothing to do (Nichts zu tun).")
        return

    dirpath = path.parent or Path(".")
    with tempfile.NamedTemporaryFile("w", dir=dirpath, delete=False) as tmp:
        tmp.write(content)
        tmp_name = tmp.name

    os.replace(tmp_name, str(path))
    print(f"{path} was created (wurde erstellt).")

if __name__ == "__main__":
    ensure_secrets_file(SECRETS_PATH, DEFAULT_CONTENT)
