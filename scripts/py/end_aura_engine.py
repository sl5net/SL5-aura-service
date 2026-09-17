import subprocess
from typing import Optional


def _kill_target_pid(single_pid: str, service_name: str) -> None:
    try:
        subprocess.run(['kill', '-9', single_pid], check=True)
        print(f'{service_name} process with PID {single_pid} has been terminated.')
    except Exception:
        pass


def end_service_script(service_name: str, exclude_pid: Optional[int] = None) -> None:
    try:
        pid_output = subprocess.check_output(['pgrep', '-f', service_name], text=True)
        for single_pid in pid_output.strip().splitlines():
            if exclude_pid is not None and single_pid.strip() == str(exclude_pid):
                continue
            _kill_target_pid(single_pid, service_name)
    except subprocess.CalledProcessError:
        pass
if __name__ == '__main__':
    service_name = 'aura_engine.py'
    end_service_script(service_name)

