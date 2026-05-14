#!/bin/bash
# type_watcher.sh
export DOTOOL_DELAY=0

DOTOOL_PID=$!

# typedelay direkt nach Start setzen
sleep 0.1  # kurz warten bis dotool bereit ist
echo "typedelay 0" > /tmp/dotool_fifo

set -euo pipefail

DIR_TO_WATCH="/tmp/sl5_aura/tts_output"
LOCKFILE="/tmp/sl5_aura/type_watcher.lock"

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
LOG_DIR="$SCRIPT_DIR/log"
LOGFILE="$LOG_DIR/type_watcher.log"

AUTO_ENTER_FLAG="/tmp/sl5_aura/sl5_auto_enter.flag"

INPUT_METHOD=""

# --- Detect Wayland or X11 ---
if [[ -n "${WAYLAND_DISPLAY:-}" ]]; then
    DISPLAY_SERVER="wayland"
    INPUT_METHOD="dotool"
    echo "🖥️  Display server: Wayland/KDE detected. Using $INPUT_METHOD for text input."
else
    DISPLAY_SERVER="x11"
    INPUT_METHOD="xdotool"


    # read file if readable, else set default
    timeout=20
    file='/tmp/sl5_aura/aura_engine.heartbeat'
    if inotifywait -q -t "$timeout" -e modify,close_write,create "$(dirname "$file")"; then
      echo "heartbeat change found $(dirname "$file")"
    fi

    backup_settings_x11_input_method_OVERRIDE_PATH="/tmp/sl5_aura/settings_py_backup/x11_input_method_OVERRIDE.txt"
    path="$backup_settings_x11_input_method_OVERRIDE_PATH"
    if [[ -r "$path" ]]; then OVERRIDE=$(<"$path"); else OVERRIDE="ERROR_2026-0301-0913"; fi

    echo "DEBUG OVERRIDE: '$OVERRIDE'"
    # [[ "$OVERRIDE" == "dotool" ]] && INPUT_METHOD="dotool"

    if [[ "$OVERRIDE" == "dotool" ]]; then
      if command -v dotool >/dev/null 2>&1; then
          INPUT_METHOD="dotool"
      else
          echo "WARNING: dotool not found, falling back to xdotool"
          INPUT_METHOD="xdotool"
      fi
    fi

    echo "🖥️  Display server: X11 detected. Using ⌨️ $INPUT_METHOD 🔣 for text  input."
fi

echo "Using: $INPUT_METHOD"


# bis 22.3.'26
#if [[ "$INPUT_METHOD" == "dotool" ]]; then
#  LANG_CODE=''
#    # 1. Modellnamen lesen
#    MODEL_PATH="config/model_name.txt"
#    if [[ -f "$MODEL_PATH" ]]; then
#        MODEL_NAME=$(cat "$MODEL_PATH")
#        # Extrahiert den Teil nach 'model-' (z.B. 'de' aus 'vosk-model-de-0.21')
#        LANG_CODE=$(echo "$MODEL_NAME" | sed -n 's/.*model-\([a-z]\{2\}\).*/\1/p')
#    fi
#    # 2. Fallback, falls Datei leer oder nicht da
#    [[ -z "$LANG_CODE" ]] && LANG_CODE="de"
#
#    # 3. dotool mitteilen, welches Layout es nutzen soll
#    export XKB_DEFAULT_LAYOUT="$LANG_CODE"
#    export DOTOOL_XKB_LAYOUT="$LANG_CODE"
#
#    echo "🌍 Language detected: $LANG_CODE (Applied to dotool)"
#fi

# neu ? 2026-0323-1412 23.3.'26 14:12 Mon
# --- dotool: Sprache & Daemon ---
if [[ "$INPUT_METHOD" == "dotool" ]]; then

    # 1. Pruefen ob dotool ueberhaupt installiert ist
    if ! command -v dotool &>/dev/null; then
        echo "WARNUNG: dotool nicht gefunden. Tippen unter Wayland nicht moeglich."
        echo "  Installieren mit: yay -S dotool"
        INPUT_METHOD="xdotool"  # Graceful Fallback
    else

        # 2. Keyboard-Layout aus Modellname ermitteln
        LANG_CODE=''
        MODEL_PATH="config/model_name.txt"
        if [[ -f "$MODEL_PATH" ]]; then
            MODEL_NAME=$(cat "$MODEL_PATH")
            LANG_CODE=$(echo "$MODEL_NAME" | sed -n 's/.*model-\([a-z]\{2\}\).*/\1/p')
        fi
        [[ -z "$LANG_CODE" ]] && LANG_CODE="de"
        export XKB_DEFAULT_LAYOUT="$LANG_CODE"
        export DOTOOL_XKB_LAYOUT="$LANG_CODE"
        echo " Language detected: $LANG_CODE (Applied to dotool)"

        # 3. dotoold Daemon starten falls noetig (nur wenn dotoold existiert)
        if command -v dotoold &>/dev/null && ! pgrep -x "dotoold" >/dev/null 2>&1; then
            echo "Aura: Starte dotoold Daemon..."
            dotoold &
            for i in {1..6}; do
                sleep 0.5
                pgrep -x "dotoold" >/dev/null 2>&1 && break
            done
        fi

    fi
