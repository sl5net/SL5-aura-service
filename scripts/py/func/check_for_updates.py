import json
import os
import subprocess
import sys
import urllib.request

# Ensure repository root is in sys.path and resolve base directory
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if REPO_DIR not in sys.path:
    sys.path.insert(0, REPO_DIR)


def get_local_commit_sha(repo_dir=REPO_DIR):
    """Returns the full commit SHA of the local git HEAD."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=2.0,
            check=True
        )
        return res.stdout.strip()
    except Exception:
        return None


def force_update_to_remote(repo_dir=REPO_DIR):
    """Forces the local repository to match origin/master, discarding any local modifications."""
    try:
        # 1. Fetch latest commits from origin master
        fetch_res = subprocess.run(
            ["git", "fetch", "origin", "master"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=20.0,
            check=False
        )
        if fetch_res.returncode != 0:
            return False, f"git fetch failed: {fetch_res.stderr.strip()}"

        # 2. Hard reset working tree and index to origin/master (overwriting all local changes)
        reset_res = subprocess.run(
            ["git", "reset", "--hard", "origin/master"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=10.0,
            check=False
        )
        if reset_res.returncode != 0:
            return False, f"git reset failed: {reset_res.stderr.strip()}"

        return True, reset_res.stdout.strip()
    except Exception as e:
        return False, str(e)


def check_for_updates(logger=None, timeout_seconds=4.0, force=False):
    """Checks GitHub for newer commits and forcefully applies updates."""
    mode = True
    try:
        from config import settings
        mode = getattr(settings, "CHECK_FOR_UPDATES_ON_STARTUP", True)
    except Exception:
        pass

    def log_msg(msg, is_error=False):
        if logger:
            logger.error(msg) if is_error else logger.info(msg)
        else:
            prefix = "[ERROR]" if is_error else "[INFO]"
            print(f"{prefix} {msg}")

    if not force and mode in [False, "off", "disabled"]:
        log_msg("Update check is disabled in config/settings.py (CHECK_FOR_UPDATES_ON_STARTUP = False).")
        return

    mode_str = str(mode).lower() if not force else "commits"
    headers = {
        "User-Agent": "SL5-Aura-Service-Update-Checker",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        if mode_str in ["releases", "stable"]:
            url = "https://api.github.com/repos/sl5net/SL5-aura-service/releases/latest"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    latest_tag = data.get("tag_name", "")
                    if latest_tag:
                        log_msg(f"Release update available: {latest_tag}. Run update script to upgrade.")
        else:
            # Default: Track commits on master branch
            local_sha = get_local_commit_sha()
            url = "https://api.github.com/repos/sl5net/SL5-aura-service/commits/master"
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    remote_sha = data.get("sha", "")
                    commit_msg = data.get("commit", {}).get("message", "").split("\n")[0]

                    if local_sha and remote_sha and not remote_sha.startswith(local_sha):
                        log_msg(
                            f"New commit found on origin/master ({remote_sha[:7]} vs local {local_sha[:7]}). Applying forced update...")

                        # Execute forced update (overwriting dirty files)
                        success, result_msg = force_update_to_remote()
                        if success:
                            log_msg(f"Update successfully applied: pulled commit {remote_sha[:7]} ('{commit_msg}').")
                        else:
                            log_msg(f"Update failed: {result_msg}", is_error=True)
                    else:
                        log_msg(f"Aura is up to date ({local_sha[:7] if local_sha else 'unknown'}).")

    except Exception as e:
        log_msg(f"Update check failed: {e}", is_error=True)


if __name__ == "__main__":
    print("=== Starting manual update check (forced) ===")
    check_for_updates(force=True)
    
