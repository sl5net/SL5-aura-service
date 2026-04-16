# POSIX sh / Dash-Integration

Um die Interaktion mit der STT-CLI (Speech-to-Text) zu vereinfachen, können Sie Ihrem Shell-Profil eine Verknüpfungsfunktion hinzufügen. Dadurch können Sie einfach „Ihre Frage“ in das Terminal eingeben.

> **Note:** Dash and other strict POSIX shells (`/bin/sh` on Debian/Ubuntu is Dash by default) do **not** support the `local` keyword in all contexts, process substitution, or arrays. Die folgende Funktion ist vollständig POSIX-kompatibel geschrieben.

## Einrichtungsanweisungen

1. Öffnen Sie Ihr Shell-Profil mit einem Editor, der Ihnen gefällt:
   ```sh
   nano ~/.profile
   # or, if your system uses ~/.shrc for interactive shells:
   nano ~/.shrc
   ```

2. Fügen Sie den folgenden Block am Ende der Datei ein:

```sh

please read newest updates in zsh - verson


# --- STT Project Path Resolution ---
unalias s 2>/dev/null
s() {
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
    timeout "$SHORT_TIMEOUT_SECONDS" \
    "$PY_EXEC" -u "$CLI_SCRIPT" "$@" \
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
            sh "$KIWIX_SCRIPT"
        fi
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        echo "BITTE ERNEUT EINGEBEN: s $*"
        return 1
    # 2. Timeout (124) OR success (0)
    elif [ "$EXIT_CODE" -eq 124 ] || [ "$EXIT_CODE" -eq 0 ]; then
        if [ "$EXIT_CODE" -eq 0 ]; then
            echo "$OUTPUT"
            return 0
        fi
        echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."
        TEMP_FILE_2=$(mktemp)
        timeout "$LONG_TIMEOUT_SECONDS" \
        "$PY_EXEC" -u "$CLI_SCRIPT" "$@" \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1
        EXIT_CODE_2=$?
        OUTPUT_2=$(cat "$TEMP_FILE_2")
        rm "$TEMP_FILE_2"
        echo "$OUTPUT_2"
        if [ "$EXIT_CODE_2" -ne 0 ]; then
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
   ```sh
   . ~/.profile
   ```

## POSIX/Dash-spezifische Hinweise

- „Lokal“ wird hier aus Gründen der maximalen Kompatibilität **nicht** verwendet. Alle Variablen sind nur durch Konvention funktionsbezogen; Sie sind technisch gesehen global in strengem POSIX sh.
- „$@“ wird bei der Übergabe von Argumenten an Befehle gegenüber „$*“ bevorzugt, um eine ordnungsgemäße Wortaufteilung mit Argumenten in Anführungszeichen zu gewährleisten.
- „bash“ wird beim Ausführen des Kiwix-Hilfsskripts durch „sh“ ersetzt, um innerhalb der POSIX-Toolchain zu bleiben.
- Diese Konfigurationsdatei wird am besten in „~/.profile“ abgelegt, das von Login-Shells bezogen wird. Für interaktive Shells ohne Anmeldung verwendet Ihre Distribution möglicherweise „~/.shrc“ – überprüfen Sie Ihre Systemdokumentation.

## Merkmale

- **Dynamische Pfade**: Findet automatisch das Projektstammverzeichnis über die Markierungsdatei „/tmp“.
- **Automatischer Neustart**: Wenn das Backend ausgefallen ist, versucht es, „start_service“ und lokale Wikipedia-Dienste auszuführen.
- **Intelligente Zeitüberschreitungen**: Versucht zunächst eine schnelle 2-Sekunden-Reaktion und fällt dann auf einen 70-Sekunden-Tiefverarbeitungsmodus zurück.