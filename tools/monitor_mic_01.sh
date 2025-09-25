
#!/bin/bash

# Define the trigger file path
TRIGGER_FILE="/tmp/sl5_record.trigger"

# find your mic
# watch -n 0.5 'pactl list sources | grep -E "Name:|Description:|Mute:|Source #"'



# Define your microphone source name (you might need to adjust this)
# Make sure this is ABSOLUTELY correct from `pactl list sources`
MICROPHONE_SOURCE="alsa_input.pci-0000_00_1f.3.analog-stereo" # <--- HIER DEINEN WERT EINSETZEN!
MICROPHONE_SOURCE="alsa_output.usb-Plantronics_Plantronics_Savi_7xx_5E832D0D1B994D56B698FBDAE8A19BE1-00.mono-fallback"

MICROPHONE_SOURCE="alsa_input.pci-0000_2f_00.4.analog-stereo"

MICROPHONE_SOURCE="alsa_input.usb-C-Media_Electronics_Inc._USB_TableMike-00.mono-fallback"




# wrong MICROPHONE_SOURCE="alsa_card.usb-Plantronics_Plantronics_Savi_7xx_5E832D0D1B994D56B698FBDAE8A19BE1-00"

# wrong MICROPHONE_SOURCE="usb-Plantronics_Plantronics_Savi_7xx_5E832D0D1B994D56B698FBDAE8A19BE1-00"



# Initialize previous state to an unknown value
PREV_MUTE_STATE=""

echo "Monitoring microphone mute state. Press Ctrl+C to stop."
echo "Using MICROPHONE_SOURCE: $MICROPHONE_SOURCE"

while true; do
    # Get the current mute state using pactl
    # We find the block for the source, then grep for Mute:
    CURRENT_MUTE_STATE=$(pactl list sources |
        awk "/Name: $MICROPHONE_SOURCE/,/^$/ {
            if (\$1 == \"Mute:\") {
                print \$2
            }
        }" | head -n 1) # head -n 1 ensures we only get the first match

    # Check if we actually got a state
    if [ -z "$CURRENT_MUTE_STATE" ]; then
        echo "Warning: Could not determine mute state for $MICROPHONE_SOURCE. Is the name correct?"
        sleep 5 # Wait longer if we can't find the state to avoid spamming
        continue
    fi

    # Check if the state has changed
    if [ "$CURRENT_MUTE_STATE" != "$PREV_MUTE_STATE" ]; then
        if [ -n "$PREV_MUTE_STATE" ]; then # Only trigger after the initial state is set
            echo "$(date): Microphone mute state changed to: $CURRENT_MUTE_STATE"
            touch "$TRIGGER_FILE"
            echo "Trigger file created/updated: $TRIGGER_FILE"
        else
            echo "$(date): Initial microphone mute state: $CURRENT_MUTE_STATE"
        fi
        PREV_MUTE_STATE="$CURRENT_MUTE_STATE"
    fi

    # Wait for a short period before checking again (e.g., 0.5 seconds)
    sleep 0.5
done

