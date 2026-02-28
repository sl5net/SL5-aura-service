#!/bin/bash
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

speak_file_path="$HOME/projects/py/TTS/speak_file.py"

INPUT_METHOD=""

# --- Detect Wayland or X11 ---
if [[ -n "${WAYLAND_DISPLAY:-}" ]]; then
    DISPLAY_SERVER="wayland"
    INPUT_METHOD="dotool"
    echo "🖥️  Display server: Wayland/KDE detected. Using $INPUT_METHOD for text input."
else
    DISPLAY_SERVER="x11"
    INPUT_METHOD="xdotool"

    # 2. Python fragen (liest die Variable sicher aus der Konfig)
    # OVERRIDE=$(python3 -c "from config.settings import x11_input_method_OVERRIDE; print(x11_input_method_OVERRIDE.strip())" 2>/dev/null)

    OVERRIDE=$(python3 -c "
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location('settings', '$(pwd)/config/settings.py')
    # Stdout unterdrücken während Import
    import io
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.stdout = old_stdout
    # Jetzt sauber ausgeben
    print(mod.x11_input_method_OVERRIDE)
    ")

    echo "DEBUG OVERRIDE: '$OVERRIDE'"
    [[ "$OVERRIDE" == "dotool" ]] && INPUT_METHOD="dotool"

    echo "🖥️  Display server: X11 detected. Using $INPUT_METHOD for text input."
fi

echo "Using: $INPUT_METHOD"



do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        printf 'typedelay 2\ntype %s\n' "$text" | dotool
    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}


