# s.ps1
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$ArgsList
)
$query = $ArgsList -join " "
if (-not $query) {
    Write-Host "question <your question>"
    exit 1
}


local TEMP_FILE=$(mktemp)
local SHORT_TIMEOUT_SECONDS=2
local LONG_TIMEOUT_SECONDS=70

# Path shortcuts
local PY_EXEC="$PROJECT_ROOT/.venv/bin/python3"
local CLI_SCRIPT="$PROJECT_ROOT/scripts/py/cli_client.py"

# --- 1. try
timeout $SHORT_TIMEOUT_SECONDS \
"$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
--lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE" 2>&1

local EXIT_CODE=$?
local OUTPUT=$(cat "$TEMP_FILE")
rm "$TEMP_FILE"

# 1. proof german: Verbindungsfehler gefunden (Service nicht erreichbar)
#if echo "$OUTPUT" | grep -q "Verbindungsfehler (Service nicht erreichbar?):"; then
    #echo "ACHTUNG: Verbindungsfehler erkannt!"

# Prüfe (Verbindungsfehler) ODER ob Streamlit fehlt
# Uvicorn und Streamlit
if echo "$OUTPUT" | grep -q "Verbindungsfehler" || ! pgrep -f "streamlit-chat.py" > /dev/null; then
    echo "Service-Check: Backend oder Frontend fehlt. Starte neu..."

    start_service

    echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
    local KIWIX_SCRIPT="$PROJECT_ROOT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh"
    if [ -f "$KIWIX_SCRIPT" ]; then
        bash "$KIWIX_SCRIPT"
    fi

    # echo './config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh'
    # ./config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh
    echo '++++++++++++++++++++++++++++++++++++++++++++++++++'

    echo "BITTE ERNEUT EINGEBEN: s $*"
    return 1

# 2. Timeout (124) == OR success (0)
elif [ $EXIT_CODE -eq 124 ] || [ $EXIT_CODE -eq 0 ]; then

    # great EXIT_CODE 0 war, success with short answer
    if [ $EXIT_CODE -eq 0 ]; then
        echo "$OUTPUT"
        return 0
    fi
    echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."

    local TEMP_FILE_2=$(mktemp)

    timeout $LONG_TIMEOUT_SECONDS \
    "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
    --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1

    local EXIT_CODE_2=$?
    local OUTPUT_2=$(cat "$TEMP_FILE_2")
    rm "$TEMP_FILE_2"
    echo "$OUTPUT_2"
    if [ $EXIT_CODE_2 -ne 0 ]; then
         echo "WARNUNG: Timeout > $LONG_TIMEOUT_SECONDS Sec. "
    fi
    return 0
# (Exit Code > 0, not 124, not connction eror Verbindungsfehler)
else
    echo "FEHLER: Das Skript ist mit einem allgemeinen Fehler beendet worden."
    echo "$OUTPUT"
    return $EXIT_CODE
fi
