# File: scripts/py/func/main.py
import importlib
import config.settings as settings

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

    global observer

    last_trigger_time = 0
    DEBOUNCE_SECONDS = 0.1  # 100ms cooldown

    active_threads = []


    # Unpack config dictionary
    script_dir = config["SCRIPT_DIR"]
    TMP_DIR = config["TMP_DIR"]

    trigger_file_path = config["TRIGGER_FILE"]
    heartbeat_file = config["HEARTBEAT_FILE"]
    critical_threshold_mb = config["CRITICAL_THRESHOLD_MB"]
    project_root = config["PROJECT_ROOT"]

    SILENCE_TIMEOUT = config["SILENCE_TIMEOUT"]

    PRELOAD_MODELS = config["PRELOAD_MODELS"]
    CRITICAL_THRESHOLD_MB = config["CRITICAL_THRESHOLD_MB"]


    if not SILENCE_TIMEOUT:
        logger.error(f"SILENCE_TIMEOUT: '{SILENCE_TIMEOUT}' ")

    # --- START: ONE-TIME PRIORITIZATION ON STARTUP ---
    last_used_file = project_root / "config/model_name_lastused.txt"



    try:
        if last_used_file.exists():
            last_used_model_name = last_used_file.read_text().strip()
            key_to_prioritize = None

            # Find the corresponding short key (e.g., 'de') for the last used model name
            for key in loaded_models.keys():
                if f"-{key}-" in last_used_model_name:
                    key_to_prioritize = key
                    break

            if key_to_prioritize:
                logger.info("Performing initial model prioritization on startup.")
                prioritize_model(logger, loaded_models, key_to_prioritize)

    except Exception as e:
        logger.error(f"Could not perform initial model prioritization: {e}")
    # --- END: ONE-TIME PRIORITIZATION ON STARTUP ---

    try:
        # --- UNIFIED LOGIC FOR ALL OS ---
        logger.info(f"Starting watchdog observer for triggers on '{trigger_file_path.name}'.")
        trigger_event = threading.Event()


        class TriggerEventHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                if event.src_path == str(trigger_file_path.resolve()):
                    trigger_event.set()


        observer = Observer()
        observer.schedule(TriggerEventHandler(), path=str(TMP_DIR), recursive=False)
        observer.start()

        while True:
            # Wait efficiently for a trigger, with a timeout for maintenance
            trigger_event.wait(timeout=5.0)

            # This block runs every 5s OR when a trigger happens
            Path(heartbeat_file).write_text(str(int(time.time())))
            active_threads = [t for t in active_threads if t.is_alive()]
            manage_models(logger, loaded_models, PRELOAD_MODELS, CRITICAL_THRESHOLD_MB, script_dir)

            if trigger_event.is_set():
                current_time = time.time()
                trigger_event.clear()  # Reset for the next trigger

                if (current_time - last_trigger_time) > DEBOUNCE_SECONDS:
                    last_trigger_time = current_time  # Update time only on success
                    handle_trigger(logger, loaded_models, active_threads, suspicious_events, project_root, TMP_DIR,
                                   recording_time, active_lt_url)
                else:
                    logger.info("Ignoring trigger action (debouncing).")



    except KeyboardInterrupt:
        logger.info("\nService interrupted by user.")
    except Exception as e:
        logger.error("FATAL ERROR in main loop:", exc_info=True)
    finally:
        observer.stop()
        observer.join()

        logger.info("Waiting for all background threads to finish...")
        for t in active_threads:
            t.join()