fi




do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        # export XKB_DEFAULT_LAYOUT=de
        # export DOTOOL_XKB_LAYOUT=de

        printf 'typedelay 2\ntype %s\n' "$text" | dotool
    else
        LC_ALL=C.UTF-8 timeout 1 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}


# Helper: press Return key
do_key_return() {
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        printf 'key enter\n' | dotool
    else
        # LC_ALL=C.UTF-8 timeout 1 xdotool key Return

        LC_ALL=C.UTF-8 timeout 1 xdotool key --delay 100 Return

    fi
}

        # DOTOOL_DELAY=0 printf 'type %s\n' "$text" | dotool
        # printf 'typedelay 0\ntype %s\n' "$text" > /tmp/dotool_fifo
        # printf 'typedelay 0\ntype %s\n' "$text" > /tmp/dotool_fifo
        # printf 'type %s\n' "$text" > /tmp/dotool_fifo
        #printf 'export DOTOOL_DELAY=0 | type %s\n' "$text" | DOTOOL_DELAY=0 dotool
        #printf 'type %s\n' "$text" | DOTOOL_DELAY=0 dotool
        #export DOTOOL_DELAY=0
        # printf 'type %s\n' "$text" | dotool
        # printf 'typedelay 0\ntype %s\n' "$text" | dotool



# Geschwindigkeitstest
# time echo "typedelay 0
# type aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" > /tmp/dotool_fifo



# Helper: type text
# - Wayland: dotool  (layout-aware, Unicode-safe, kein Daemon nötig)
# - X11:     timeout 1 xdotool or dotool

# Helper: timeout 1 xdotool with error suppression under Wayland (XWayland fallback for game macros)
xdotool_safe() {
    LC_ALL=C.UTF-8 timeout 1 xdotool "$@" || true
}













PROJECT_ROOT="$SCRIPT_DIR"

# Default: Unix virtualenv layout
PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python3"











# Das kann unangenehm genehm sein, wenn man einmal längere Zeit die Shift Taste drücken möchte zum

# Rarely needed, but acts as a safety net for stuck modifier keys.
# Releases Alt/Ctrl/Shift/Super etc. every 15s without interrupting active key combos.
$PROJECT_ROOT/tools/keep-keys-up.sh --init &

# --- END: Read Python config ---

mkdir -p "$LOG_DIR"

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOGFILE"
}
log_message "Hello from Watcher (display: $DISPLAY_SERVER)"

# --- Lockfile-Logic ---
if [ -e "$LOCKFILE" ]; then
    pid=$(cat "$LOCKFILE" 2>/dev/null)
    if [ -n "$pid" ] && ps -p "$pid" > /dev/null; then
        msg="Watcher already runs (PID: $pid). Exiting."
        echo "$msg"
        log_message "$msg"
        exit 0
    fi
    rm -f "$LOCKFILE"
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"' EXIT

# --- Wait for directory ---
while [ ! -d "$DIR_TO_WATCH" ]; do
    sleep 0.5
done

sanitize_transcription_start() {
    local raw_text="$1"
    local clean_text="$raw_text"

    clean_text=$(echo "$clean_text" | sed 's/^\xef\xbb\xbf//')
    clean_text=$(echo "$clean_text" | sed 's/^\xe2\x80\x8b//')
    clean_text=$(echo "$clean_text" | sed -e 's/^[[:space:]]*//')

    echo "$clean_text"
}

#get_active_window_title() {
#    timeout 1 xdotool getactivewindow 2>/dev/null | xargs -I{} timeout 1 xdotool getwindowname {} 2>/dev/null || true
#}

