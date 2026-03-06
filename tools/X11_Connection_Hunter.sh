import subprocess
from collections import Counter

# Count open file descriptors pointing to the X11 socket

# tip: systemctl restart display-manager (sudo).
# Der hilfreiche Befehl war der „Radikal-Putzer“, um hängende Prozesse zu beenden:
# pkill -9 xprop; pkill -9 xdotool; pkill -9 xset; pkill -9 xwininfo

try:
    cmd = "lsof -U | grep /tmp/.X11-unix/X0"
    output = subprocess.check_output(cmd, shell=True).decode()
    # Extract PIDs (second column)
    pids = [line.split()[1] for line in output.splitlines()]
    counts = Counter(pids).most_common(10)

    print("--- Top 10 X11 Client Leakers ---")
    for pid, count in counts:
        name = subprocess.check_output(["ps", "-p", pid, "-o", "comm="]).decode().strip()
        print(f"PID {pid} ({name}): {count} connections")
except Exception as e:
    print(f"Error: {e} (X-Server might be unreachable)")
