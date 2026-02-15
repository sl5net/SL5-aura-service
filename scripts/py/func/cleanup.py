# file: scripts/py/func/cleanup.py
def cleanup(logger, files_to_remove):
    # file: scripts/py/func/cleanup.py
    import sys
    import traceback
    import os

    # Check if an exception triggered this
    exc_type, exc_value, exc_traceback = sys.exc_info()

    if exc_type:
        logger.error("❌ AURA CRASHED WITH EXCEPTION:")
        logger.error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    else:
        # Check if it was a signal or just a regular exit
        logger.info(f"ℹ️ Aura reached a clean exit (PID: {os.getpid()}). No active Exception.")

        # --- Ghost Plugin / Deactivation Hint ---
        logger.info("❓ UNEXPECTED SHUTDOWN? Check for 'ghost' plugins!")
        logger.info("💡 PRO-TIP: Renaming 'file.py' to 'file OFF.py' does NOT deactivate it.")
        logger.info("💡 The engine still loads any file ending in '.py'.")
        logger.info("💡 To truly deactivate a plugin, change the extension to '.py_bak' or move it out of the folder.")
        # ----------------------------------------------


    # Final location check
    logger.info("🏁 Cleanup Stack-Trace (where the process ended):\n" + "".join(traceback.format_stack()))


    for f in files_to_remove:
        f.unlink(missing_ok=True)
    logger.info("✅ Cleanup complete.")


