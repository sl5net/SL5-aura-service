#!/usr/bin/env bash
# File: ~/bin/keep-keys-up.sh
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

# --- Hilfsfunktion: Prüfe ob Tasten physisch gedrückt sind (nur X11) ---
any_key_physically_pressed() {
    # xinput query-state gibt "key[N]=down" aus wenn eine Taste gedrückt ist
    # Wir suchen das Keyboard-Gerät automatisch (erstes "keyboard" das kein "Virtual" ist)
    local device_id
    device_id=$(xinput list 2>/dev/null \
        | grep -i "keyboard" \
        | grep -iv "virtual\|pointer\|XTEST" \
        | head -1 \
        | grep -oP 'id=\K[0-9]+')

    if [ -z "$device_id" ]; then
        return 1  # Kein Gerät gefunden → lieber nicht blockieren
    fi

    xinput query-state "$device_id" 2>/dev/null | grep -q "key\[.*\]=down"
}

# --- Hauptschleife ---
echo "keep-keys-up läuft (PID $$). Interval: ${SLEEP_BETWEEN_CHECKS}s"

while true; do
    sleep "$SLEEP_BETWEEN_CHECKS"

    # Unter X11: Tasten-Druck prüfen → wenn aktiv, überspringen
    if [[ "$XDG_SESSION_TYPE" == "x11" ]]; then
        if any_key_physically_pressed; then
            echo "  [skip] Taste physisch gedrückt – warte auf Loslassen..."
            # Warte bis alle Tasten losgelassen wurden (max 10s)
            local_timeout=10
            while any_key_physically_pressed && [ $local_timeout -gt 0 ]; do
                sleep 0.3
                (( local_timeout-- )) || true
            done
            # Nochmal kurz warten damit die Aktion (z.B. Markierung) abgeschlossen ist
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
        Caps_Lock 2>/dev/null || true

    # Caps Lock ggf. ausschalten (falls noch aktiv nach keyup)
    if xset q 2>/dev/null | grep -q "Caps Lock:   on"; then
        xdotool key Caps_Lock
        echo "  [fix] Caps Lock ausgeschaltet"
    fi

done
