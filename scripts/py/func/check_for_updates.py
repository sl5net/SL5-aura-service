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
            check=True,
        )
        return res.stdout.strip()
    except Exception:
        return None


def force_update_to_remote(repo_dir=REPO_DIR):
    """Forces the local repository to match the current remote branch, discarding modifications."""
    try:
        from scripts.py.func.config.dynamic_settings import settings

        if getattr(settings, "DEV_MODE", False):
            return False, "DEV_MODE is enabled; skipping forced reset"

        # Example: settings.UPDATE_EXCLUDED_USERS expected as iterable of usernames
        excluded = getattr(settings, "UPDATE_EXCLUDED_USERS", None)
        if excluded:
            # normalize to set of lowercase strings for robust checks
            if not isinstance(excluded, (set, list, tuple)):
                raise TypeError("UPDATE_EXCLUDED_USERS must be a list, tuple or set of usernames")
            excluded_set = {str(u).lower() for u in excluded}

            # current_user should be provided by caller (or derived elsewhere)
            if settings.current_user and str(settings.current_user).lower() in excluded_set:
                return False, f"User '{settings.current_user}' is excluded from forced updates"

        current_branch = get_current_branch(repo_dir)
        if not current_branch:
            return (
                False,
                "Cannot determine git branch; skipping reset to prevent data loss",
            )

        # 1. Fetch latest commits from origin for the current branch
        fetch_res = subprocess.run(
            ["git", "fetch", "origin", current_branch],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=20.0,
            check=False,
        )
        if fetch_res.returncode != 0:
            return False, f"git fetch failed: {fetch_res.stderr.strip()}"
        # 2. Hard reset working tree and index to origin/<current_branch>
        reset_res = subprocess.run(
            ["git", "reset", "--hard", f"origin/{current_branch}"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=10.0,
            check=False,
        )
        if reset_res.returncode != 0:
            return False, f"git reset failed: {reset_res.stderr.strip()}"

        return True, reset_res.stdout.strip()
    except Exception as e:
        return False, str(e)


def get_current_branch(repo_dir=REPO_DIR):
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=5.0,
            check=False,
        )
        if proc.returncode == 0:
            branch = proc.stdout.strip()
            return branch if branch and branch != "HEAD" else None
    except Exception:
        pass
    return None


