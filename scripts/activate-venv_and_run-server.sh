#!/bin/bash
# activate-venv_and_run-server.sh
# Exit immediately if a command fails

SCRIPT_firstName="dictation_service"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

PROJECT_ROOT="$SCRIPT_DIR/.."


$PROJECT_ROOT/type_watcher.sh &

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


echo "Activating virtual environment at '$PROJECT_ROOT/venv'..."
python3 -m venv .venv
source "$PROJECT_ROOT/.venv/bin/activate"

echo "Starting Python server from '$PROJECT_ROOT'..."
# We run the python script using its absolute path to be safe

echo "Starting service..."

python3 "$SCRIPT_TO_START" & 