get_active_window_title() {
    local id
    id=$(timeout 1 xdotool getactivewindow 2>/dev/null) || return
    timeout 1 xdotool getwindowname "$id" 2>/dev/null || true
}

OS_TYPE=$(uname -s)

if [[ "$OS_TYPE" == "Darwin" ]]; then
    echo "✅ Watcher starting in macOS mode (using fswatch and osascript)."
    log_message "Watcher starting in macOS mode."
    fswatch -0 "$DIR_TO_WATCH" | while read -d "" file; do
        if [[ "$file" == *tts_output_*.txt ]]; then
            osascript -e "tell application \"System Events\" to keystroke \"$(cat "$file")\""
            rm -f "$file"
        fi
    done

elif [[ "$OS_TYPE" == "Linux" ]]; then
    echo "✅ Watcher starting. Watching: $DIR_TO_WATCH (mode: $DISPLAY_SERVER)"
    log_message "Watcher starting. Watching $DIR_TO_WATCH in Linux/$DISPLAY_SERVER mode."

    while true; do




# If running on Windows under a POSIX shell, prefer Windows venv layout
case "$(uname -s 2>/dev/null || echo Unknown)" in
  MINGW*|MSYS*|CYGWIN*)
    # Git Bash / MSYS / Cygwin
    PYTHON_BIN="$PROJECT_ROOT/.venv/Scripts/python.exe"
    ;;
  *)
    # Linux/macOS/WSL use the Unix path above
    ;;
esac

TYPE_WATCHER_ENABLED=$("$PYTHON_BIN" - <<'PY' 2>/dev/null || echo "True"
import sys, importlib
sys.path.insert(0, "$PROJECT_ROOT")
try:
    cfg = importlib.import_module("config.settings_local")
    val = getattr(cfg, "TYPE_WATCHER_ENABLED", True)
except ImportError:
    val = True
print("True" if bool(val) else "False")
PY
)

# echo "DEBUG: <$TYPE_WATCHER_ENABLED>"


        # Use the value
        if [[ "$TYPE_WATCHER_ENABLED" == "False" ]]; then
            echo "TYPE_WATCHER_ENABLED=False — exiting."
            sleep 5
            exit 0
        fi





         inotifywait -q -e create,close_write "$DIR_TO_WATCH" --format '%f' | grep -q "tts_output_"

