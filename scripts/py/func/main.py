# File: scripts/py/func/main.py
import platform, subprocess, threading, time, sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

from .handle_trigger import handle_trigger
from .check_memory_critical import check_memory_critical
from .notify import notify
from .prioritize_model import prioritize_model
from .model_manager import manage_models


def main(logger, loaded_models, config, suspicious_events, recording_time, active_lt_url):
    active_threads = []

    # Unpack config dictionary
    script_dir = config["SCRIPT_DIR"]
    TMP_DIR = config["TMP_DIR"]
    trigger_file = config["TRIGGER_FILE"]
    heartbeat_file = config["HEARTBEAT_FILE"]
    project_root = config["PROJECT_ROOT"]
    PRELOAD_MODELS = config["PRELOAD_MODELS"]
    CRITICAL_THRESHOLD_MB = config["CRITICAL_THRESHOLD_MB"]

    # --- START: ONE-TIME PRIORITIZATION ON STARTUP ---
    last_used_file = project_root / "config/model_name_lastused.txt"
    try:
        if last_used_file.exists():
            last_used_model_name = last_used_file.read_text().strip()
            key_to_prioritize = None
            for key in loaded_models.keys():
                if f"-{key}-" in last_used_model_name:
                    key_to_prioritize = key
                    break
            if key_to_prioritize:
                logger.info("Performing initial model prioritization on startup.")
                prioritize_model(logger, loaded_models, key_to_prioritize)
    except Exception as e:
        logger.error(f"Could not perform initial model prioritization: {e}")

    # --- STATE MANAGEMENT ---
    recording_thread = None
    stop_recording_event = threading.Event()

    def process_trigger():
        nonlocal recording_thread
        if recording_thread and recording_thread.is_alive():
            logger.info("Recording active. Sending stop signal.")
            stop_recording_event.set()
        else:
            logger.info("Starting new recording.")
            stop_recording_event.clear()
            recording_thread = threading.Thread(
                target=handle_trigger,
                args=(
                    logger, loaded_models, active_threads, suspicious_events,
                    project_root, TMP_DIR, recording_time, active_lt_url,
                    stop_recording_event
                )
            )
            recording_thread.start()

    # --- Main Loop ---
    try:
        if platform.system() == "Linux":
            logger.info(f"Main loop started. Waiting for triggers on '{trigger_file.name}'.")
            while True:
                Path(heartbeat_file).write_text(str(int(time.time())))
                active_threads = [t for t in active_threads if t.is_alive()]
                manage_models(logger, loaded_models, PRELOAD_MODELS, CRITICAL_THRESHOLD_MB, script_dir)

                if recording_thread and not recording_thread.is_alive():
                    logger.info("Recording thread has finished. Ready for a new trigger.")
                    recording_thread = None

                try:
                    proc = subprocess.run(
                        ['inotifywait', '-q', '-e', 'create,close_write', '--format', '%f', str(TMP_DIR)],
                        capture_output=True, text=True, timeout=5
                    )
                    if proc.stdout.strip() == trigger_file.name:
                        trigger_file.unlink(missing_ok=True)
                        process_trigger()
                except subprocess.TimeoutExpired:
                    pass

        else:  # Windows/macOS
            observer = Observer()

            class TriggerEventHandler(FileSystemEventHandler):
                def on_created(self, event):
                    if event.src_path == str(trigger_file.resolve()):
                        logger.info("Trigger file detected by filesystem event.")
                        trigger_event.set()

            trigger_event = threading.Event()
            observer.schedule(TriggerEventHandler(), path=str(TMP_DIR), recursive=False)
            observer.start()
            logger.info(f"Event-driven listener started for non-Linux OS. Watching for '{trigger_file.name}'.")

            while True:
                trigger_event.wait(timeout=5.0)
                Path(heartbeat_file).write_text(str(int(time.time())))
                manage_models(logger, loaded_models, PRELOAD_MODELS, CRITICAL_THRESHOLD_MB, script_dir)

                if recording_thread and not recording_thread.is_alive():
                    logger.info("Recording thread has finished. Ready for a new trigger.")
                    recording_thread = None

                if trigger_event.is_set():
                    trigger_event.clear()
                    trigger_file.unlink(missing_ok=True)
                    process_trigger()

    except KeyboardInterrupt:
        logger.info("\nService interrupted by user.")
    except Exception as e:
        logger.error("FATAL ERROR in main loop:", exc_info=True)
    finally:
        logger.info("Waiting for all background threads to finish...")
        for t in active_threads:
            t.join()