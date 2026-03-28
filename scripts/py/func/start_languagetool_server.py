# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# file: scripts/py/func/start_languagetool_server.py

from pathlib import Path
import subprocess
import requests
import time
import sys
import importlib
from .config.dynamic_settings import DynamicSettings

import os
import psutil  # pip install psutil

settings = DynamicSettings()


# Sentinel object to indicate LT was already running.
# The sentinel has the minimal methods (poll, terminate) to be safely passed
# to atexit.register and handled by stop_languagetool_server.
# scripts/py/func/start_languagetool_server.py:15
LT_ALREADY_RUNNING_SENTINEL = type('LTAlreadyRunning', (object,), {
    'pid': -1,
    'poll': lambda self: None,
    'terminate': lambda self: None
})()

# /home/seeh/projects/py/STT/scripts/py/func/start_languagetool_server.py
def _update_settings_file(logger, java_path):
    config_path = Path('config/settings.py')
    new_lines = []
    java_path_found = False

    config_path.parent.mkdir(exist_ok=True)

    if config_path.is_file():
        with open(config_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    else:
        lines = ['# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY\n']

    # scripts/py/func/start_languagetool_server.py:36
    new_java_line = f'JAVA_EXECUTABLE_PATH = r"{java_path}"\n'

    for line in lines:
        if line.strip().startswith('JAVA_EXECUTABLE_PATH'):
            new_lines.append(new_java_line)
            java_path_found = True
        else:
            new_lines.append(line)

    if not java_path_found:
        if new_lines and new_lines[-1] and not new_lines[-1].endswith('\n'):
            new_lines.append('\n')
        new_lines.append('\n# Auto-detected Java path\n')
        new_lines.append(new_java_line)

    with open(config_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    if settings.DEV_MODE:
        logger.info(f"Settings file updated. Java path set to: {java_path}")

def _is_lt_server_responsive(url, timeout=1):
    """Checks if the LanguageTool server at the given URL is responsive."""
    try:
        # Check against a known lightweight endpoint
        # response = requests.get(f"{url}/v2/languages", timeout=timeout)
        response = requests.get(f"{url}/v2/languages", timeout=timeout, allow_redirects=True)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        # logger.debug(f"LT Check failed: {e}")
        print(f"LanguageTool(LT) Check failed: {e}")
        return False
    except Exception as e2:
        # logger.debug(f"LT Check failed: {e}")
        print(f"LanguageTool(LT) Check failed: {e2}")
        return False

    # backup
    # return {
    #     "xms": f"-Xms{xms_gb}G",
    #     "xmx": f"-Xmx{xmx_gb}G",
    #     "threads": str(threads),
    # }
    #



def get_languagetool_jvm_args(for_self_test=False):
    cpu_cores = os.cpu_count() or 4
    ram_gb = psutil.virtual_memory().total / (1024 ** 3)

    if for_self_test:
        threads = cpu_cores * 2          # kein Cap bei 16
        xms_mb = max(512, int(ram_gb * 0.1 * 1024))
        xmx_mb = max(2048, int(ram_gb * 0.6 * 1024))  # 60% statt 35%
    else:

        # Threads: 2× Kerne, min 2, max 16
        threads = max(2, min(16, cpu_cores * 2))

        # Xms: klein halten → JVM startet schlank, GC hat Luft zum Atmen
        # 5% RAM, min 512MB, max 2GB
        xms_mb = max(512, min(2048, int(ram_gb * 0.05 * 1024)))

        # Xmx: genug für Test-Runs
        # 35% RAM, min 1GB, max 16GB
        xmx_mb = max(1024, min(16384, int(ram_gb * 0.35 * 1024)))

    return {
        "xms": f"-Xms{xms_mb}m",
        "xmx": f"-Xmx{xmx_mb}m",
        "threads": str(threads),
        # G1GC: gibt RAM automatisch zurück nach Test-Runs (kein Neustart nötig)
        "gc_flags": [
            "-XX:+UseG1GC",
            "-XX:MinHeapFreeRatio=10",   # unter 10% frei → GC expandiert
            "-XX:MaxHeapFreeRatio=30",   # über 30% frei → JVM gibt RAM zurück
            "-XX:MaxGCPauseMillis=200",  # weichere GC-Pausen → ruhigere Lüfter
            "-XX:G1HeapRegionSize=16m",
        ],
    }


def start_languagetool_server(logger, languagetool_jar_path, base_url, for_self_test=False):
    # 1. Port extrahieren und URL säubern
    # Falls base_url nur eine Zahl ist, mach eine URL draus
    if base_url.isdigit():
        port = base_url
    else:
        port = base_url.split(':')[-1].split('/')[0]

    full_base_url = f"http://127.0.0.1:{port}"


    # Wir prüfen /v2/languages (Standard) ODER einfach nur /v2
    if _is_lt_server_responsive(full_base_url, timeout=0.5):  # Timeout etwas höher
        logger.info(f"✅ LanguageTool Server is ALREADY online at {full_base_url}. Skipping startup.")
        return LT_ALREADY_RUNNING_SENTINEL
    else:
        logger.info(f"x Failed: Checking for existing LanguageTool on {full_base_url}...")

    # 2. Check Java path (existing logic)
    try:
        import config.settings
        importlib.reload(config.settings)
        java_executable_path = getattr(config.settings, 'JAVA_EXECUTABLE_PATH', None)
    except (ImportError, AttributeError):
        java_executable_path = None

    if not java_executable_path or not Path(java_executable_path).exists():
        logger.info("Java executable path is not set or invalid. Auto-detecting...")
        try:
            command = ['where', 'java'] if sys.platform == "win32" else ['which', 'java']
            result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
            detected_path = result.stdout.strip().split('\n')[0].strip()

            _update_settings_file(logger, detected_path)
            java_executable_path = detected_path

        except (subprocess.CalledProcessError, FileNotFoundError, IndexError) as e:
            logger.critical(f"CRITICAL: Failed to auto-detect Java. Please install it. Error: {e}")
            return False

    if not java_executable_path:
        logger.critical("CRITICAL: Java path could not be determined. Aborting.")
        return False

    if not Path(languagetool_jar_path).exists():
        logger.critical(f"LanguageTool JAR not found at {languagetool_jar_path}")
        return False

    # 3. Start the process (existing logic)
    if settings.DEV_MODE:
        logger.info(f"Starting LanguageTool Server using Java from: {java_executable_path}")

    try:
        # command_strOld = f'"{java_executable_path}" -jar "{languagetool_jar_path}" --port {port} --allow-origin "*"'

        # scripts/py/func/start_languagetool_server.py:121

        args = get_languagetool_jvm_args(for_self_test=for_self_test)

        command_str = [
            java_executable_path,
            args["xms"],
            args["xmx"],
            *args["gc_flags"],
            "-jar", str(languagetool_jar_path),
            "--port", str(port),
            "--threads", args["threads"],
            "--address", '127.0.0.1',
            "--allow-origin", "*"
        ]

        # command_str = [
        #     java_executable_path,
        #     "-Xms1G",  # Optional: Startet direkt mit 1GB (beschleunigt Warmup)
        #     "-Xmx4G",  # Maximal 4GB RAM
        #     "-jar", str(languagetool_jar_path),
        #     "--port", str(port),
        #     "--threads", "16",  # Muss ein String sein!
        #     "--address", '127.0.0.1',
        #     "--allow-origin", "*"
        # ]

        # FIX: Windows can get with PIPE Deadlocks
        # Optional: Use File when want read Logs
        log_dir = Path("log")
        log_dir.mkdir(exist_ok=True)
        log_file = open(log_dir / "languagetool_server.log", "w", encoding="utf-8")
        if settings.DEV_MODE:
            logger.info(f"Executing command via shell: {command_str}")
        languagetool_process = subprocess.Popen(command_str,
                                                stdout=log_file,
                                                stderr=log_file,
                                                text=True,
                                                encoding='utf-8', shell=False)
    except Exception as e:
        logger.fatal(f"x Failed to start LanguageTool Server process with shell=True: {e}")
        return False

    # stdout=subprocess.PIPE,
    # stderr=subprocess.PIPE,

    # scripts/py/func/start_languagetool_server.py:137
    # 4. Wait for responsiveness (existing logic)
    if settings.DEV_MODE:
        logger.info("Waiting for LanguageTool Server to be responsive...")
    for _ in range(40):
        log_file.flush()
        if _is_lt_server_responsive(full_base_url, timeout=1.5):
            if settings.DEV_MODE:
                logger.info("LanguageTool Server is online.")
            return languagetool_process

        if languagetool_process.poll() is not None:
            logger.fatal("LanguageTool process terminated unexpectedly.")
            _, stderr = languagetool_process.communicate()
            if stderr:
                logger.error(f"LanguageTool STDERR:\n{stderr}")
            return False
        time.sleep(1.0)

    logger.critical("LanguageTool Server did not become responsive.")
    from .stop_languagetool_server import stop_languagetool_server
    stop_languagetool_server(logger, languagetool_process)
    return False
