#!/bin/bash
# scripts/activate-venv_and_run-server.sh
# Exit immediately if a command fails

SCRIPT_firstName="aura_engine"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

PROJECT_ROOT="$SCRIPT_DIR/.."

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
  $PROJECT_ROOT/type_watcher_keep_alive.sh &
fi


set -e


HEARTBEAT_FILE="/tmp/$SCRIPT_firstName.heartbeat"
SCRIPT_TO_START="$SCRIPT_DIR/../$SCRIPT_firstName.py"
MAX_STALE_SECONDS=5

export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus"
export DISPLAY=:0
export XAUTHORITY=${HOME}/.Xauthority
export DICTATION_SERVICE_STARTED_CORRECTLY="true"

if [ -f "$HEARTBEAT_FILE" ]
then
    last_update=$(cat "$HEARTBEAT_FILE")
    current_time=$(date +%s)
    age=$((current_time - last_update))

    if [ "$age" -lt "$MAX_STALE_SECONDS" ]
    then
        echo "Service appears to be running and healthy."
        exit 0 
    else
        echo "Service heartbeat is stale. Attempting to restart."
    fi
else
    echo "Service is not running."
fi


python3 -m venv .env

echo "Activating virtual environment at '$PROJECT_ROOT/venv'..."
python3 -m venv .venv
source "$PROJECT_ROOT/.venv/bin/activate"

echo "Starting Python server from '$PROJECT_ROOT'..."
# We run the python script using its absolute path to be safe

echo "Starting service..."

# export PYTHONDONTWRITEBYTECODE=1
PYTHONDONTWRITEBYTECODE=1 python3 "$SCRIPT_TO_START" &


