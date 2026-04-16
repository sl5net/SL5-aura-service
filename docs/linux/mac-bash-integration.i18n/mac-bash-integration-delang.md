# macOS Bash Shell-Integration

> **Standard-Shell vor macOS Catalina (10.15).** Seit Catalina wird macOS mit Zsh als Standard-Shell ausgeliefert. Wenn Sie einen modernen Mac verwenden und Ihre Shell nicht geändert haben, lesen Sie stattdessen die [macOS Zsh Integration](.././mac-zsh-integration.i18n/mac-zsh-integration-delang.md)-Anleitung.
>
> Sie können Ihre aktuelle Shell überprüfen mit:
> „Bash
> echo $SHELL
> ```

Um die Interaktion mit der STT-CLI (Speech-to-Text) zu vereinfachen, können Sie Ihrem „~/.bash_profile“ eine Verknüpfungsfunktion hinzufügen. Dadurch können Sie einfach „Ihre Frage“ in das Terminal eingeben.

## Einrichtungsanweisungen

1. Öffnen Sie Ihre Bash-Konfiguration mit einem Editor, der Ihnen gefällt:
   ```bash
   nano ~/.bash_profile
   open -e ~/.bash_profile   # opens in TextEdit
   ```

2. Fügen Sie den folgenden Block am Ende der Datei ein:

```bash

please read newest updates in zsh - verson


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
   ```bash
   source ~/.bash_profile
   ```

## macOS-spezifische Hinweise

- **`Timeout` ist nicht in macOS integriert.** Installieren Sie es über Homebrew, bevor Sie diese Funktion verwenden:
  ```bash
  brew install coreutils
  ```
Nach der Installation ist „timeout“ als „gtimeout“ verfügbar. Fügen Sie entweder einen Alias hinzu oder ersetzen Sie „timeout“ durch „gtimeout“ in der obigen Funktion:
  ```bash
  alias timeout=gtimeout
  ```
Fügen Sie den Alias über der Funktion „s()“ in Ihrem „~/.bash_profile“ hinzu.

- **macOS verwendet „~/.bash_profile“ für Anmelde-Shells** (Terminal.app öffnet standardmäßig Anmelde-Shells), während Linux normalerweise „~/.bashrc“ verwendet. Wenn Sie möchten, dass die Funktion in allen Kontexten verfügbar ist, können Sie sie voneinander beziehen:
  ```bash
  # Add to ~/.bash_profile:
  [ -f ~/.bashrc ] && source ~/.bashrc
  ```

- **macOS wird mit Bash 3.2 ausgeliefert** (aufgrund der GPLv3-Lizenz). Diese Funktion ist vollständig kompatibel mit Bash 3.2+. Wenn Sie Bash 5 benötigen, installieren Sie es über Homebrew:
  ```bash
  brew install bash
  ```

- **Python-Pfad**: Stellen Sie sicher, dass Ihre virtuelle Umgebung unter „$PROJECT_ROOT/.venv“ eingerichtet ist. Wenn Sie Python mit „pyenv“ oder „conda“ verwalten, passen Sie „PY_EXEC“ entsprechend an.

## Merkmale

- **Dynamische Pfade**: Findet automatisch das Projektstammverzeichnis über die Markierungsdatei „/tmp“.
- **Automatischer Neustart**: Wenn das Backend ausgefallen ist, versucht es, „start_service“ und lokale Wikipedia-Dienste auszuführen.
- **Intelligente Zeitüberschreitungen**: Versucht zunächst eine schnelle 2-Sekunden-Reaktion und fällt dann auf einen 70-Sekunden-Tiefverarbeitungsmodus zurück.