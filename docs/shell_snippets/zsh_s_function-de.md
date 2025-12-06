# Zsh Funktion: s() - KI-Client mit Adaptivem Timeout

Diese Zsh-Funktion (`s`) dient als Wrapper für den Python-Client (`cli_client.py`) und implementiert eine robuste Fehlerbehandlung sowie eine adaptive Timeout-Strategie, um sowohl Service-Verbindungsfehler schnell zu erkennen als auch lange Antworten der KI (bis zu 70 Sekunden) vollständig abzuwarten.

---

## German (Deutsch)

### Zweck
Startet den KI-Client, um eine Frage zu stellen. Die Funktion reagiert auf zwei Zustände:
1.  **Verbindungsfehler:** Schlägt der erste schnelle Versuch fehl, wird der Service-Startbefehl auf die Konsole ausgegeben, damit der Benutzer ihn einfach per Enter ausführen kann.
2.  **Lange Antwort:** Benötigt die KI-Antwort länger als 2 Sekunden, wird der Befehl mit einem Timeout von 70 Sekunden wiederholt, um die vollständige Antwort zu erhalten.

### Quellcode-Ausschnitt
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

    local TEMP_FILE=$(mktemp)
    local SHORT_TIMEOUT_SECONDS=2
    local LONG_TIMEOUT_SECONDS=70

    # --- 1. VERSUCH: Kurzes Timeout (2s) für schnelle Fehlererkennung ---
    timeout $SHORT_TIMEOUT_SECONDS \
    /home/seeh/projects/py/STT/.venv/bin/python3 \
    -u \
    /home/seeh/projects/py/STT/scripts/py/cli_client.py \
    "$*" \
    --lang \
    "de-DE" < /dev/null > "$TEMP_FILE" 2>&1

    local EXIT_CODE=$?
    local OUTPUT=$(cat "$TEMP_FILE")
    rm "$TEMP_FILE"

    # 1. PRÜFUNG: Verbindungsfehler gefunden
    if echo "$OUTPUT" | grep -q "Verbindungsfehler (Service nicht erreichbar?):"; then
        echo "ACHTUNG: Verbindungsfehler erkannt!"
        start_service
        echo "BITTE ERNEUT EINGEBEN: s $*"
        return 1

    # 2. PRÜFUNG: Timeout (124) oder Erfolg (0)
    elif [ $EXIT_CODE -eq 124 ] || [ $EXIT_CODE -eq 0 ]; then

        # Fall 2a: Kurzer Erfolg (EXIT_CODE 0)
        if [ $EXIT_CODE -eq 0 ]; then
            echo "$OUTPUT"
            return 0
        fi
        
        # Fall 2b: Timeout (EXIT_CODE 124) - Löst zweiten Versuch aus
        echo "Antwort > $SHORT_TIMEOUT_SECONDS Sek. Starte Versuch mit langem Timeout ($LONG_TIMEOUT_SECONDS s)..."

        local TEMP_FILE_2=$(mktemp)

        # --- 2. VERSUCH: Langes Timeout (70s) für vollständige Antwort ---
        timeout $LONG_TIMEOUT_SECONDS \
        /home/seeh/projects/py/STT/.venv/bin/python3 \
        -u \
        /home/seeh/projects/py/STT/scripts/py/cli_client.py \
        "$*" \
        --lang \
        "de-DE" < /dev/null > "$TEMP_FILE_2" 2>&1

        local EXIT_CODE_2=$?
        local OUTPUT_2=$(cat "$TEMP_FILE_2")
        rm "$TEMP_FILE_2"
        echo "$OUTPUT_2"

        if [ $EXIT_CODE_2 -ne 0 ]; then
             echo "WARNUNG: Timeout > $LONG_TIMEOUT_SECONDS Sec. Die Antwort ist möglicherweise unvollständig."
        fi
        return 0
        
    # 3. PRÜFUNG: Anderer, unerwarteter Fehler (Exit Code > 0, nicht 124)
    else
        echo "FEHLER: Das Skript ist mit einem allgemeinen Fehler beendet worden."
        echo "$OUTPUT"
        return $EXIT_CODE
    fi
}
# source ~/.zshrc
