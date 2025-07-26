# file: scripts/py/func/start_languagetool_server.py
from pathlib import Path
import os, subprocess, requests, time
from .stop_languagetool_server import stop_languagetool_server

def start_languagetool_server(logger, jar_path, base_url):
    # Use the passed jar_path, not a relative one.
    if not Path(jar_path).exists():
        logger.critical(f"LanguageTool JAR not found at {jar_path}")
        return None # Return None on failure

    port = base_url.split(':')[-1].split('/')[0]
    logger.info("Starting LanguageTool Server...")
    command = ["java", "-jar", jar_path, "--port", port, "--allow-origin", "*"]
    try:
        languagetool_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        logger.fatal(f"Failed to start LanguageTool Server process: {e}")
        return False
    logger.info("Waiting for LanguageTool Server to be responsive...")
    for _ in range(20):
        try:
            ping_url = f"{base_url}/v2/languages"
            response = requests.get(ping_url, timeout=1.5)
            if response.status_code == 200:
                logger.info("LanguageTool Server is online.")
                return languagetool_process
        except requests.exceptions.RequestException:
            pass
        if languagetool_process and languagetool_process.poll() is not None:
            logger.fatal("LanguageTool process terminated unexpectedly.")
            stdout, stderr = languagetool_process.communicate()
            if stderr: logger.error(f"LanguageTool STDERR:\n{stderr}")
            return False
        time.sleep(1)
    logger.fatal("LanguageTool Server did not become responsive.")
    stop_languagetool_server(languagetool_process)
    return False
