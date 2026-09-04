import json
import os
import subprocess
import sys
import urllib.request

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if REPO_DIR not in sys.path:
    sys.path.insert(0, REPO_DIR)


def get_local_commit_sha():
    """Returns the short commit SHA of the local git HEAD if available."""
    try:
        subprocess.run(
            ["git", "branch", "--set-upstream-to=origin/master", "master"],
            cwd=REPO_DIR,
            capture_output=True,
            timeout=2.0,
            check=False
        )
        res = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=2.0,
            check=True
        )
        return res.stdout.strip()
    except Exception:
        return None


def check_for_updates(logger=None, timeout_seconds=4.0):
    """Checks GitHub for newer commits or official releases without blocking."""
    try:
        from config import settings
        mode = getattr(settings, "CHECK_FOR_UPDATES_ON_STARTUP", "commits")
    except Exception:
        mode = "commits"

    if not mode or mode in [False, "off", "disabled"]:
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
        elif mode_str == "commits":
            # Track and auto-update master commits
            local_sha = get_local_commit_sha()
            url = "https://api.github.com/repos/sl5net/SL5-aura-service/commits/master"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    remote_sha = data.get("sha", "")[:7]
                    commit_msg = data.get("commit", {}).get("message", "").split("\n")[0]

                    if local_sha and remote_sha and local_sha != remote_sha:
                        # Overwrite any dirty local files to guarantee update succeeds
                        subprocess.run(["git", "fetch", "origin", "master"], cwd=REPO_DIR, timeout=15.0, capture_output=True, check=False)
                        reset_res = subprocess.run(["git", "reset", "--hard", "origin/master"], cwd=REPO_DIR, timeout=10.0, capture_output=True, text=True, check=False)

                        if reset_res.returncode == 0:
                            msg = f"Update applied: pulled commit {remote_sha} ('{commit_msg}')."
                        else:
                            msg = f"Update available: New commit {remote_sha} ('{commit_msg}'), but update failed: {reset_res.stderr.strip()}"

                        if logger:
                            logger.info(msg)
                        else:
                            print(f"[INFO] {msg}")

    except Exception:
        # Offline or timeout - fail silently without blocking startup
        pass


if __name__ == "__main__":
    check_for_updates()
    
    
