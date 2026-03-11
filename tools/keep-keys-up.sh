#!/usr/bin/env bash
# File: ~/bin/keep-keys-up.sh
# tools/keep-keys-up.sh:3
# Purpose: Every few seconds send "keyup" for stuck modifier keys.
#          Skips if user is actively pressing keys (to not interrupt text selection).

# --- Singleton via flock ---
exec 9>/tmp/keep-keys-up.lock
flock -n 9 || { echo "Script läuft bereits."; exit 1; }

TTS_DIR="/tmp/sl5_aura/tts_output"
SLEEP_BETWEEN_CHECKS=15   # Pause zwischen den Durchläufen

# --- Abhängigkeiten prüfen ---
command -v xdotool >/dev/null 2>&1 || { echo "xdotool nicht gefunden"; exit 1; }
command -v xset    >/dev/null 2>&1 || { echo "xset nicht gefunden"; exit 1; }

# --- DISPLAY sicherstellen ---
: "${DISPLAY:=:0}"
export DISPLAY

# --- Einmalige Keyboard-Konfiguration je nach Session ---
case "$XDG_SESSION_TYPE" in
    x11)
        echo "X11 erkannt: Setze caps:none via setxkbmap"
        setxkbmap -option caps:none
        ;;
    wayland)
        echo "Wayland erkannt ($XDG_CURRENT_DESKTOP)"
        case "$XDG_CURRENT_DESKTOP" in
            *KDE*)
                kwriteconfig6 --file kxkbrc --group Layout --key Options "caps:none"
                qdbus org.kde.keyboard /Layouts reconfigure 2>/dev/null || true
                ;;
            *GNOME*)
                gsettings set org.gnome.desktop.input-sources xkb-options "['caps:none']"
                ;;
            *)
                echo "  Unbekanntes Wayland-Desktop: $XDG_CURRENT_DESKTOP – kein caps:none gesetzt"
                ;;
        esac
        ;;
    *)
        echo "Unbekannte Session-Umgebung: '$XDG_SESSION_TYPE' – fahre trotzdem fort"
        ;;
esac

#!/usr/bin/env bash

# --- Hilfsfunktion: Prüfe ob Tasten physisch gedrückt sind (nur X11) ---
any_key_physically_pressed() {
    # Prüfe ob xinput verfügbar ist
    if ! command -v xinput >/dev/null 2>&1; then
        echo "Fehler: xinput nicht gefunden." >&2
        return 2
    fi

    # Prüfe ob wir ein X-Display haben
    if [ -z "${DISPLAY:-}" ]; then
        # echo "Fehler: DISPLAY nicht gesetzt. Vermutlich keine X11-Session." >&2
        return 2
    fi

    local ids id found_keys=""
    ids="$(xinput list --id-only 2>/dev/null)"
    [ -z "$ids" ] && return 1

    while IFS= read -r id; do
        [ -z "$id" ] && continue
        # Capture the specific key codes that are currently 'down'
        local keys
        keys=$(xinput query-state "$id" 2>/dev/null | grep "key\[.*\]=down")
        if [ -n "$keys" ]; then
            # Clean up the output (remove extra spaces/newlines) to show on one line
            found_keys+="$(echo "$keys" | tr '\n' ' ')"
        fi
    done <<<"$ids"

    if [ -n "$found_keys" ]; then
        echo "$found_keys" # Output the keys found
        return 0
    fi

    return 1
  }

# --- Hauptschleife ---
echo "keep-keys-up läuft (PID $$). Interval: ${SLEEP_BETWEEN_CHECKS}s"

while true; do
    sleep "$SLEEP_BETWEEN_CHECKS"

    # Unter X11: Tasten-Druck prüfen → wenn aktiv, überspringen

    if [[ "$XDG_SESSION_TYPE" == "x11" ]]; then
        # Capture the output of the function into a variable
        pressed_info=$(any_key_physically_pressed)
        if [ $? -eq 0 ]; then
            # Now we print the variable 'pressed_info' which contains the keys
            echo "  [skip] keys physically pressed: $pressed_info – wait for release..."

            local_timeout=10
            while any_key_physically_pressed >/dev/null && [ $local_timeout -gt 0 ]; do
                sleep 0.3
                (( local_timeout-- )) || true
            done
            sleep 0.5
        fi
    fi

    # Modifier-Tasten freigeben
    xdotool keyup \
        Alt_L Alt_R \
        Control_L Control_R \
        Shift_L Shift_R \
        Super_L Super_R \
        ISO_Level3_Shift \
        Num_Lock \

           # Nur keyup senden, wenn CapsLock wirklich AN ist (weniger invasiv)
    if xset q | grep -q "Caps Lock:   on"; then
        xdotool key Caps_Lock
    fi

done
