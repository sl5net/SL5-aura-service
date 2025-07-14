# scripts/setup_validator.py
#
# This script contains functions to validate the application's environment.
import os
import sys


def validate_setup(project_root):
    """
    Verifies that essential setup steps have been completed.
    If a check fails, it prints an error and exits the program.

    Args:
        project_root (str): The absolute path to the project's root directory.
    """
    print("INFO: Running setup validation...")

    # --- Check 1: Existence of the 'log' directory ---
    log_dir = os.path.join(project_root, 'log')
    if not os.path.isdir(log_dir):
        # This error is printed to stderr, which is standard for errors.
        print(
            "\nFATAL: Setup validation failed. The 'log' directory is missing.",
            file=sys.stderr
        )
        print(
            "       Please run the appropriate script from the 'setup/' directory.",
            file=sys.stderr
        )
        sys.exit(1) # Exit with an error code

    # --- Add future checks here ---
    # Example: Check for a specific config file
    # config_file = os.path.join(project_root, 'config', 'model_name.txt')
    # if not os.path.isfile(config_file):
    #     print("FATAL: Config file 'model_name.txt' is missing.", file=sys.stderr)
    #     sys.exit(1)

    print("INFO: Setup validation successful.")

