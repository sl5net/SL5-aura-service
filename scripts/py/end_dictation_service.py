import subprocess

def end_service_script(service_name):
    try:
        # Find the process ID (PID) of the target service
        pid_output = subprocess.check_output(['pgrep', '-f', service_name], text=True, shell=True)
        pid = pid_output.strip()

        if pid:
            # Kill the process using the PID
            kill_command = f'kill -9 {pid}'
            subprocess.run(kill_command, shell=True, check=True)

            print(f'{service_name} process with PID {pid} has been terminated.')
        else:
            print(f'{service_name} process is not running.')

    except subprocess.CalledProcessError as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    service_name = 'dictation_service.py'
    end_service_script(service_name)
