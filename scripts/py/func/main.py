# File: scripts/py/func/main
import platform
import subprocess
import threading
import time
from pickle import GLOBAL

from config.settings import SUSPICIOUS_THRESHOLD, SUSPICIOUS_TIME_WINDOW

from .cleanup import cleanup
from .check_memory_critical import check_memory_critical
from .transcribe_audio_with_feedback import transcribe_audio_with_feedback
from .process_text_in_background import process_text_in_background
from .notify import notify

import vosk

SAMPLE_RATE = 16000
SILENCE_TIMEOUT = 0.4



from scripts.py.func.notify import notify
from scripts.py.func.process_text_in_background import process_text_in_background
from scripts.py.func.check_memory_critical import check_memory_critical
from scripts.py.func.transcribe_audio_with_feedback import transcribe_audio_with_feedback

from scripts.py.func import cleanup
from pathlib import Path

"""
    config = {
        "TMP_DIR": TMP_DIR,
        "HEARTBEAT_FILE": HEARTBEAT_FILE,
        "PIDFILE": PIDFILE,
        "TRIGGER_FILE": TRIGGER_FILE
        "LT_LANGUAGE" = LT_LANGUAGE
        "CRITICAL_THRESHOLD_MB" = CRITICAL_THRESHOLD_MB   
    }

"""

def main(logger, LT_LANGUAGE, model, config, suspicious_events, TMP_DIR, recording_time,active_lt_url):
    active_threads = []

    tmp_dir = config["TMP_DIR"]
    heartbeat_file = config["HEARTBEAT_FILE"]
    pidfile = config["PIDFILE"]
    trigger_file = config["TRIGGER_FILE"]
    lt_language = config["LT_LANGUAGE"]
    critical_threshold_mb = config["CRITICAL_THRESHOLD_MB"]

    try:
        if platform.system() == "Linux":
            logger.info(f"Listening for triggers via inotifywait on '{tmp_dir}'. Waiting for '{trigger_file.name}'.")
            while True:
                active_threads = [t for t in active_threads if t.is_alive()]
                try:
                    proc = subprocess.run(
                        ['inotifywait', '-q', '-e', 'create,close_write', '--format', '%f', str(tmp_dir)],
                        capture_output=True, text=True, timeout=5
                    )
                    if proc.stdout.strip() == trigger_file.name:
                        logger.info(f"TRIGGER DETECTED via inotifywait! Active threads: {len(active_threads)}")
                        trigger_file.unlink(missing_ok=True)
                        recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
                        raw_text = transcribe_audio_with_feedback(logger, recognizer, lt_language,
                                          SILENCE_TIMEOUT, SAMPLE_RATE)
                        if not raw_text.strip() or len(raw_text.split()) < 1:
                            suspicious_events.append(time.time())
                        now = time.time()
                        suspicious_events = [t for t in suspicious_events if now - t < SUSPICIOUS_TIME_WINDOW]
                        if len(suspicious_events) >= SUSPICIOUS_THRESHOLD:
                            notify(
                                "Tip: Record to short?",
                                "Record is very short. You maybe want set SILENCE_TIMEOUT to 0.8 or 1.0 ?",
                                "normal"
                            )
                            suspicious_events = []
                        if raw_text.strip():
                            thread = threading.Thread(target=process_text_in_background,
                                                      args=(logger,
                                                            LT_LANGUAGE,
                                                            raw_text,
                                                            TMP_DIR,
                                                            recording_time,active_lt_url))
                            thread.start()
                            active_threads.append(thread)
                except subprocess.TimeoutExpired:
                    pass


                is_critical, avail_mb = check_memory_critical(critical_threshold_mb)
                if is_critical:
                    logger.critical(f"Low memory detected ({avail_mb:.0f}MB available). Shutting down.")
                    notify("Vosk: Critical Error", "Low memory detected. Service shutting down.", "critical")
                    sys.exit(1)

                Path(heartbeat_file).write_text(str(int(time.time())))
        else:
            # Polling
            logger.info("Listening for triggers via file polling...")
            while True:
                if trigger_file.exists():
                    pass
                time.sleep(0.2)
                Path(heartbeat_file).write_text(str(int(time.time())))

    except Exception as e:
        logger.error("FATAL ERROR in main loop:", exc_info=True)
    except KeyboardInterrupt:
        logger.info("\nService interrupted by user.")
    finally:

        logger.info("Waiting for all background threads to finish...")
        for t in active_threads:
            t.join()

"""
    logger.info("Waiting for all background threads to finish...")
    for t in active_threads:
        t.join()
    cleanup( HEARTBEAT_FILE, PIDFILE, TRIGGER_FILE)
    stop_lt_server_func()
    notify("Vosk Service", "Service has been shut down.", "normal")
"""
