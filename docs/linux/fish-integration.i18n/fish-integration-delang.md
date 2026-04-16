# Integration von Fischschalen

Um die Interaktion mit der STT-CLI (Speech-to-Text) zu vereinfachen, können Sie Ihrer Fish-Konfiguration eine Verknüpfungsfunktion hinzufügen. Dadurch können Sie einfach „Ihre Frage“ in das Terminal eingeben.

## Einrichtungsanweisungen

Fischschalenspeicher fungieren als einzelne Dateien. Der empfohlene Ansatz besteht darin, eine dedizierte Funktionsdatei zu erstellen.

1. Erstellen Sie die Funktionsdatei (das Verzeichnis wird automatisch erstellt, wenn es nicht existiert):
   ```fish
   mkdir -p ~/.config/fish/functions
   nano ~/.config/fish/functions/s.fish
   ```

2. Fügen Sie den folgenden Block in die Datei ein:

```fish


please newest updates in zsh - verson


# --- STT Project Path Resolution ---
function s --description "STT CLI shortcut"
    if test (count $argv) -eq 0
        echo "question <your question>"
        return 1
    end

    update_github_ip

    set TEMP_FILE (mktemp)
    set SHORT_TIMEOUT_SECONDS 2
    set LONG_TIMEOUT_SECONDS 70

    # Path shortcuts
    set PY_EXEC "$PROJECT_ROOT/.venv/bin/python3"
    set CLI_SCRIPT "$PROJECT_ROOT/scripts/py/cli_client.py"

    # --- 1. try
    timeout $SHORT_TIMEOUT_SECONDS \
        "$PY_EXEC" -u "$CLI_SCRIPT" $argv \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE" 2>&1
    set EXIT_CODE $status
    set OUTPUT (cat "$TEMP_FILE")
    rm "$TEMP_FILE"

    if echo "$OUTPUT" | grep -q "Verbindungsfehler"; or not pgrep -f "streamlit-chat.py" > /dev/null
        echo "Service-Check: Backend oder Frontend fehlt. Starte neu..."
        start_service
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        set KIWIX_SCRIPT "$PROJECT_ROOT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh"
        if test -f "$KIWIX_SCRIPT"
            bash "$KIWIX_SCRIPT"
        end
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        echo "BITTE ERNEUT EINGEBEN: s $argv"
        return 1

    # 2. Timeout (124) OR success (0)
    else if test $EXIT_CODE -eq 124; or test $EXIT_CODE -eq 0
        if test $EXIT_CODE -eq 0
            echo "$OUTPUT"
            return 0
        end
        echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."
        set TEMP_FILE_2 (mktemp)
        timeout $LONG_TIMEOUT_SECONDS \
            "$PY_EXEC" -u "$CLI_SCRIPT" $argv \
            --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1
        set EXIT_CODE_2 $status
        set OUTPUT_2 (cat "$TEMP_FILE_2")
        rm "$TEMP_FILE_2"
        echo "$OUTPUT_2"
        if test $EXIT_CODE_2 -ne 0
            echo "WARNUNG: Timeout > $LONG_TIMEOUT_SECONDS Sec. "
        end
        return 0

    else
        echo "ERROR"
        echo "$OUTPUT"
        return $EXIT_CODE
    end
end
```

3. Die Funktion ist sofort in allen neuen Fish-Sitzungen verfügbar. Um es in der aktuellen Sitzung zu laden, ohne ein neues Terminal zu öffnen:
   ```fish
   source ~/.config/fish/functions/s.fish
   ```

## Fischspezifische Hinweise

- Fish verwendet „set VAR value“ anstelle von „VAR=value“ für die Variablenzuweisung.
- Bedingungen verwenden „test“- und „end“-Blöcke anstelle von „[]“ und „fi“.
- „$argv“ ersetzt „$*“ / „$@“ für die Argumentübergabe.
- „$status“ ersetzt „$?“ für Exit-Codes.
- „oder“ / „und“ ersetzen „||“ / „&&“ in bedingten Ausdrücken.
- Fish verwendet **nicht** „local“ – alle Variablen innerhalb von Funktionen sind standardmäßig lokal.

## Merkmale

- **Dynamische Pfade**: Findet automatisch das Projektstammverzeichnis über die Markierungsdatei „/tmp“.
- **Automatischer Neustart**: Wenn das Backend ausgefallen ist, versucht es, „start_service“ und lokale Wikipedia-Dienste auszuführen.
- **Intelligente Zeitüberschreitungen**: Versucht zunächst eine schnelle 2-Sekunden-Reaktion und fällt dann auf einen 70-Sekunden-Tiefverarbeitungsmodus zurück.