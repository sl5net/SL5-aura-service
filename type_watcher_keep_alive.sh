#!/bin/bash
# type_watcher_keep_alive.sh
# Stoppen: pkill -f type_watcher_keep_alive.sh

# --- PURPOSE OF THIS WRAPPER SCRIPT ---
#
# The main 'type_watcher.sh' script is generally stable, but has been
# observed to crash under specific, hard-to-reproduce circumstances,
# likely related to race conditions or heavy load (e.g., after processing
# many consecutive inputs).
#
# This wrapper script acts as a simple and robust "keep-alive" watchdog.
# It runs 'type_watcher.sh' in an infinite loop. If the main script
# ever crashes or exits unexpectedly, this watchdog will automatically
# restart it after a short delay. This ensures high availability without
# making the main script overly complex.

clear

# This script acts as a watchdog for type_watcher.sh.
# It runs it in an infinite loop, so if it ever crashes, it will be
# automatically restarted after a 1-second delay.

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
LOG_DIR="$SCRIPT_DIR/log"
LOGFILE="$LOG_DIR/type_watcher_keep_alive.sh"

CONFIG_FILE_1="$SCRIPT_DIR/config/settings.py"
CONFIG_FILE_2="$SCRIPT_DIR/config/settings_local.py"

# Initial timestamps
ts1_old=$(stat -c %Y "$CONFIG_FILE_1" 2>/dev/null || echo 0)
ts2_old=$(stat -c %Y "$CONFIG_FILE_2" 2>/dev/null || echo 0)


log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOGFILE"
}

echo "Starting watchdog for type_watcher.sh"
log_message "Starting watchdog for type_watcher.sh"


while true; do
    # Check if the process is running by looking for a process with the script's name.
    # We use 'pgrep -f' and exclude the watchdog script itself.

    # Check config changes
    ts1_new=$(stat -c %Y "$CONFIG_FILE_1" 2>/dev/null || echo 0)
    ts2_new=$(stat -c %Y "$CONFIG_FILE_2" 2>/dev/null || echo 0)


    if [ "$ts1_old" != "$ts1_new" ] || [ "$ts2_old" != "$ts2_new" ]; then
        log_message "Config changed - killing type_watcher for restart"
        pkill -f "type_watcher.sh"
        ts1_old=$ts1_new
        ts2_old=$ts2_new
    fi


    if pgrep -f "type_watcher.sh" | grep -qv "$$"; then
        # It's running, do nothing.
        :
    else
        # It's not running, so it must have crashed. Start it.
        log_message "WATCHDOG: 'type_watcher.sh' is not running. Starting it now."
        log_message "$SCRIPT_DIR/type_watcher.sh"
        echo log_message "WATCHDOG: 'type_watcher.sh' is not running. Starting it now "
        echo $SCRIPT_DIR/type_watcher.sh
        $SCRIPT_DIR/type_watcher.sh
    fi

    # Wait for a few seconds before checking again.
    sleep 5
done


