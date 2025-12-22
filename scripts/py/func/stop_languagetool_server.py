# scripts/py/func/stop_languagetool_server.py:1
import subprocess
def stop_languagetool_server(logger, languagetool_process):
    if languagetool_process and languagetool_process.poll() is None:
        if languagetool_process and hasattr(languagetool_process, 'wait'):
            try:
                languagetool_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                languagetool_process.kill()
        else:
            if hasattr(languagetool_process, 'kill'):
                languagetool_process.kill()




