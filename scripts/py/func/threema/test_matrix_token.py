# ---
"""Diagnostic script to verify Matrix access token and account identity."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import httpx

PROJECT_ROOT = Path(__file__).resolve().parents[4]
SECRETS_PATH = PROJECT_ROOT / ".secrets"

if SECRETS_PATH.exists():
    load_dotenv(SECRETS_PATH)

token = os.environ.get("MATRIX_ACCESS_TOKEN", "").strip().strip("'\"")
homeserver = os.environ.get("MATRIX_HOMESERVER_URL", "https://matrix.tchncs.de").rstrip("/")

print(f"Loaded Homeserver: {homeserver}")
print(f"Token Length: {len(token)}")
if token:
    print(f"Token Preview: {token[:1]}...{token[-1:]}")
else:
    print("Error: MATRIX_ACCESS_TOKEN is empty.")
    sys.exit(1)

headers = {"Authorization": f"Bearer {token}"}

for target in [homeserver, "https://matrix-client.matrix.org"]:
    url = f"{target}/_matrix/client/v3/account/whoami"
    try:
        resp = httpx.get(url, headers=headers, timeout=10.0)
        print(f"\nTarget: {target}")
        print(f"Status: {resp.status_code}")
        print(f"Body: {resp.text}")
    except httpx.RequestError as exc:
        print(f"\nTarget: {target} failed: {exc}")

