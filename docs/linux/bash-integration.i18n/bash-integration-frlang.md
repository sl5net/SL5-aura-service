# Intégration du shell Bash

Pour faciliter l'interaction avec la CLI STT (Speech-to-Text), vous pouvez ajouter une fonction de raccourci à votre `~/.bashrc`. Cela vous permet de taper simplement « votre question » dans le terminal.

## Instructions de configuration

1. Ouvrez votre configuration Bash avec un éditeur que vous aimez :
   ```bash
   nano ~/.bashrc
   kate ~/.bashrc
   ```

2. Collez le bloc suivant à la fin du fichier :

```bash
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
    # 2. Timeout (124) == OR success (0)
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

3. Rechargez votre configuration :
   ```bash
   source ~/.bashrc
   ```

> **Remarque :** Si vous utilisez Bash comme shell de connexion (par exemple via SSH), ajoutez également le même bloc à `~/.bash_profile`, ou sourcez `~/.bashrc` à partir de celui-ci :
> ```bash
> [ -f ~/.bashrc ] && source ~/.bashrc
> ```

## Caractéristiques

- **Chemins dynamiques** : recherche automatiquement la racine du projet via le fichier de marqueur `/tmp`.
- **Auto-Restart** : si le backend est en panne, il tente d'exécuter `start_service` et les services Wikipédia locaux.
- **Smart Timeouts** : essaie d'abord une réponse rapide de 2 secondes, puis revient à un mode de traitement approfondi de 70 secondes.