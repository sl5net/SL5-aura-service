# file: scripts/py/func/checks/integrity_checker.py
# integrity_checker.py

import os
import sys
from .integrity_rules import INTEGRITY_CHECKS, UNSAFE_LINE_STARTS, FORBIDDEN_PATTERNS


def check_code_integrity(project_root, logger):
    """
    Checks files for the presence of critical code fragments defined in integrity_rules.py.
    If a fragment is missing, logs a fatal error and exits the program.
    """
    logger.info("14: DEV_MODE: Running code integrity check...")
    failed_checks = 0

    for file_path, fragments in INTEGRITY_CHECKS.items():
        full_path = os.path.join(project_root, file_path)

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            for fragment in fragments:
                if len(fragment)>0 and fragment not in content:
                    logger.fatal("-" * 60)
                    logger.fatal("FATAL INTEGRITY CHECK FAILED!")
                    logger.fatal(f"  File: {file_path}")
                    logger.fatal(f"❌ 🛑🛑🛑 Missing Fragment: '{fragment}'")
                    logger.fatal(f"Missing Fragment: '{fragment}'")
                    logger.fatal("  This part of the code is critical and must not be changed.")
                    logger.fatal("-" * 60)
                    failed_checks += 1

        except FileNotFoundError:
            logger.fatal(f"35: FATAL INTEGRITY CHECK: File not found at '{full_path}'")
            failed_checks += 1

    for root, dirs, files in os.walk(project_root):

        if ".git" in dirs: dirs.remove(".git")
        if "__pycache__" in dirs: dirs.remove("__pycache__")
        if "venv" in dirs: dirs.remove("venv")

        for file in files:
            if file.endswith(".py") or file.endswith(".bat") or file.endswith(".ps1"):
                full_path = os.path.join(root, file)

                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    for line_num, line in enumerate(lines, 1):
                        # We check every line against the forbidden beginnings
                        for unsafe_start in UNSAFE_LINE_STARTS:
                            # startswith prüft exakt den Anfang (Spalte 0)
                            if line.startswith(unsafe_start):
                                logger.fatal("-" * 60)
                                logger.fatal("FATAL SECURITY CHECK FAILED!")
                                logger.fatal(f"  File: {full_path}:{line_num}")
                                logger.fatal(f"❌ Unsafe Import detected at start of line: '{unsafe_start.strip()}...'")
                                logger.fatal("  Global settings imports MUST be inside a try-except block (indented).")
                                logger.fatal("-" * 60)
                                failed_checks += 1
                                sys.exit(1)

                        if "integrity_rules.py" not in file:
                            for forbidden in FORBIDDEN_PATTERNS:
                                if forbidden in line:
                                    # Exception: We allow it if it is a comment (starts with #)

                                    logger.fatal("-" * 60)
                                    logger.fatal("FATAL SECURITY CHECK FAILED!")
                                    logger.fatal(f"  File: {full_path}:{line_num}")
                                    logger.fatal(f"❌ Forbidden Pattern detected: '{forbidden}'")
                                    logger.fatal("  SOLUTION: Use 'if getattr(settings, \"VARIABLE\", False):' instead!")
                                    logger.fatal("-" * 60)
                                    failed_checks += 1
                                    sys.exit(1)

                except Exception as e:
                    logger.warning(f"Could not scan file {full_path}: {e}")


    if failed_checks > 0:
        logger.fatal(f"Aborting due to {failed_checks} failed integrity check(s).")
        sys.exit(1)
    else:
        logger.info("✅ OK: All code integrity checks passed.")
