# File: scripts/py/func/main.py
import platform, subprocess, threading, time, sys
from pathlib import Path

from .handle_trigger import handle_trigger
from .check_memory_critical import check_memory_critical
from .notify import notify

from config.settings import SAMPLE_RATE, SUSPICIOUS_TIME_WINDOW, SUSPICIOUS_THRESHOLD, \
    PRE_RECORDING_TIMEOUT, SILENCE_TIMEOUT


def main(logger, loaded_models, config, suspicious_events, TMP_DIR, recording_time, active_lt_url):
    active_threads = []

    # Unpack config dictionary
    trigger_file = config["TRIGGER_FILE"]
    heartbeat_file = config["HEARTBEAT_FILE"]
    critical_threshold_mb = config["CRITICAL_THRESHOLD_MB"]
    project_root = config["PROJECT_ROOT"]

    if not SILENCE_TIMEOUT:
        logger.error(f"SILENCE_TIMEOUT: '{SILENCE_TIMEOUT}' ")



    # --- Main Loop ---
    try:
        if platform.system() == "Linux":
            logger.info(f"Main loop started. Waiting for triggers on '{trigger_file.name}'.")
            while True:
                Path(heartbeat_file).write_text(str(int(time.time())))
                active_threads = [t for t in active_threads if t.is_alive()]

                is_critical, avail_mb = check_memory_critical(critical_threshold_mb)
                if is_critical:
                    logger.critical(f"Low memory ({avail_mb:.0f}MB). Shutting down.")
                    sys.exit(1)

                try:
                  proc = subprocess.run(
                        ['inotifywait', '-q', '-e', 'create,close_write', '--format', '%f', str(TMP_DIR)],
                        capture_output=True, text=True, timeout=5
                    )
                  if proc.stdout.strip() == trigger_file.name:
                        trigger_file.unlink(missing_ok=True)
                        handle_trigger(
                            logger, loaded_models, active_threads, suspicious_events,
                            project_root, TMP_DIR, recording_time, active_lt_url
                        )
                except subprocess.TimeoutExpired:
                    pass

        else:  # Polling (Windows, macOS)
            logger.info("Listening for triggers via file polling...")
            while True:


                is_critical, avail_mb = check_memory_critical(critical_threshold_mb)
                if is_critical:
                    logger.critical(f"Low memory ({avail_mb:.0f}MB). Shutting down.")
                    sys.exit(1)

                Path(heartbeat_file).write_text(str(int(time.time())))

                if trigger_file.exists():
                    logger.info("Trigger file detected by polling.")
                    trigger_file.unlink(missing_ok=True)
                    handle_trigger(
                        logger, loaded_models, active_threads, suspicious_events,
                        project_root, TMP_DIR, recording_time, active_lt_url,
                        config
                    )

                time.sleep(0.2)


    except KeyboardInterrupt:
        logger.info("\nService interrupted by user.")
    except Exception as e:
        logger.error("FATAL ERROR in main loop:", exc_info=True)
    finally:
        logger.info("Waiting for all background threads to finish...")
        for t in active_threads:
            t.join()

#
