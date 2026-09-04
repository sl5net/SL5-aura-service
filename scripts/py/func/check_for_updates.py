import json
import subprocess
import urllib.request


def get_local_commit_sha():
    """Returns the short commit SHA of the local git HEAD if available."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=1.0,
            check=True
        )
        return res.stdout.strip()
    except Exception:
        return None


def check_for_updates(logger=None, timeout_seconds=2.0):
    """Checks GitHub for newer commits or official releases without blocking."""
    try:
        from config import settings
        mode = getattr(settings, "CHECK_FOR_UPDATES_ON_STARTUP", False)
        if not mode or mode in [False, "off", "disabled"]:
            return
    except Exception:
        return

    mode_str = str(mode).lower()
    headers = {"User-Agent": "SL5-Aura-Service-Update-Checker"}

    try:
        if mode_str in ["releases", "stable"]:
            url = "https://api.github.com/repos/sl5net/SL5-aura-service/releases/latest"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    latest_tag = data.get("tag_name", "")
                    if latest_tag:
                        msg = f"Release update available: {latest_tag}. Run update script to upgrade."
                        if logger:
                            logger.info(msg)
                        else:
                            print(f"[INFO] {msg}")
        else:
            # Default to tracking master commits
            local_sha = get_local_commit_sha()
            url = "https://api.github.com/repos/sl5net/SL5-aura-service/commits/master"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    remote_sha = data.get("sha", "")[:7]
                    commit_msg = data.get("commit", {}).get("message", "").split("\n")[0]
                    if local_sha and remote_sha and local_sha != remote_sha:
                        msg = f"Update available: New commit {remote_sha} ('{commit_msg}'). Run 'git pull' to update."
                        if logger:
                            logger.info(msg)
                        else:
                            print(f"[INFO] {msg}")
    except Exception:
        # Offline or timeout - fail silently without blocking startup
        pass
