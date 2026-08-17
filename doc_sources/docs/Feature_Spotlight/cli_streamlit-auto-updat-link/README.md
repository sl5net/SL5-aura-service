### 1. Vorbereitung der Datei (`cli_integration-de.md`)

**Datei: `docs/Feature_Spotlight/cli_integration-de.md`**

### 2. Das Zsh-Update-Skript


```sh
unalias sl 2>/dev/null
unalias s 2>/dev/null



# Funktion zum Abrufen der aktuellen öffentlichen IP
get_current_ip() {
    curl -s https://api.ipify.org
    # curl -s checkip.dyndns.org
}

# Funktion zur Durchführung des Git-Updates
update_github_ip() {
    local NEW_IP=$(get_current_ip)
    local REPO_DIR="/home/[HOME]/[proj]"

    local README_FILE="$REPO_DIR/docs/Feature_Spotlight/cli_integration-de.md"


    local OLD_IP=$(grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}" "$README_FILE" | head -n 1) # Annahme: Die IP steht als nackte IP in der README

    # Nur aktualisieren, wenn sich die IP geändert hat
    if [[ "$NEW_IP" != "$OLD_IP" ]]; then
        echo "IP-Adresse hat sich geändert: $OLD_IP -> $NEW_IP. Aktualisiere GitHub..."

        # 1. README-Datei lokal aktualisieren (Logik zum Ersetzen der alten IP durch die neue)
        sed -i "s/$OLD_IP/$NEW_IP/g" "$README_FILE"

        # 2. Git-Befehle ausführen
        cd "$REPO_DIR"

        git add "$README_FILE"
        git commit -m "IP-Update" --no-verify
        git push origin master

        cd - > /dev/null # Zurück zum ursprünglichen Verzeichnis

        echo "GitHub IP-Update abgeschlossen."
    else
        echo "IP unverändert ($NEW_IP). Kein Update nötig."
    fi
}







# -----------------------------------------------
# 1. Funktion zum Starten des Service





start_service() {
    echo "cd ~/[proj]; python3 scripts/py/start_uvicorn_service.py"
}
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

    # --- 1. try
    timeout $SHORT_TIMEOUT_SECONDS \
    /home/[HOME]/[proj]/.venv/bin/python3 \
    -u \
    /home/[HOME]/[proj]/scripts/py/cli_client.py \
    "$*" \
    --lang \
    "de-DE" < /dev/null > "$TEMP_FILE" 2>&1

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
        /home/[HOME]/[proj]/.venv/bin/python3 \
        -u \
        /home/[HOME]/[proj]/scripts/py/cli_client.py \
        "$*" \
        --lang \
        "de-DE" < /dev/null > "$TEMP_FILE_2" 2>&1

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





unalias sl 2>/dev/null
unalias slz 2>/dev/null
# LÖSUNG: Funktion slz() verwendet "$*", um Argumente zusammenzufassen und an 'print -z' zu senden.
sl() {
    if [ $# -eq 0 ]; then
        echo "Nutzung: slz <Ihre Frage, deren Ergebnis in die Zeile eingefügt werden soll>"
        return 1
    fi

    # 1. Befehl ausführen und Ergebnis in die Variable COMMAND speichern
    #    "$*" fasst alle übergebenen Argumente zu EINEM String zusammen, was der CLI-Client erwartet.
    COMMAND=$(/home/[HOME]/[proj]/.venv/bin/python3 \
        /home/[HOME]/[proj]/scripts/py/cli_client.py \
        "$*" --lang "de-DE")

    # 2. Ergebnis mit print -z in die Befehlszeile einfügen
    print -z "$COMMAND"
}



# Funktion zur Ausführung des Services und des Ergebnisses
slxXsoidfuasdzof() {
    if [ $# -eq 0 ]; then
        echo "Nutzung: slx <Ihre Frage, deren Ergebnis ausgeführt werden soll>"
        return 1
    fi

    # Führt den CLI-Client aus und speichert die Ausgabe in der Variable 'COMMAND'
    COMMAND=$(/home/[HOME]/[proj]/.venv/bin/python3 \
        /home/[HOME]/[proj]/scripts/py/cli_client.py \
        "$*" \
        --lang "de-DE")

    # Prüfen, ob eine Ausgabe vorhanden ist
    if [ -n "$COMMAND" ]; then
        echo "--> Ausführen des Befehls: $COMMAND"
        # Führt den gespeicherten String als Shell-Befehl aus
        #########################eval "$COMMAND"
        echo "5.12.'25 10:54 Fri gerade deaktiviert."
    else
        echo "Keine Befehls-Ausgabe vom Service erhalten."
    fi
}



