#!/bin/bash
#
# restart_venv_and_run-server.sh
#
# Final version: Correctly terminates ALL associated processes (main service and watcher)
# and reliably waits for them to disappear before starting a new instance.

# --- Configuration ---
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

SERVER_SCRIPT="$SCRIPT_DIR/activate-venv_and_run-server.sh"
SERVICE_NAME_MAIN="dictation_service.py"

os_type=$(uname -s)
if [[ "$os_type" == "MINGW"* || "$os_type" == "CYGWIN"* || "$os_type" == "MSYS"* ]]; then
    # This is a Windows-based shell environment
    detected_os="windows"
else
    # This is any other OS (Linux, macOS, FreeBSD, etc.)
    detected_os="other"
fi

if [ "$detected_os" = "windows" ]; then
  echo "please start type_watcher.ahk"
  echo "please start trigger-hotkeys.ahk"
else
  SERVICE_NAME_WATCHER="type_watcher.sh"
fi



echo "Requesting restart for all services..."

# --- Step 1: Check if any of the target processes are running ---
# The -f flag for pgrep searches the full command line.
if ! pgrep -f "$SERVICE_NAME_MAIN" > /dev/null && ! pgrep -f "$SERVICE_NAME_WATCHER" > /dev/null; then
    echo "Info: No running server or watcher processes found. Starting fresh."
else
    # --- Step 2: Kill ALL old processes (Main Service AND Watcher) ---
    echo "Stopping old processes..."
    # Use -f to match the full command line, just like in pgrep.
    pkill -f "$SERVICE_NAME_MAIN"
    pkill -f "$SERVICE_NAME_WATCHER"
    echo pkill -f "$SERVICE_NAME_MAIN"
    echo pkill -f "$SERVICE_NAME_WATCHER"

    # realpath /tmp/../tmp/../tmp
    # /tmp
    # PROJECT_ROOT=realpath $SCRIPT_DIR/..
    PROJECT_ROOT=$(realpath "$SCRIPT_DIR/..")

    echo SCRIPT_DIR=$SCRIPT_DIR
    echo PROJECT_ROOT=$PROJECT_ROOT

    echo "Activating virtual environment at '$PROJECT_ROOT/venv'..."
    cd $PROJECT_ROOT
    python3 -m venv .venv
    source .venv/bin/activate
    end_dictation_servicePY="$PROJECT_ROOT/scripts/py/end_dictation_service.py"
    echo end_dictation_servicePY=$end_dictation_servicePY
    exit
    python3 "$end_dictation_servicePY" &



    # --- Step 3: Reliably wait for BOTH processes to terminate ---
    echo -n "Waiting for all processes to shut down "
    TIMEOUT_SECONDS=10
    for (( i=0; i<TIMEOUT_SECONDS; i++ )); do
        # The loop continues as long as EITHER the main service OR the watcher is found.
        if ! pgrep -f "$SERVICE_NAME_MAIN" > /dev/null && ! pgrep -f "$SERVICE_NAME_WATCHER" > /dev/null; then
            echo -e "\nInfo: All services have been terminated."
            break # Exit the loop, we are done waiting.
        fi
        echo -n "."
        sleep 1
    done
fi

sleep 1

# --- Step 4: Start the new server instance ---
echo "Starting new server and watcher..."
if [ -x "$SERVER_SCRIPT" ]; then
    "$SERVER_SCRIPT"
else
    echo "Error: Server script is not executable: $SERVER_SCRIPT"
    echo "Please run: chmod +x $SERVER_SCRIPT"
    exit 1
fi

echo "Server started or closed now."
