# file: scripts/py/func/checks/integrity_checker.py
# integrity_checker.py

import os
import sys
from .integrity_rules import INTEGRITY_CHECKS

def check_code_integrity(project_root, logger):
    """
    Checks files for the presence of critical code fragments defined in integrity_rules.py.
    If a fragment is missing, logs a fatal error and exits the program.
    """
    logger.info("DEV_MODE: Running code integrity check...")
    failed_checks = 0

    for file_path, fragments in INTEGRITY_CHECKS.items():
        full_path = os.path.join(project_root, file_path)

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            for fragment in fragments:
                if fragment not in content:
                    logger.fatal("-" * 60)
                    logger.fatal(f"FATAL INTEGRITY CHECK FAILED!")
                    logger.fatal(f"  File: {file_path}")
                    logger.fatal(f"❌ 🛑🛑🛑 Missing Fragment: '{fragment}'")
                    logger.fatal("  This part of the code is critical and must not be changed.")
                    logger.fatal("-" * 60)
                    failed_checks += 1

        except FileNotFoundError:
            logger.fatal(f"FATAL INTEGRITY CHECK: File not found at '{full_path}'")
            failed_checks += 1

    for root, dirs, files in os.walk(project_root):

        if ".git" in dirs: dirs.remove(".git")
        if "__pycache__" in dirs: dirs.remove("__pycache__")
        if "venv" in dirs: dirs.remove("venv")

        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)

                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    for line_num, line in enumerate(lines, 1):
                        # Wir prüfen jede Zeile gegen die verbotenen Anfänge
                        for unsafe_start in UNSAFE_LINE_STARTS:
                            # startswith prüft exakt den Anfang (Spalte 0)
                            if line.startswith(unsafe_start):
                                logger.fatal("-" * 60)
                                logger.fatal(f"FATAL SECURITY CHECK FAILED!")
                                logger.fatal(f"  File: {full_path}:{line_num}")
                                logger.fatal(f"❌ Unsafe Import detected at start of line: '{unsafe_start.strip()}...'")
                                logger.fatal("  Global settings imports MUST be inside a try-except block (indented).")
                                logger.fatal("-" * 60)
                                failed_checks += 1
                                sys.exit(1)

                except Exception as e:
                    # Falls eine Datei nicht lesbar ist (z.B. falsches Encoding), warnen wir nur kurz
                    logger.warning(f"Could not scan file {full_path}: {e}")


    if failed_checks > 0:
        logger.fatal(f"Aborting due to {failed_checks} failed integrity check(s).")
        sys.exit(1)
    else:
        logger.info("✅ OK: All code integrity checks passed.")
