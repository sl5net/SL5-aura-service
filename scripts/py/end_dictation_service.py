import subprocess

def end_service_script(service_name):
    try:
        # pgrep richtig aufrufen:
        pid_output = subprocess.check_output(['pgrep', '-f', service_name], text=True)
        pid = pid_output.strip()
        if pid:
            # Mehrere PIDs abfangen
            for single_pid in pid.splitlines():
                kill_command = ['kill', '-9', single_pid]
                subprocess.run(kill_command, check=True)
                print(f'{service_name} process with PID {single_pid} has been terminated.')
        else:
            print(f'{service_name} process is not running.')
    except subprocess.CalledProcessError as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    service_name = 'dictation_service.py'
    end_service_script(service_name)

