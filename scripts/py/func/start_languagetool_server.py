# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# file: scripts/py/func/start_languagetool_server.py

from pathlib import Path
import subprocess
import requests
import time
import sys
import importlib
from config.dynamic_settings import settings

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


def start_languagetool_server(logger, languagetool_jar_path, base_url):
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

            # THE FIX: Use the path we just found directly!
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

    port = base_url.split(':')[-1].split('/')[0]
    if settings.DEV_MODE:
        logger.info(f"Starting LanguageTool Server using Java from: {java_executable_path}")

    try:
        command_str = f'"{java_executable_path}" -jar "{languagetool_jar_path}" --port {port} --allow-origin "*"'
        if settings.DEV_MODE:
            logger.info(f"Executing command via shell: {command_str}")

        languagetool_process = subprocess.Popen(command_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                                encoding='utf-8', shell=True)
    except Exception as e:
        logger.fatal(f"Failed to start LanguageTool Server process with shell=True: {e}")
        return False

    if settings.DEV_MODE:
        logger.info("Waiting for LanguageTool Server to be responsive...")
    for _ in range(20):
        try:
            response = requests.get(f"{base_url}/v2/languages", timeout=1.5)
            if response.status_code == 200:
                if settings.DEV_MODE:
                    logger.info("LanguageTool Server is online.")
                return languagetool_process
        except requests.exceptions.RequestException:
            pass

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