# Helper: press Return key
do_key_return() {
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        printf 'key Return\n' | dotool
    else
        LC_ALL=C.UTF-8 xdotool key Return
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
# - X11:     xdotool or dotool

# Helper: xdotool with error suppression under Wayland (XWayland fallback for game macros)
xdotool_safe() {
    LC_ALL=C.UTF-8 xdotool "$@" || true
}

# --- START: Read Python config ---
PROJECT_ROOT="$SCRIPT_DIR"
PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python3"

PRIMARY_TTS_ENGINE=$($PYTHON_BIN -c "import sys; sys.path.append('$PROJECT_ROOT'); from config.settings import USE_AS_PRIMARY_SPEAK; print(USE_AS_PRIMARY_SPEAK)" 2>/dev/null) || PRIMARY_TTS_ENGINE="ERROR"

echo "PRIMARY_TTS_ENGINE=$PRIMARY_TTS_ENGINE"

# Das kann unangenehm genehm sein, wenn man einmal längere Zeit die Shift Taste drücken möchte zum Beispiel:
# Schön es aktuell nicht mehr nötig ist:
# $PROJECT_ROOT/tools/keep-keys-up.sh &


if [[ "$PRIMARY_TTS_ENGINE" == "ESPEAK" ]]; then
    echo "Primary speak is ESPEAK, disabling external speaker script by clearing path."
    speak_file_path=""
fi
# --- END: Read Python config ---

if [ -e "$speak_file_path" ]; then
    echo " ok $speak_file_path exist"
else
    speak_file_path=''
    echo "$speak_file_path dont exist"
fi

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

get_active_window_title() {
    xdotool getactivewindow 2>/dev/null | xargs -I{} xdotool getwindowname {} 2>/dev/null || true
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
        inotifywait -q -e create,close_write "$DIR_TO_WATCH" --format '%f' | grep -q "tts_output_"
        sleep 0.1

        while IFS= read -r -d '' f; do
            [ -f "$f" ] || continue

            mapfile -t lines < "$f"
            for line in "${lines[@]}"; do
                trimmed_line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

                # Game macros: always use xdotool (XWayland)
                # dotool cannot target specific windows or do mouse clicks
                GAME_WINDOW_ID=$(xdotool search --name "0 A.D." 2>/dev/null | head -1 || true)

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
                        if [[ -n "$speak_file_path" ]]; then
                            python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                            sleep 0.012
                        fi
                        rm -f "$f"
                        continue

                    elif [[ "$trimmed_line" == 'alt+w' ]]; then
                        xte "keydown Alt_L" "keydown w" "keyup w" "keyup Alt_L" || true
                        log_message "Sent alt+w"
                        if [[ -n "$speak_file_path" ]]; then
                            python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                            sleep 0.012
                        fi
                        rm -f "$f"
                        continue

                    elif [[ "$trimmed_line" == 'ctrl+c' ]]; then
                        xdotool_safe key ctrl+c clearmodifiers
                        log_message "Sent ctrl+c"
                        if [[ -n "$speak_file_path" ]]; then
                            python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                            sleep 0.012
                        fi
                        rm -f "$f"
                        continue

                    elif [[ "$trimmed_line" == 'baue Haus' ]]; then
                        xdotool_safe key h
                        sleep 0.15
                        xdotool_safe click --delay 10 --repeat 8 1
                        log_message "baue Haus"
                        if [[ -n "$speak_file_path" ]]; then
                            python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                            sleep 0.012
                        fi
                        rm -f "$f"
                        continue

                    elif [[ "$trimmed_line" == 'baue Lagerhaus' ]]; then
                        xdotool_safe key s
                        sleep 0.15
                        xdotool_safe click --delay 10 --repeat 8 1
                        log_message "baue Lagerhaus"
                        if [[ -n "$speak_file_path" ]]; then
                            python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                            sleep 0.012
                        fi
                        rm -f "$f"
                        continue

                    elif [[ "$trimmed_line" == 'select iddle' ]]; then
                        xdotool_safe keydown alt
                        xdotool_safe type '#'
                        xdotool_safe keyup alt
                        sleep 0.15
                        log_message "select iddle"
                        if [[ -n "$speak_file_path" ]]; then
                            python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                            sleep 0.012
                        fi
                        rm -f "$f"
                        continue

                    elif [[ "$trimmed_line" == 'baue Baracke' ]]; then
                        xdotool_safe key b
                        sleep 0.15
                        xdotool_safe click --delay 10 --repeat 8 1
                        sleep 4
                        log_message "baue Baracke"
                        if [[ -n "$speak_file_path" ]]; then
                            python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                            sleep 0.012
                        fi
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

                    if [[ -n "$speak_file_path" ]]; then
                        python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1 &
                        sleep 0.1
                    fi

                    do_type "$CLEAN_CONTENT"
                    sleep 0.025

                    if [[ -n "$speak_file_path" ]]; then
                        sleep 3
                    fi

                    log_message "typed content of $f (dotool/xdotool hybrid)"
                    rm -f "$f"
                    continue
                fi
            done

            rm -f "$f"

            # --- Conditional Enter Key ---
            window_title=$(get_active_window_title)
            if [[ -f "$AUTO_ENTER_FLAG" ]]; then
                regexLine=$(cat "$AUTO_ENTER_FLAG")
                if echo "$window_title" | grep -Eq "$regexLine"; then
                    log_message "INFO: Auto-Enter is enabled. Pressing Return."
                    if [ -z "${CI:-}" ]; then
                        do_key_return
                    fi
                fi
            fi
        done < <(find "$DIR_TO_WATCH" -maxdepth 1 -type f -name 'tts_output_*.txt' -print0)
    done

else
    echo "ERROR: Unsupported operating system '$OS_TYPE'. Exiting."
    exit 1
fi

cleanup() {
    xdotool keyup Alt_L Alt_R Control_L Control_R Shift_L Shift_R 2>/dev/null || true
    # dotool: alle Modifier explizit loslassen
    if [[ "$DISPLAY_SERVER" == "dotool" ]]; then
        printf 'key shift:up\nkey ctrl:up\nkey alt:up\n' | dotool 2>/dev/null || true
    fi
}
trap cleanup EXIT INT TERM
