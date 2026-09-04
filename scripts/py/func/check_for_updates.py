import json
import urllib.request


def check_for_updates(logger=None, timeout_seconds=1.5):
    """Checks GitHub for a newer release tag during startup without blocking."""
    try:
        from config import settings
        if not getattr(settings, "CHECK_FOR_UPDATES_ON_STARTUP", False):
            return
    except Exception:
        return

    url = "https://api.github.com/repos/sl5net/SL5-aura-service/releases/latest"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "SL5-Aura-Service-Update-Checker"}
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                latest_tag = data.get("tag_name", "")
                if latest_tag:
                    msg = f"Update available: Latest release is {latest_tag}. Run update script to upgrade."
                    if logger:
                        logger.info(msg)
                    else:
                        print(f"[INFO] {msg}")
    except Exception:
        # Offline or timeout - fail silently without blocking startup
        pass
