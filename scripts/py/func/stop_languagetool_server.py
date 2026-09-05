# scripts/py/func/stop_languagetool_server.py
import subprocess
import psutil
from .language_tool_cooldown import set_language_tool_cooldown

def evict_languagetool_process(logger=None, cooldown_seconds=300.0):
    """Emergency eviction of LanguageTool to free RAM, activating cooldown."""
    set_language_tool_cooldown(cooldown_seconds)
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline') or []
            if any('languagetool' in str(arg).lower() for arg in cmdline):
                proc.kill()
                if logger:
                    logger.warning(f"Evicted LanguageTool PID {proc.pid} due to low memory.")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def stop_languagetool_server(logger, languagetool_process):
    if languagetool_process and languagetool_process.poll() is None:
        try:
            if hasattr(languagetool_process, 'terminate'):
                languagetool_process.terminate()
            languagetool_process.wait(timeout=0.5)
        except (subprocess.TimeoutExpired, Exception):
            if hasattr(languagetool_process, 'kill'):
                languagetool_process.kill()


