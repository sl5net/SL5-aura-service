# file: scripts/py/func/cleanup.py
def cleanup(logger, files_to_remove):
    logger.info("Cleaning up files...")
    for f in files_to_remove:
        f.unlink(missing_ok=True)
    logger.info("Cleanup complete.")


