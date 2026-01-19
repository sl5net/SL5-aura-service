# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# file: scripts/py/func/start_languagetool_server.py

from pathlib import Path
import subprocess
import requests
import time
import sys
import importlib
from .config.dynamic_settings import settings

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
        response = requests.get(f"{url}/v2/languages", timeout=timeout)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False



def start_languagetool_server(logger, languagetool_jar_path, base_url):
    # 1. EARLY CHECK: Prevent double startup
    port = base_url.split(':')[-1].split('/')[0]
    # full_base_url = f"http://localhost:{port}"
    full_base_url = f"http://127.0.0.1:{port}" # Using 127.0.0.1 explicitly to avoid Windows IPv6 localhost issues

    # scripts/py/func/start_languagetool_server.py:75
    if _is_lt_server_responsive(full_base_url, timeout=0.5):
        logger.info(f"LanguageTool Server is ALREADY online at {full_base_url}. Skipping new startup (RAM optimization).")
        return LT_ALREADY_RUNNING_SENTINEL # Return the sentinel object

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
        command_str = f'"{java_executable_path}" -jar "{languagetool_jar_path}" --port {port} --allow-origin "*"'

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

                                                # stdout=subprocess.PIPE,
                                                # stderr=subprocess.PIPE,

                                                text=True,
                                                encoding='utf-8', shell=True)
    except Exception as e:
        logger.fatal(f"Failed to start LanguageTool Server process with shell=True: {e}")
        return False

    # scripts/py/func/start_languagetool_server.py:137
    # 4. Wait for responsiveness (existing logic)
    if settings.DEV_MODE:
        logger.info("Waiting for LanguageTool Server to be responsive...")
    for _ in range(20):
        if _is_lt_server_responsive(full_base_url, timeout=1.5):
            if settings.DEV_MODE:
                logger.info("LanguageTool Server is online.")
            return languagetool_process

        if languagetool_process.poll() is not None:
            logger.fatal("LanguageTool process terminated unexpectedly.")
            _, stderr = languagetool_process.communicate()
            if stderr: logger.error(f"LanguageTool STDERR:\n{stderr}")
            return False
        time.sleep(1.5)

    logger.critical("LanguageTool Server did not become responsive.")
    from .stop_languagetool_server import stop_languagetool_server
    stop_languagetool_server(logger, languagetool_process)
    return False
