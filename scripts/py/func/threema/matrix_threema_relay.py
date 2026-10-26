
"""Standalone Matrix long-polling relay to Threema Beta."""
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
import httpx

from scripts.py.func.get_project_root import get_aura_project_root
from scripts.py.func.threema.send_to_threema_window import send_to_threema_window

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
LOGGER = logging.getLogger("MatrixThreemaRelay")


def extract_text_messages(
    sync_payload: Dict[str, Any],
    target_room_id: Optional[str] = None,
    ignored_sender: Optional[str] = None,
) -> List[str]:
    """
    Pure function: extract text messages from Matrix sync payload.

    Benefits of functional purity:
    - Deterministic: Same input dictionary always yields identical message lists.
    - No side effects: Operates strictly without modifying input structures or external state.
    """
    messages: List[str] = []
    rooms_join = sync_payload.get("rooms", {}).get("join", {})

    for room_id, room_data in rooms_join.items():
        if target_room_id and room_id != target_room_id:
            continue

        events = room_data.get("timeline", {}).get("events", [])
        for event in events:
            if event.get("type") != "m.room.message":
                continue
            if ignored_sender and event.get("sender") == ignored_sender:
                continue

            content = event.get("content", {})
            if content.get("msgtype") == "m.text":
                body = content.get("body", "").strip()
                if body:
                    messages.append(body)

    return messages


def load_matrix_config() -> Dict[str, str]:
    """Load Matrix credentials from environment or project .secrets file."""
    root_dir = get_aura_project_root()
    secrets_path = Path(root_dir) / ".secrets"
    if secrets_path.exists():
        load_dotenv(secrets_path)

    homeserver = os.environ.get("MATRIX_HOMESERVER_URL", "https://tchncs.de").rstrip("/")
    token = os.environ.get("MATRIX_ACCESS_TOKEN", "").strip()
    room_id = os.environ.get("MATRIX_ROOM_ID", "").strip()
    ignored_sender = os.environ.get("MATRIX_IGNORED_SENDER", "").strip()

    return {
        "homeserver": homeserver,
        "token": token,
        "room_id": room_id,
        "ignored_sender": ignored_sender,
    }


def run_relay() -> None:
    """Run long-polling sync loop and forward received messages to Threema."""
    config = load_matrix_config()
    token = config["token"]
    if not token:
        LOGGER.error("MATRIX_ACCESS_TOKEN is not set. Please add it to .secrets or environment.")
        sys.exit(1)

    homeserver = config["homeserver"]
    room_id = config["room_id"] or None
    ignored_sender = config["ignored_sender"] or None

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    client = httpx.Client(base_url=homeserver, headers=headers, timeout=40.0)

    LOGGER.info("Starting initial sync against %s ...", homeserver)
    try:
        initial_resp = client.get("/_matrix/client/v3/sync", params={"timeout": 0})
        initial_resp.raise_for_status()
        next_batch = initial_resp.json().get("next_batch", "")
        LOGGER.info("Initial sync successful. Ready to relay incoming messages.")
    except httpx.HTTPError as exc:
        LOGGER.error("Initial sync failed: %s", exc)
        sys.exit(1)

    while True:
        try:
            params = {
                "since": next_batch,
                "timeout": 30000,
            }
            resp = client.get("/_matrix/client/v3/sync", params=params)
            if resp.status_code == 200:
                data = resp.json()
                next_batch = data.get("next_batch", next_batch)
                new_messages = extract_text_messages(
                    data,
                    target_room_id=room_id,
                    ignored_sender=ignored_sender,
                )
                for text in new_messages:
                    LOGGER.info("Forwarding message to Threema: %s", text)
                    send_to_threema_window(text=text, press_enter=True)
            else:
                LOGGER.warning("Sync returned unexpected status %d: %s", resp.status_code, resp.text)
                time.sleep(5.0)

        except httpx.RequestError as exc:
            LOGGER.warning("Network request error during sync: %s. Retrying in 5s...", exc)
            time.sleep(5.0)
        except KeyboardInterrupt:
            LOGGER.info("Relay stopped by user.")
            break


if __name__ == "__main__":
    run_relay()

