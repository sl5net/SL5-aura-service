#!/bin/bash
end_service_script() {
    local service_name=$1
# Find the process ID (PID) of the target service
pid=$(pgrep -f "$service_name")

    if [[ -n "$pid" ]]; then
# Kill the process using the PID
kill -9 "$pid" 2>/dev/null

        echo "$service_name process with PID $pid has been terminated."
else
echo "$service_name process is not running."
fi
}

main() {
    local service_name="aura_engine.py"
end_service_script "$service_name"
}

main
