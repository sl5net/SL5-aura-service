#!/bin/bash
# restart_venv_and_run-server.sh

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

CONFIG_FILE="$SCRIPT_DIR/../config/server.conf"
SERVER_SCRIPT="$SCRIPT_DIR/activate-venv_and_run-server.sh"

source "$CONFIG_FILE" # loads Variable PORT

echo "Restarting TTS Server on Port $PORT..."

pkill -f dictation_service.py
pkill -f type_watcher.sh
sleep 1

PID=$(lsof -t -i :$PORT)
if [ -n "$PID" ]; then
    kill $PID
    sleep 1
fi
$SERVER_SCRIPT