#        FILE=$(inotifywait -q -e close_write "$DIR_TO_WATCH" --format '%w%f')
#        [[ "$FILE" == *tts_output_* ]] || continue
#        sleep 0.015 # if you have maybe problems with the grep may use this

        while IFS= read -r -d '' f; do
            [ -f "$f" ] || continue


            # Skip and delete files older than 8 seconds
            file_age=$(( $(date +%s) - $(stat -c %Y "$f") ))
            if [ "$file_age" -gt 8 ]; then
                rm -f "$f"
                continue
            fi

            sleep 0.4


            mapfile -t lines < "$f"
            for line in "${lines[@]}"; do
                trimmed_line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

                # Game macros: always use timeout 1 xdotool (XWayland)
                # dotool cannot target specific windows or do mouse clicks

                # Nur xdotool aufrufen wenn 0ad Prozess läuft
                if pgrep -x "pyrogenesis" > /dev/null 2>&1; then
                    GAME_WINDOW_ID=$(timeout 1 xdotool search --name "0 A.D." 2>/dev/null | head -1 || true)
                else
                    GAME_WINDOW_ID=""
                    #                 GAME_WINDOW_ID=$(timeout 1 xdotool search --name "0 A.D." 2>/dev/null | head -1 || true)
                    # old. used till 2026-0306

                fi


                if [[ -n "$GAME_WINDOW_ID" ]]; then
                    log_message "GAME_WINDOW_ID = $GAME_WINDOW_ID"

                    if [[ "$trimmed_line" == 'alt+i' ]]; then
                        xdotool_safe windowactivate "$GAME_WINDOW_ID"
                        sleep 0.2
                        log_message "Sende ALT+i explizit mit keydown/keyup"
                        xdotool_safe keydown --window "$GAME_WINDOW_ID" 64
                        sleep 0.05
                        xdotool_safe key --window "$GAME_WINDOW_ID" 31
                        sleep 0.05
                        xdotool_safe keyup --window "$GAME_WINDOW_ID" 64
                        sleep 0.1
                        log_message "Fertig mit ALT+i Sequenz. Sent alt+i"
                        sleep 0.012
                        rm -f "$f"
                        continue

                    elif [[ "$trimmed_line" == 'alt+w' ]]; then
                        xte "keydown Alt_L" "keydown w" "keyup w" "keyup Alt_L" || true
                        log_message "Sent alt+w"

                        rm -f "$f"
                        continue

                    elif [[ "$trimmed_line" == 'ctrl+c' ]]; then
                        xdotool_safe key ctrl+c clearmodifiers
                        log_message "Sent ctrl+c"
                            sleep 0.012
                        rm -f "$f"
                        continue

                    elif [[ "$trimmed_line" == 'baue Haus' ]]; then
                        xdotool_safe key h
                        sleep 0.15
                        xdotool_safe click --delay 10 --repeat 8 1
                        log_message "baue Haus"
                            sleep 0.012
                        rm -f "$f"
                        continue

                    elif [[ "$trimmed_line" == 'baue Lagerhaus' ]]; then
                        xdotool_safe key s
                        sleep 0.15
                        xdotool_safe click --delay 10 --repeat 8 1
                        log_message "baue Lagerhaus"

                            sleep 0.012
                        rm -f "$f"
                        continue

                    elif [[ "$trimmed_line" == 'select iddle' ]]; then
                        xdotool_safe keydown alt
                        xdotool_safe type '#'
                        xdotool_safe keyup alt
                        sleep 0.15
                        log_message "select iddle"

                            sleep 0.012
                        rm -f "$f"
                        continue

                    elif [[ "$trimmed_line" == 'baue Baracke' ]]; then
                        xdotool_safe key b
                        sleep 0.15
                        xdotool_safe click --delay 10 --repeat 8 1
                        sleep 4
                        log_message "baue Baracke"

                            sleep 0.012
                        rm -f "$f"
                        f=""
                        continue
                    fi
                fi

                # --- Fallback: type file content ---
                if [ -z "${CI:-}" ]; then

                    RAW_CONTENT=$(cat "$f")

                    EMOJI='🗣️'
                    PLACEHOLDER='°202511101302°'
                    SL5de='SL5.de'

                    RAW_MOD=$(printf '%s' "$RAW_CONTENT" | sed "s/Powered by $SL5de/$PLACEHOLDER$SL5de/g")
                    RAW_MOD=$(printf '%s' "$RAW_MOD"     | sed "s|$SL5de/Aura|$PLACEHOLDER$SL5de/Aura|g")

                    SANITIZED=$(sanitize_transcription_start "$RAW_MOD")

                    CLEAN_CONTENT=$(printf '%s' "$SANITIZED" | sed "s/$PLACEHOLDER/$EMOJI/g")

                    sleep 0.4

                    do_type "$CLEAN_CONTENT"
                    ($PROJECT_ROOT/tools/keep-keys-up.sh --cleanup &)
                    sleep 0.025

                    # # sleep 2

                    log_message "typed content of $f (dotool/timeout 1 xdotool hybrid)"
                    rm -f "$f"
                    continue
                fi
            done

            rm -f "$f"

            # --- Conditional Enter Key ---
            window_title=$(get_active_window_title)

            # echo "415: '$window_title' "

            if [[ -f "$AUTO_ENTER_FLAG" ]]; then
                # regexLine=$(cat "$AUTO_ENTER_FLAG")
                regexLine=$(<"$AUTO_ENTER_FLAG" tr -d '\r\n')

                if echo "$window_title" | grep -Eiq "$regexLine"; then
                    log_message "INFO: Auto-Enter is enabled. Pressing Return."
                    if [ -z "${CI:-}" ]; then
                        do_key_return
                    fi
                fi
            fi
        done < <(find "$DIR_TO_WATCH" -maxdepth 1 -type f -name 'tts_output_*.txt' -print0 | sort -z)
    done

else
    echo "ERROR: Unsupported operating system '$OS_TYPE'. Exiting."
    exit 1
fi

cleanup() {
    timeout 1 xdotool keyup Alt_L Alt_R Control_L Control_R Shift_L Shift_R 2>/dev/null || true
    # dotool: alle Modifier explizit loslassen
    if [[ "$DISPLAY_SERVER" == "dotool" ]]; then
        printf 'key shift:up\nkey ctrl:up\nkey alt:up\n' | dotool 2>/dev/null || true
    fi
}
trap cleanup EXIT INT TERM
