#!/bin/bash
#
# test Okay it's good to see me online today and oh, and it's in English okay English is also nice
#  I can understand a little bit British English You need from the United States that can speak so well But sometimes need to listen to British or am I correct in English Undies from the United States It's And Trump is also from the United States

echo "keep_alive.sh: Checks if the dictation_service is running and restarts it if needed."
echo "Additionally, check the timestamp of /tmp/dictation_service.heartbeat An old timestamp indicates that the service has become unresponsive."


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

CONFIG_FILE="$SCRIPT_DIR/config/server.conf"
SERVER_SCRIPT="$SCRIPT_DIR/scripts/activate-venv_and_run-server.sh"

source "$CONFIG_FILE" # loads Variable PORT

while true
do
    # ps aux | grep dictation_service

    if pgrep -f dictation_service > /dev/null; then
        :
    else
        echo "dictation_service is not running, starting..."
        echo "Starting TTS Server on Port $PORT..."
        #./scripts/activate-venv_and_run-server.sh
        $SERVER_SCRIPT
        sleep 10
    fi
    #time.sleep(0.40)
    sleep 0.41
done

#
