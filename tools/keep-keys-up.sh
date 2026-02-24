#!/usr/bin/env bash
# File: ~/bin/keep-keys-up.sh
# Purpose: every 5s send "keyup" for modifier keys unless TTS output dir non-empty

# Prüfe, ob mehr als eine Instanz dieses Scripts läuft
if [ "$(pgrep -f $(basename "$0"))" != "$$" ]; then
    echo "Script läuft bereits."
    exit 1
fi



TTS_DIR="/tmp/sl5_aura/tts_output"
SLEEP=3

# Ensure we have xdotool available
command -v xdotool >/dev/null 2>&1 || { echo "xdotool not found"; exit 1; }
command -v xset >/dev/null 2>&1 || { echo "xset not found"; exit 1; }

# Ensure DISPLAY is set (adjust if you need specific display)
: "${DISPLAY:=:0}"
export DISPLAY


setxkbmap -option caps:none


while true; do
  # if directory exists and is non-empty, skip sending keys
  if [ -d "$TTS_DIR" ] && [ "$(ls -A "$TTS_DIR" 2>/dev/null)" ]; then
    sleep "$SLEEP"
#    continue
  fi

  sleep 0.15

  # send keyup for modifiers (ignore errors)
#  xdotool keyup Alt_L Alt_R Control_L Control_R Shift_L Shift_R Caps_Lock 2>/dev/null || true
#  xdotool keyup Alt_L Alt_R Control_L Control_R Shift_L Shift_R Caps_Lock Super_L Super_R 2>/dev/null || true
  xdotool keyup Alt_L Alt_R Control_L Control_R Shift_L Shift_R Caps_Lock Super_L Super_R ISO_Level3_Shift Num_Lock 2>/dev/null || true


  # xdotool keyup Alt_L Alt_R Control_L Control_R Shift_L Shift_R 2>/dev/null || true

  # 'xset q' fragt den Status ab. Wenn "Caps Lock: on" gefunden wird,
  # drücken wir die Taste einmal, um sie auszuschalten.
  if xset q | grep -q "Caps Lock:   on"; then
    xdotool key Caps_Lock
  fi

  sleep "$SLEEP"
done


