#!/bin/bash

# find your mic
# watch -n 0.5 'pactl list sources | grep -E "Name:|Description:|Mute:|Source #"'

# Define the trigger file path
TRIGGER_FILE="/tmp/sl5_record.trigger"

# Define your microphone source name (MAKE SURE THIS IS CORRECT!)

MICROPHONE_SOURCE="alsa_input.pci-0000_2f_00.4.analog-stereo"

# Debounce time in seconds.
# The state must remain unchanged for this duration before a trigger occurs.
DEBOUNCE_TIME=0.5 # State must be stable for 1 second

# Polling interval in seconds
POLLING_INTERVAL=0.2 # Check more frequently than debounce time

LAST_CHANGE_TIMESTAMP=$(date +%s.%N)

echo "Monitoring microphone mute state. Press Ctrl+C to stop."
echo "Using MICROPHONE_SOURCE: $MICROPHONE_SOURCE"
echo "Debounce time: ${DEBOUNCE_TIME}s"


CURRENT_MUTE_STATE=$(pactl list sources |
    awk "/Name: $MICROPHONE_SOURCE/,/^$/ {
        if (\$1 == \"Mute:\") {
            print \$2
        }
    }" | head -n 1)

echo "$(date): Initialize STATE: $CURRENT_MUTE_STATE"

# Initialize previous state and timestamp
PREV_MUTE_STATE="$CURRENT_MUTE_STATE" # Immediately update PREV_MUTE_STATE to prevent immediate re-trigger
                                        # but actual trigger is delayed by debounce

#    LAST_CHANGE_TIMESTAMP=$(date +%s.%N)


while true; do
    # Get the current mute state using pactl
    CURRENT_MUTE_STATE=$(pactl list sources |
        awk "/Name: $MICROPHONE_SOURCE/,/^$/ {
            if (\$1 == \"Mute:\") {
                print \$2
            }
        }" | head -n 1)

    # Check if we actually got a state
    if [ -z "$CURRENT_MUTE_STATE" ]; then
        echo "Warning: Could not determine mute state for $MICROPHONE_SOURCE. Is the name correct?"
        sleep 5 # Wait longer if we can't find the state
        exit
    fi


    # Now, check if the *current* state has been stable for long enough
    CURRENT_TIMESTAMP=$(date +%s.%N)
    TIME_SINCE_LAST_CHANGE=$(echo "$CURRENT_TIMESTAMP - $LAST_CHANGE_TIMESTAMP" | bc -l)

    # Only trigger if the state is stable AND it's a *new* stable state
    if (( $(echo "$TIME_SINCE_LAST_CHANGE >= $DEBOUNCE_TIME" | bc -l) )); then
        # We need an additional variable to track the *actually triggered* state
        # to prevent re-triggering if it stays stable for a long time
        if [ "$CURRENT_MUTE_STATE" != "$PREV_MUTE_STATE" ]; then
            LAST_CHANGE_TIMESTAMP=$(date +%s.%N)

            echo "$(date): CURRENT_MUTE_STATE : $CURRENT_MUTE_STATE"

            # exit

            # touch "$TRIGGER_FILE"
            echo "Trigger file created/updated: $TRIGGER_FILE"
            PREV_MUTE_STATE="$CURRENT_MUTE_STATE"
        fi
    fi



    # Wait for a short period before checking again
    sleep $POLLING_INTERVAL
done
