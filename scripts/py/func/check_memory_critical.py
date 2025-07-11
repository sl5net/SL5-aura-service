# file scripts/py/func/check_memory_critical.py
import psutil

def check_memory_critical(threshold_mb: int) -> tuple[bool, float]:
    mem = psutil.virtual_memory()
    available_mb = mem.available / (1024 * 1024)
    return available_mb < threshold_mb, available_mb
