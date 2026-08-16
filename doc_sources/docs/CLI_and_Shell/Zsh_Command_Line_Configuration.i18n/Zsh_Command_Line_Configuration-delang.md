Dieses Dokument fasst die endgültige und überprüfte Zsh-Konfiguration für die Interaktion mit Ihrem Python-Dienst über die Befehlszeile zusammen.

Die Konfiguration bietet drei verschiedene Methoden für den Zugriff auf den Dienst, von der sicheren Ausgabe bis zur sofortigen Ausführung.

## Zusammenfassung der Zsh-Befehlszeilenkonfiguration

### 1. Konfigurationsdatei

Der gesamte folgende Code sollte in Ihre **`~/.zshrc`**-Datei eingefügt werden. Denken Sie daran, ~/.zshrc zu **`sourcen** oder eine neue Terminalsitzung zu öffnen, nachdem Sie Änderungen vorgenommen haben.

### 2. Der letzte Codeblock

Dieser Block definiert die drei erforderlichen Funktionen. Es enthält die notwendigen „unalias“-Befehle, um den zuvor aufgetretenen Konfliktfehler zu verhindern.

```bash
# ===================================================================
# == 1. sl: Output Only (Safe Mode - Just prints the result)
# ===================================================================

# Unalias 'sl' in case it was previously defined as a simple alias
unalias sl 2>/dev/null
sl() {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi
    /home/seeh/projects/py/STT/.venv/bin/python3 /home/seeh/projects/py/STT/scripts/py/cli_client.py "$*" --lang "de-DE"
}
# source ~/.zshrc


# ===================================================================
# == 2. slz: Zsh Line Insertion (Safe Prep Mode - Paste output to prompt)
# ===================================================================

# Unalias 'slz' in case it was previously defined as an alias
unalias slz 2>/dev/null
slz() {
    if [ $# -eq 0 ]; then
        echo "Usage: slz <your question whose result should be pasted to the line>"
        return 1
    fi

    # 1. Execute the client and capture the output (the command string)
    # "$*" ensures all arguments are passed as a single string to the CLI client.
    COMMAND=$(/home/seeh/projects/py/STT/.venv/bin/python3 \
        /home/seeh/projects/py/STT/scripts/py/cli_client.py \
        "$*" --lang "de-DE")

    # 2. Use 'print -z' to paste the captured command into the current prompt line.
    print -z "$COMMAND"
}
# source ~/.zshrc

# ===================================================================
# == 3. slxXsoidfuasdzof: Immediate Execution (DANGEROUS MODE)
# ===================================================================

# Unalias the long name in case it was previously defined
unalias slxXsoidfuasdzof 2>/dev/null
slxXsoidfuasdzof() {
    if [ $# -eq 0 ]; then
        echo "Usage: slx <your question whose result will be executed immediately>"
        return 1
    fi

    # Führt den CLI-Client aus und speichert die Ausgabe in der Variable 'COMMAND'
    COMMAND=$(/home/seeh/projects/py/STT/.venv/bin/python3 \
        /home/seeh/projects/py/STT/scripts/py/cli_client.py \
        "$*" \
        --lang "de-DE")

    # Check if any output was received
    if [ -n "$COMMAND" ]; then
        echo "--> Ausführen des Befehls: $COMMAND"
        echo "--> Executing command: $COMMAND"
        # DANGER: 'eval' executes the command string immediately
        eval "$COMMAND"
    else
        echo "No command output received from the service."
    fi
}
# source ~/.zshrc

```

---

### 3. Verwendung der drei Befehle

| Befehl | Funktionalität | Sicherheitsniveau | Beispiel |
| :--- | :--- | :--- | :--- |
| **`sl`** | **Standardausgabe:** Führt den Dienst aus und druckt die gesamte Ausgabe direkt auf der Konsole. | **SICHER** | `sl Was ist ein Haus` (Drucke: „Ein Haus ist...“) |
| **`slz`** | **Sichere Ausführungsvorbereitung:** Führt den Dienst aus und fügt die Ausgabe (z. B. einen Shell-Befehl) in die Zsh-Eingabezeile ein, bereit zur Überprüfung oder Ausführung. | **SICHER/VORBEREITUNG** | `slz git` (Fügt ein: `git add . && git commit...` **führt es aber nicht aus**.) |
| **`slxXsoidfuasdzof`** | **Sofortige Ausführung:** Führt den Dienst aus und führt die Ausgabe sofort als Shell-Befehl aus. Verwenden Sie den kryptischen Namen als Sicherheitsmaßnahme. | **GEFÄHRLICH** | `slxXsoidfuasdzof git` (Führt den Befehl `git add...` sofort aus.) |