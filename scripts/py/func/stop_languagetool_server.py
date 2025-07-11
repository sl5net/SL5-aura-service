import subprocess
def stop_languagetool_server(logger, languagetool_process):
    if languagetool_process and languagetool_process.poll() is None:
        logger.info("Shutting down LanguageTool Server...")
        languagetool_process.terminate()
        try:
            languagetool_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            languagetool_process.kill()
        languagetool_process = None

