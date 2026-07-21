#!/usr/bin/env bash
# tools/keep-keys-up.sh

# --- Singleton via flock ---
exec 9>/tmp/keep-keys-up.lock
flock -n 9 || { exit 0; } # Beenden, wenn bereits eine Instanz läuft

# --- DISPLAY sicherstellen ---
: "${DISPLAY:=:0}"
export DISPLAY

do_setup() {
    case "$XDG_SESSION_TYPE" in
        x11)
            setxkbmap -option caps:none
            ;;
        wayland)
            case "$XDG_CURRENT_DESKTOP" in
                *KDE*)
                    kwriteconfig6 --file kxkbrc --group Layout --key Options "caps:none"
                    qdbus org.kde.keyboard /Layouts reconfigure 2>/dev/null || true
                    ;;
                *GNOME*)
                    gsettings set org.gnome.desktop.input-sources xkb-options "['caps:none']"
                    ;;
            esac
            ;;
    esac
}

any_key_physically_pressed() {
    command -v xinput >/dev/null 2>&1 || return 2
    [ -z "${DISPLAY:-}" ] && return 2
    
    local ids
    ids="$(xinput list --id-only 2>/dev/null)"
    [ -z "$ids" ] && return 1
    
    while IFS= read -r id; do
        [ -z "$id" ] && continue
        if xinput query-state "$id" 2>/dev/null | grep -q "key\[.*\]=down"; then
            return 0
        fi
    done <<<"$ids"
    return 1
}

do_cleanup() {
    # Falls der User gerade physisch Tasten drückt, kurz warten oder abbrechen
    if [[ "$XDG_SESSION_TYPE" == "x11" ]]; then
        local retry=0
        while any_key_physically_pressed && [ $retry -lt 5 ]; do
            sleep 0.2
            ((retry++))
        done
    fi

    # Modifier-Tasten freigeben
    xdotool keyup Alt_L Alt_R Control_L Control_R Shift_L Shift_R Super_L Super_R ISO_Level3_Shift Num_Lock 2>/dev/null
#    xdotool keyup Alt_L Alt_R Control_L Control_R Shift_L Shift_R Super_L Super_R ISO_Level3_Shift Num_Lock 2>/dev/null

    # dotool: free all keys (if dotool is Input-Backend) docs/bugfix/NOTES_type_watcher_stuck_key_dotool.md
    # docs/bugfix/NOTES_type_watcher_stuck_key_dotool.md
    if [[ "${INPUT_METHOD:-}" == "dotool" ]] && command -v dotool >/dev/null 2>&1; then
        printf 'keyup shift ctrl alt a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8 9 0 minus equal leftbrace rightbrace semicolon apostrophe grave backslash comma dot slash space enter tab backspace kp0 kp1 kp2 kp3 kp4 kp5 kp6 kp7 kp8 kp9 kpdot kpplus kpminus kpasterisk kpslash kpenter\n' | dotool 2>/dev/null
    fi


    # CapsLock nur ausschalten, wenn es an ist
    if command -v xset >/dev/null 2>&1; then
        if xset q 2>/dev/null | grep -q "Caps Lock:   on"; then
            xdotool key Caps_Lock
        fi
    fi
}

# Logik basierend auf Argumenten
case "$1" in
    --init)
        do_setup
        ;;
    --cleanup)
        # Kurze Verzögerung, damit do_type sicher fertig ist
        sleep 1.5
        do_cleanup
        ;;
    *)
        # Default: Beides (für Abwärtskompatibilität)
        do_setup
        do_cleanup
        sleep 1.5
        do_setup
        do_cleanup
        ;;
esac
