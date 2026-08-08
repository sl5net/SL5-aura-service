import os
import pty
import time

master, slave = pty.openpty()
pid = os.fork()
if pid == 0:
    os.close(master)
    os.setsid()
    os.dup2(slave, 0)
    os.dup2(slave, 1)
    os.dup2(slave, 2)
    os.execv("/bin/bash", ["bash", "scripts/search_rules/run_rule.sh"])
else:
    os.close(slave)
    time.sleep(0.5)
    os.write(master, b"Affenbrotbaum\n")
    time.sleep(0.5)
    output = os.read(master, 10240).decode("utf-8", errors="ignore")
    os.close(master)
    with open("/tmp/fzf_screen.log", "w") as f:
        f.write(output)
    print("Execution output saved to /tmp/fzf_screen.log")