def ensure_git_repo(
    repo_dir=REPO_DIR,
    default_branch="master",
    remote_url="https://github.com/sl5net/SL5-aura-service.git",
) -> bool:
    """Initializes git repository and sets up tracking branch if .git is missing."""
    git_dir = os.path.join(repo_dir, ".git")
    if os.path.isdir(git_dir):
        return True

    try:
        init_res = subprocess.run(
            ["git", "init"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=10.0,
            check=False,
        )
        if init_res.returncode != 0:
            return False

        subprocess.run(
            ["git", "remote", "remove", "origin"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=5.0,
            check=False,
        )
        add_res = subprocess.run(
            ["git", "remote", "add", "origin", remote_url],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=5.0,
            check=False,
        )
        if add_res.returncode != 0:
            return False

        fetch_res = subprocess.run(
            ["git", "fetch", "origin", default_branch],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=30.0,
            check=False,
        )
        if fetch_res.returncode != 0:
            return False

        checkout_res = subprocess.run(
            ["git", "checkout", "-B", default_branch, f"origin/{default_branch}"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            timeout=10.0,
            check=False,
        )
        return checkout_res.returncode == 0
    except Exception:
        return False


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
        log_msg(
            "Update check is disabled in config/settings.py (CHECK_FOR_UPDATES_ON_STARTUP = False)."
        )
        return

    mode_str = str(mode).lower() if not force else "commits"
    headers = {
        "User-Agent": "SL5-Aura-Service-Update-Checker",
        "Accept": "application/vnd.github.v3+json",
    }

    if not force and (os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS")):
        log_msg("Update check skipped: running in CI environment.")
        return

    verify_and_repair_languagetool(logger)

    try:
        if mode_str in ["releases", "stable"]:
            url = "https://api.github.com/repos/sl5net/SL5-aura-service/releases/latest"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    latest_tag = data.get("tag_name", "")
                    if latest_tag:
                        log_msg(
                            f"Release update available: {latest_tag}. Run update script to upgrade."
                        )
        else:
            from scripts.py.func.config.dynamic_settings import settings

            if getattr(settings, "DEV_MODE", False):
                log_msg("Update check skipped: DEV_MODE is enabled.")
                return


            if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
                log_msg("Git repository not found. Initializing git tracking...")
                update_branch = getattr(settings, "AURA_UPDATE_BRANCH", "master")
                remote_url = getattr(settings, "AURA_REMOTE_URL", "https://github.com/sl5net/SL5-aura-service.git")
                if ensure_git_repo(REPO_DIR, default_branch=update_branch, remote_url=remote_url):
                    log_msg("Git repository initialized successfully.")
                else:
                    log_msg("Failed to initialize git repository for updates.", is_error=True)
                    return False, "Failed to initialize git repository"

            current_branch = get_current_branch(REPO_DIR)
            
            
            if not current_branch:
                return (
                    False,
                    "Cannot determine git branch; skipping reset to prevent data loss",
                )

            local_sha = get_local_commit_sha()
            url = f"https://api.github.com/repos/sl5net/SL5-aura-service/commits/{current_branch}"
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    remote_sha = data.get("sha", "")
                    commit_msg = (
                        data.get("commit", {}).get("message", "").split("\n")[0]
                    )

                    if (
                        local_sha
                        and remote_sha
                        and not remote_sha.startswith(local_sha)
                    ):
                        log_msg(
                            f"New commit found on origin/master ({remote_sha[:7]} vs local {local_sha[:7]}). Applying forced update…"
                        )

                        # Execute forced update (overwriting dirty files)
                        success, result_msg = force_update_to_remote()
                        if success:
                            log_msg(
                                f"Update successfully applied: pulled commit {remote_sha[:7]} ('{commit_msg}')."
                            )
                        else:
                            log_msg(f"Update failed: {result_msg}", is_error=True)
                    else:
                        log_msg(
                            f"Aura is up to date ({local_sha[:7] if local_sha else 'unknown'})."
                        )

    except Exception as e:
        log_msg(f"Update check failed: {e}", is_error=True)


def verify_and_repair_languagetool(logger=None, repo_dir=REPO_DIR):
    """Verifies LanguageTool-6.6 is completely installed and repairs it via
    the shared download/extract helper if the completeness marker is missing.
    A broken LanguageTool (unlike a missing Vosk model) is easy to miss
    during normal use, so this runs on every startup."""

    def log_msg(msg, is_error=False):
        if logger:
            logger.error(msg) if is_error else logger.info(msg)
        else:
            prefix = "[ERROR]" if is_error else "[INFO]"
            print(f"{prefix} {msg}")

    # LanguageTool-6.6/languagetool-server.jar

    marker = os.path.join(repo_dir, "LanguageTool-6.6", "languagetool-server.jar")
    if os.path.isfile(marker):
        return

    log_msg("LanguageTool installation incomplete or missing. Attempting repair...")

    helper_script = os.path.join(
        repo_dir, "setup", "helpers", "linux_mac", "download_and_extract_helper.sh"
    )
    env = os.environ.copy()
    env["SL5NET_AURA_PROJECT_ROOT"] = repo_dir
    env["EXCLUDE_LANGUAGES"] = "all"  # skip Vosk models; LanguageTool/lid.176 are mandatory

    try:
        result = subprocess.run(
            ["bash", "-c", f'source "{helper_script}"'],
            cwd=repo_dir,
            env=env,
            capture_output=True,
            text=True,
            timeout=300.0,
        )
    except Exception as e:
        log_msg(f"LanguageTool repair failed to run: {e}", is_error=True)
        return

    if os.path.isfile(marker):
        log_msg("LanguageTool repair successful.")
    else:
        log_msg(
            f"LanguageTool repair failed (helper exit {result.returncode}): "
            f"{result.stderr.strip()[-500:]}",
            is_error=True,
        )


if __name__ == "__main__":
    print("=== Starting manual update check (forced) ===")
    check_for_updates(force=True)
