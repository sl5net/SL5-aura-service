# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# scripts/py/func/checks/check_installer_sizes.py

# import os
from pathlib import Path
import sys

# ANSI color codes for better output
COLOR_GREEN = '\033[92m'
COLOR_RED = '\033[91m'
COLOR_RESET = '\033[0m'

def check_file_sizes(base_dir: Path, primary_group: list[str], secondary_group: list[str], primary_tolerance: float, secondary_tolerance: float) -> bool:
    """
    Checks the consistency of file sizes for different groups of installers.
    """
    all_ok = True
    primary_sizes = {}

    for filename in primary_group:
        try:
            size = (base_dir / filename).stat().st_size
            primary_sizes[filename] = size
        except FileNotFoundError:
            print(f"{COLOR_RED}ERROR: Primary file not found: {filename}{COLOR_RESET}")
            all_ok = False

    if not primary_sizes:
        print(f"{COLOR_RED}ERROR: No primary files found to compare.{COLOR_RESET}")
        return False

    if not all_ok:
        return False

    avg_primary_size = sum(primary_sizes.values()) / len(primary_sizes)
    print(f"Primary group average size: {avg_primary_size:.0f} bytes")
    print("------------------------------------------")

    for filename, size in primary_sizes.items():
        diff = abs(size - avg_primary_size)
        percent_diff = (diff / avg_primary_size) * 100 if avg_primary_size > 0 else 0

        if percent_diff > primary_tolerance:
            print(f"{COLOR_RED}WARNING:{COLOR_RESET} '{filename}' ({size} bytes) differs by {percent_diff:.1f}% (>{primary_tolerance}%)")
            all_ok = False
        else:
            print(f"{COLOR_GREEN}OK:{COLOR_RESET}      '{filename}' ({size} bytes) is within tolerance.")

    print("------------------------------------------")

    for filename in secondary_group:
        try:
            size = (base_dir / filename).stat().st_size
            diff = abs(size - avg_primary_size)
            percent_diff = (diff / avg_primary_size) * 100 if avg_primary_size > 0 else 0

            if percent_diff > secondary_tolerance:
                print(f"{COLOR_RED}WARNING:{COLOR_RESET} '{filename}' ({size} bytes) differs by {percent_diff:.1f}% (>{secondary_tolerance}%)")
                all_ok = False
            else:
                print(f"{COLOR_GREEN}OK:{COLOR_RESET}      '{filename}' ({size} bytes) is within tolerance.")
        except FileNotFoundError:
            print(f"{COLOR_RED}ERROR: Secondary file not found: {filename}{COLOR_RESET}")
            all_ok = False

    return all_ok

def check_installer_sizes():
    """Defines the configuration and runs the check."""
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
    SETUP_DIR = PROJECT_ROOT / "setup"

    primary_files = ["macos_setup.sh", "ubuntu_setup.sh", "manjaro_arch_setup.sh",'suse_setup.sh']
    secondary_files = ["windows11_setup.ps1"]
    primary_diff_percent = 1.3
    secondary_diff_percent = 110

    print(f"Checking installer sizes in: {SETUP_DIR}")

    success = check_file_sizes(
        base_dir=SETUP_DIR,
        primary_group=primary_files,
        secondary_group=secondary_files,
        primary_tolerance=primary_diff_percent,
        secondary_tolerance=secondary_diff_percent
    )

    print("------------------------------------------")
    if success:
        print(f"{COLOR_GREEN}All installer sizes are consistent.{COLOR_RESET}")
        return 0
    else:
        print(f"{COLOR_RED}Installer size consistency check failed.{COLOR_RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(check_installer_sizes())
