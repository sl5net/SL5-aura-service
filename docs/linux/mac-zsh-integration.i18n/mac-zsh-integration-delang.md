# macOS Zsh Shell-Integration

> **Standard-Shell seit macOS Catalina (10.15).** Wenn Sie macOS Mojave oder früher verwenden, lesen Sie stattdessen die [macOS Bash Integration](.././mac-bash-integration.i18n/mac-bash-integration-delang.md)-Anleitung.

Um die Interaktion mit der STT-CLI (Speech-to-Text) zu vereinfachen, können Sie Ihrer „~/.zshrc“ eine Verknüpfungsfunktion hinzufügen. Dadurch können Sie einfach „Ihre Frage“ in das Terminal eingeben.

## Einrichtungsanweisungen

1. Öffnen Sie Ihre Zsh-Konfiguration mit einem Editor, der Ihnen gefällt:
   ```zsh
   nano ~/.zshrc
   open -e ~/.zshrc   # opens in TextEdit
   ```

2. Fügen Sie den folgenden Block am Ende der Datei ein:

```zsh
# --- STT Project Path Resolution ---
unalias s 2>/dev/null
s() {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi
    update_github_ip
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
    if echo "$OUTPUT" | grep -q "Verbindungsfehler" || ! pgrep -f "streamlit-chat.py" > /dev/null; then
        echo "Service-Check: Backend oder Frontend fehlt. Starte neu..."
        start_service
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        local KIWIX_SCRIPT="$PROJECT_ROOT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh"
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
    else
        echo "ERROR"
        echo "$OUTPUT"
        return $EXIT_CODE
    fi
}
```

3. Laden Sie Ihre Konfiguration neu:
   ```zsh
   source ~/.zshrc
   ```

## macOS-spezifische Hinweise

- **`Timeout` ist nicht in macOS integriert.** Installieren Sie es über Homebrew, bevor Sie diese Funktion verwenden:
  ```zsh
  brew install coreutils
  ```
Nach der Installation ist „timeout“ als „gtimeout“ verfügbar. Fügen Sie entweder einen Alias hinzu oder ersetzen Sie „timeout“ durch „gtimeout“ in der obigen Funktion:
  ```zsh
  alias timeout=gtimeout
  ```
Fügen Sie den Alias über der Funktion „s()“ in Ihrer „~/.zshrc“ hinzu.

- **`pgrep`** ist standardmäßig auf macOS verfügbar.

- **Python-Pfad**: Stellen Sie sicher, dass Ihre virtuelle Umgebung unter „$PROJECT_ROOT/.venv“ eingerichtet ist. Wenn Sie Python mit „pyenv“ oder „conda“ verwalten, passen Sie „PY_EXEC“ entsprechend an.

## Merkmale

- **Dynamische Pfade**: Findet automatisch das Projektstammverzeichnis über die Markierungsdatei „/tmp“.
- **Automatischer Neustart**: Wenn das Backend ausgefallen ist, versucht es, „start_service“ und lokale Wikipedia-Dienste auszuführen.
- **Intelligente Zeitüberschreitungen**: Versucht zunächst eine schnelle 2-Sekunden-Reaktion und fällt dann auf einen 70-Sekunden-Tiefverarbeitungsmodus zurück.