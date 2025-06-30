#!/bin/bash
# activate-venv_and_run-server.sh
# Exit immediately if a command fails
set -e

SCRIPT_firstName="dictation_service"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

PROJECT_ROOT="$SCRIPT_DIR/.."

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
        exit 1
    else
        echo "Service heartbeat is stale. Attempting to restart."
    fi
else
    echo "Service is not running."
fi


echo "Activating virtual environment at '$PROJECT_ROOT/venv'..."
source "$PROJECT_ROOT/.venv/bin/activate"

echo "Starting Python server from '$PROJECT_ROOT'..."
# We run the python script using its absolute path to be safe

echo "Starting service..."
# python3 "$SCRIPT_TO_START" &
python3 "$SCRIPT_TO_START" &

# echo "PROJECT_ROOT = $PROJECT_ROOT"
pkill -9 -f "$PROJECT_ROOT/type_watcher.sh"
sleep 0.02
$PROJECT_ROOT/type_watcher.sh &
#exit 1


# bash -x $PROJECT_ROOT/type_watcher.sh &

