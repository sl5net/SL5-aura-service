# scripts/py/func/checks/check_path_length.py

import os
import sys
from pathlib import Path

# Windows API limit
MAX_PATH_LIMIT = 260

def get_cache_file(LOCK_DIR):
    return LOCK_DIR / "path_check.passed"


def run_path_check(project_root, LOCK_DIR ,  force=False):
    """
    Checks if the installation path is too long for Windows.
    Uses a cache file to avoid re-scanning on every start.
    """
    current_root_str = project_root
    if sys.platform != 'win32':
        return True

    cache_file = get_cache_file(LOCK_DIR)

    # 1. Check Cache (Performance Optimization)
    if not force and cache_file.exists():
        try:
            cached_path = cache_file.read_text("utf-8").strip()
            if cached_path == current_root_str:
                # Path hasn't changed since last success -> Skip check
                return True
        except Exception:
            # Ignore read errors, just run the check
            pass


    print(f"[CHECK] Verifying path length for root: {project_root}")

    # Ensure project_root is a Path object
    project_root = Path(project_root).resolve()

    longest_relative_path = ""
    max_internal_length = 0

    # 1. Scan for the deepest file
    for root, dirs, files in os.walk(project_root):
        if ".git" in dirs:
            dirs.remove(".git")

        for file in files:
            try:
                abs_path = os.path.join(root, file)
                # Calculate relative path length
                rel_path = os.path.relpath(abs_path, project_root)
                current_len = len(rel_path)

                if current_len > max_internal_length:
                    max_internal_length = current_len
                    longest_relative_path = rel_path
            except Exception:
                continue

    # 2. Calculate totals
    current_root_len = len(str(project_root))
    # +1 for the backslash separator
    total_len = current_root_len + 1 + max_internal_length

    headroom = MAX_PATH_LIMIT - total_len

    # 3. Evaluate
    if total_len >= headroom:
        print("❌ -----------------------------------------------------------")
        print("❌ CRITICAL ERROR: INSTALLATION PATH IS TOO LONG")
        print(f"❌ Windows Limit: {MAX_PATH_LIMIT} characters")
        print(f"❌ Your Path:     {total_len} characters")
        print("❌")
        print(f"❌ The file causing the overflow is inside:")
        print(f"❌ ...\\{longest_relative_path}")
        print("❌")
        print("❌ SOLUTION: Please move the entire folder to a shorter path.")
        print("❌ Example: Move it to 'C:\\SL5'")
        print("❌ -----------------------------------------------------------")
        return False

    elif total_len > 240:
        print(f"⚠️ WARNING: Path length is very close to limit ({total_len}/{MAX_PATH_LIMIT}).")
        print("   Consider moving to a shorter path just to be safe.")
        return True

    else:
        # Path is safe
        # print(f"✅ Path length check passed ({total_len}/{MAX_PATH_LIMIT}).")
        return True

# Helper to run it standalone for testing
if __name__ == "__main__":
    # Assume we are in scripts/py/func/checks/
    # Go up 4 levels to find project root: checks -> func -> py -> scripts -> ROOT
    root_guess = Path(__file__).parents[4]
    run_path_check(root_guess)
