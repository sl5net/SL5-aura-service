
"""Utility script to generate a permanent Matrix device session token."""
import getpass
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import httpx

PROJECT_ROOT = Path(__file__).resolve().parents[4]
SECRETS_PATH = PROJECT_ROOT / ".secrets"

HOMESERVER = "https://matrix.tchncs.de"


def obtain_permanent_token() -> None:
    """Prompt for Matrix credentials and save permanent access token to .secrets."""
    username = input("Matrix username (e.g. seeh): ").strip().lstrip("@").split(":")[0]
    password = getpass.getpass("Matrix password: ")

    payload = {
        "type": "m.login.password",
        "user": username,
        "password": password,
        "initial_device_display_name": "AuraThreemaRelay",
    }

    url = f"{HOMESERVER}/_matrix/client/v3/login"
    try:
        resp = httpx.post(url, json=payload, timeout=20.0)
        if resp.status_code != 200:
            print(f"Login failed ({resp.status_code}): {resp.text}")
            sys.exit(1)

        data = resp.json()
        token = data.get("access_token")
        user_id = data.get("user_id")
        device_id = data.get("device_id")

        print(f"\nLogin successful: {user_id} (Device: {device_id})")

        # Update .secrets cleanly
        existing_lines = []
        if SECRETS_PATH.exists():
            existing_lines = SECRETS_PATH.read_text(encoding="utf-8").splitlines()

        filtered_lines = [
            line for line in existing_lines
            if not line.startswith("MATRIX_ACCESS_TOKEN=")
            and not line.startswith("MATRIX_HOMESERVER_URL=")
        ]
        filtered_lines.append(f'MATRIX_HOMESERVER_URL="{HOMESERVER}"')
        filtered_lines.append(f'MATRIX_ACCESS_TOKEN="{token}"')

        SECRETS_PATH.write_text("\n".join(filtered_lines) + "\n", encoding="utf-8")
        print(f"Permanent token successfully written to {SECRETS_PATH}")

    except httpx.RequestError as exc:
        print(f"Network error during login: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    obtain_permanent_token()
