import psutil
from typing import Optional


def _is_matching_process(proc: psutil.Process, service_name: str, exclude_pid: Optional[int]) -> bool:
    if exclude_pid is not None and proc.pid == exclude_pid:
        return False
    try:
        return service_name in " ".join(proc.cmdline())
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def _kill_single_process(proc: psutil.Process, service_name: str) -> None:
    try:
        proc.kill()
        print(f'{service_name} process with PID {proc.pid} has been terminated.')
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass


def end_service_script(service_name: str, exclude_pid: Optional[int] = None) -> None:
    for proc in psutil.process_iter(['pid']):
        if _is_matching_process(proc, service_name, exclude_pid):
            _kill_single_process(proc, service_name)    
    
if __name__ == '__main__':
    service_name = 'aura_engine.py'
    end_service_script(service_name)

