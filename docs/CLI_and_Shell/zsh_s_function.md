# Zsh Funktion: s() - KI-Client mit Adaptivem Timeout

English (Englisch)
Purpose

This Zsh function (s) acts as a wrapper for the Python client (cli_client.py) and implements robust error handling and an adaptive timeout strategy. It is designed to quickly detect service connection errors and ensure full AI responses (up to 70 seconds) are captured.
Key Logic

The function relies on two shell features for robustness:

    timeout: Prevents the script from hanging indefinitely and allows quick error detection.

    mktemp / Temporary Files: Bypasses shell output buffering issues by reading the script's output from a file after termination.

Usage
code Bash

    
s <your question text>
# Example: s Computer Guten Morgen

  
  
### source
```bash
# -----------------------------------------------
# 1. Funktion zum Starten des Service (Vereinfacht)
# -----------------------------------------------
start_service() {
    # Gibt den Befehl aus, um den User zum manuellen Starten aufzufordern
    echo "cd ~/projects/py/STT; python3 scripts/py/start_uvicorn_service.py"
}

# -----------------------------------------------
# 2. Die Hauptfunktion s() mit zweistufigem Timeout
# -----------------------------------------------
unalias s 2>/dev/null
s() {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi

    update_github_ip
    update_streamlitchat_fallback_ip

    local TEMP_FILE=$(mktemp)
    local SHORT_TIMEOUT_SECONDS=2
    local LONG_TIMEOUT_SECONDS=70

    # --- 1. try
    timeout $SHORT_TIMEOUT_SECONDS \
    /home/seeh/projects/py/STT/.venv/bin/python3 \
    -u \
    /home/seeh/projects/py/STT/scripts/py/cli_client.py \
    "$*" \
    --lang \
    "de-DE" --unmasked < /dev/null > "$TEMP_FILE" 2>&1

    local EXIT_CODE=$?
    local OUTPUT=$(cat "$TEMP_FILE")
    rm "$TEMP_FILE"

    # 1. proof german: Verbindungsfehler gefunden (Service nicht erreichbar)
    if echo "$OUTPUT" | grep -q "Verbindungsfehler (Service nicht erreichbar?):"; then
        echo "ACHTUNG: Verbindungsfehler erkannt!"

        start_service

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
        /home/seeh/projects/py/STT/.venv/bin/python3 \
        -u \
        /home/seeh/projects/py/STT/scripts/py/cli_client.py \
        "$*" \
        --lang \
        "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1

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
}
# source ~/.zshrc
