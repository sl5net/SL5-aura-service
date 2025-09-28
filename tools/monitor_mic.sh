#!/bin/bash

# find your mic
# # # # # # # # # # # # # # # # # # # # # #
# watch -n 0.5 'pactl list sources | grep -E "Name:|Description:|Mute:|Source #"'
# # # # # # # # # # # # # # # # # # # # # #

# Define the trigger file path
TRIGGER_FILE="/tmp/sl5_record.trigger"

# Define your microphone source name (MAKE SURE THIS IS CORRECT!)

# Plantronics 1
MICROPHONE_SOURCE="alsa_input.pci-0000_2f_00.4.analog-stereo"

# Plantronics 2
MICROPHONE_SOURCE="alsa_input.usb-Plantronics_Plantronics_Savi_7xx_5E832D0D1B994D56B698FBDAE8A19BE1-00.mono-fallback"

# Debounce time in seconds.
# The state must remain unchanged for this duration before a trigger occurs.
DEBOUNCE_TIME=1.0 # State must be stable for 1 second (adjusted for rapid toggles)

# Polling interval in seconds
POLLING_INTERVAL=0.2 # Check more frequently than debounce time for responsiveness

# --- New Robustness Settings ---
RAPID_TOGGLE_THRESHOLD=4 # If more than this many toggles happen...
RAPID_TOGGLE_WINDOW=5    # ...within this many seconds, trigger a cooldown.
COOLDOWN_DURATION=4     # Duration in seconds to "sleep" after rapid toggles.
# -------------------------------

LAST_CHANGE_TIMESTAMP=$(date +%s.%N)
LAST_TRIGGER_STATE="" # The mute state that last successfully caused a trigger

# Initialize previous state and timestamp for internal debounce logic
PREV_MUTE_STATE_INTERNAL=""

# Array to store timestamps of recent mute state changes for rapid toggle detection
declare -a toggle_history
last_cooldown_end_time=$(date +%s.%N) # Initialize to current time, so no cooldown initially

echo "Monitoring microphone mute state. Press Ctrl+C to stop."
echo "Using MICROPHONE_SOURCE: $MICROPHONE_SOURCE"
echo "Debounce time: ${DEBOUNCE_TIME}s"
echo "Rapid toggle detection: ${RAPID_TOGGLE_THRESHOLD} toggles in ${RAPID_TOGGLE_WINDOW}s triggers a ${COOLDOWN_DURATION}s cooldown."

# Function to get current mute state
get_mute_state() {
    pactl list sources |
        awk "/Name: $MICROPHONE_SOURCE/,/^$/ {
            if (\$1 == \"Mute:\") {
                print \$2
            }
        }" | head -n 1
}

# Initial state check
CURRENT_MUTE_STATE=$(get_mute_state)
if [ -z "$CURRENT_MUTE_STATE" ]; then
    echo "ERROR: Could not determine initial mute state for $MICROPHONE_SOURCE. Is the name correct? Exiting."
    exit 1
fi
echo "$(date): Initial STATE: $CURRENT_MUTE_STATE"
LAST_TRIGGER_STATE="$CURRENT_MUTE_STATE"
PREV_MUTE_STATE_INTERNAL="$CURRENT_MUTE_STATE" # Set internal state to match initially

