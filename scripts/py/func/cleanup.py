# file: func/cleanup.py
def cleanup(logger, stop_lt_server_func, files_to_remove):
    logger.info("Cleaning up files...")
    # stop_lt_server_func()
    for f in files_to_remove:
        f.unlink(missing_ok=True)
    logger.info("Cleanup complete.")


