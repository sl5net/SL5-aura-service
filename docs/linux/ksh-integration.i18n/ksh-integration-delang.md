# Ksh (Korn Shell)-Integration

Um die Interaktion mit der STT-CLI (Speech-to-Text) zu vereinfachen, können Sie Ihrer „~/.kshrc“ eine Verknüpfungsfunktion hinzufügen. Dadurch können Sie einfach „Ihre Frage“ in das Terminal eingeben.

## Einrichtungsanweisungen

1. Öffnen Sie Ihre Ksh-Konfiguration mit einem Editor, der Ihnen gefällt:
   ```bash
   nano ~/.kshrc
   kate ~/.kshrc
   ```

2. Fügen Sie den folgenden Block am Ende der Datei ein:

```ksh
# --- STT Project Path Resolution ---
unalias s 2>/dev/null
function s {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi
    update_github_ip
    TEMP_FILE=$(mktemp)
    SHORT_TIMEOUT_SECONDS=2
    LONG_TIMEOUT_SECONDS=70
    # Path shortcuts
    PY_EXEC="$PROJECT_ROOT/.venv/bin/python3"
    CLI_SCRIPT="$PROJECT_ROOT/scripts/py/cli_client.py"
    # --- 1. try
    timeout $SHORT_TIMEOUT_SECONDS \
    "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
    --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE" 2>&1
    EXIT_CODE=$?
    OUTPUT=$(cat "$TEMP_FILE")
    rm "$TEMP_FILE"
    if echo "$OUTPUT" | grep -q "Verbindungsfehler" || ! pgrep -f "streamlit-chat.py" > /dev/null; then
        echo "Service-Check: Backend oder Frontend fehlt. Starte neu..."
        start_service
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        KIWIX_SCRIPT="$PROJECT_ROOT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh"
        if [ -f "$KIWIX_SCRIPT" ]; then
            bash "$KIWIX_SCRIPT"
        fi
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        echo "BITTE ERNEUT EINGEBEN: s $*"
        return 1
    # 2. Timeout (124) OR success (0)
    elif [ $EXIT_CODE -eq 124 ] || [ $EXIT_CODE -eq 0 ]; then
        if [ $EXIT_CODE -eq 0 ]; then
            echo "$OUTPUT"
            return 0
        fi
        echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."
        TEMP_FILE_2=$(mktemp)
        timeout $LONG_TIMEOUT_SECONDS \
        "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1
        EXIT_CODE_2=$?
        OUTPUT_2=$(cat "$TEMP_FILE_2")
        rm "$TEMP_FILE_2"
        echo "$OUTPUT_2"
        if [ $EXIT_CODE_2 -ne 0 ]; then
             echo "WARNUNG: Timeout > $LONG_TIMEOUT_SECONDS Sec. "
        fi
        return 0
    else
        echo "ERROR"
        echo "$OUTPUT"
        return $EXIT_CODE
    fi
}
```

3. Stellen Sie sicher, dass Ksh Ihre Konfigurationsdatei lädt. Fügen Sie dies in „~/.profile“ hinzu oder überprüfen Sie es:
   ```ksh
   export ENV="$HOME/.kshrc"
   ```

4. Laden Sie Ihre Konfiguration neu:
   ```ksh
   . ~/.kshrc
   ```

## Ksh-spezifische Hinweise

- Ksh unterstützt sowohl die Syntax „Funktionsname { }“ als auch „name() { }“; Aus Gründen der Übersichtlichkeit wird hier das Schlüsselwort „function“ verwendet.
- „local“ wird **nicht** in allen Ksh-Varianten unterstützt (z. B. „ksh88“). Variablen in der obigen Funktion werden daher ohne „local“ deklariert. Wenn Sie „mksh“ oder „ksh93“ verwenden, kann stattdessen „typeset“ verwendet werden: „typeset TEMP_FILE=$(mktemp)“.
– Die Variable „ENV“ steuert, welche Ksh-Quellen für interaktive Sitzungen abgelegt werden, ähnlich wie „.bashrc“.

## Merkmale

- **Dynamische Pfade**: Findet automatisch das Projektstammverzeichnis über die Markierungsdatei „/tmp“.
- **Automatischer Neustart**: Wenn das Backend ausgefallen ist, versucht es, „start_service“ und lokale Wikipedia-Dienste auszuführen.
- **Intelligente Zeitüberschreitungen**: Versucht zunächst eine schnelle 2-Sekunden-Reaktion und fällt dann auf einen 70-Sekunden-Tiefverarbeitungsmodus zurück.