while true; do
    CURRENT_TIMESTAMP=$(date +%s.%N)

    # --- Cooldown Check ---
    if (( $(echo "$CURRENT_TIMESTAMP < $last_cooldown_end_time" | bc -l) )); then
        remaining_cooldown=$(echo "$last_cooldown_end_time - $CURRENT_TIMESTAMP" | bc -l | xargs printf "%.1f")
        echo "$(date): Currently in cooldown. Ignoring state changes for another ${remaining_cooldown}s."
        sleep $POLLING_INTERVAL
        continue # Skip processing until cooldown ends
    fi
    # If we just exited cooldown, reset internal state to avoid immediate re-trigger
    if [ "$LAST_TRIGGER_STATE" == "" ]; then # This means we are coming out of an uninitialized state after cooldown
         PREV_MUTE_STATE_INTERNAL=$(get_mute_state)
         LAST_TRIGGER_STATE="$PREV_MUTE_STATE_INTERNAL"
         echo "$(date): Cooldown ended. Resetting internal state to $LAST_TRIGGER_STATE."
    fi
    # ----------------------


    CURRENT_MUTE_STATE=$(get_mute_state)

    # Check if we actually got a state
    if [ -z "$CURRENT_MUTE_STATE" ]; then
        echo "Warning: Could not determine mute state for $MICROPHONE_SOURCE. Is the name correct? Retrying..."
        sleep 1 # Short wait if state lookup fails
        continue
    fi

    # Check for state change for debounce and rapid toggle detection
    if [ "$CURRENT_MUTE_STATE" != "$PREV_MUTE_STATE_INTERNAL" ]; then
        LAST_CHANGE_TIMESTAMP=$CURRENT_TIMESTAMP
        PREV_MUTE_STATE_INTERNAL="$CURRENT_MUTE_STATE"
        # echo "$(date): Internal state change detected to $CURRENT_MUTE_STATE. Starting debounce."
    fi

    TIME_SINCE_LAST_INTERNAL_CHANGE=$(echo "$CURRENT_TIMESTAMP - $LAST_CHANGE_TIMESTAMP" | bc -l)

    # --- Debounce Logic ---
    # A trigger condition is met if:
    # 1. The current state is stable (unchanged for DEBOUNCE_TIME)
    # 2. AND this stable state is different from the state that last caused a successful trigger.
    if (( $(echo "$TIME_SINCE_LAST_INTERNAL_CHANGE >= $DEBOUNCE_TIME" | bc -l) )); then
        if [ "$CURRENT_MUTE_STATE" != "$LAST_TRIGGER_STATE" ]; then
            echo "$(date): Mute state stable at '$CURRENT_MUTE_STATE' for ${DEBOUNCE_TIME}s. Triggering event."

            # Add current timestamp to toggle history
            toggle_history+=("$CURRENT_TIMESTAMP")

            # Clean up old entries from toggle history
            # Remove timestamps older than RAPID_TOGGLE_WINDOW
            cutoff_time=$(echo "$CURRENT_TIMESTAMP - $RAPID_TOGGLE_WINDOW" | bc -l)
            new_history=()
            for t_stamp in "${toggle_history[@]}"; do
                if (( $(echo "$t_stamp >= $cutoff_time" | bc -l) )); then
                    new_history+=("$t_stamp")
                fi
            done
            toggle_history=("${new_history[@]}")

            echo "$(date): Toggle history size: ${#toggle_history[@]} within ${RAPID_TOGGLE_WINDOW}s."

            # --- Rapid Toggle Detection ---
            if [ "${#toggle_history[@]}" -ge "$RAPID_TOGGLE_THRESHOLD" ]; then
                echo "--- !!! RAPID TOGGLE DETECTED !!! ---"
                echo "$(date): ${#toggle_history[@]} toggles in less than ${RAPID_TOGGLE_WINDOW}s. Entering ${COOLDOWN_DURATION}s cooldown."
                last_cooldown_end_time=$(echo "$CURRENT_TIMESTAMP + $COOLDOWN_DURATION" | bc -l)
                toggle_history=() # Clear history after triggering cooldown
                LAST_TRIGGER_STATE="" # Reset last trigger state to force re-evaluation after cooldown
                sleep $COOLDOWN_DURATION # Immediately sleep for cooldown duration
                continue # Go to the next loop iteration, which will then handle cooldown end
            fi

            # If no rapid toggle, proceed with normal trigger
            touch "$TRIGGER_FILE"
            echo "Trigger file created/updated: $TRIGGER_FILE with state: $CURRENT_MUTE_STATE"
            LAST_TRIGGER_STATE="$CURRENT_MUTE_STATE" # Update the last successfully triggered state
        fi
    fi

    sleep $POLLING_INTERVAL
done
