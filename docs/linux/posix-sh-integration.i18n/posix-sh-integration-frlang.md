# Intégration POSIX sh/Dash

Pour faciliter l'interaction avec la CLI STT (Speech-to-Text), vous pouvez ajouter une fonction de raccourci à votre profil shell. Cela vous permet de taper simplement « votre question » dans le terminal.

> **Remarque :** Dash et d'autres shells POSIX stricts (`/bin/sh` sur Debian/Ubuntu est Dash par défaut) ne prennent **pas** en charge le mot-clé `local` dans tous les contextes, substitutions de processus ou tableaux. La fonction ci-dessous est écrite pour être entièrement compatible POSIX.

## Instructions de configuration

1. Ouvrez votre profil shell avec un éditeur que vous aimez :
   ```sh
   nano ~/.profile
   # or, if your system uses ~/.shrc for interactive shells:
   nano ~/.shrc
   ```

2. Collez le bloc suivant à la fin du fichier :

```sh
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

3. Rechargez votre configuration :
   ```sh
   . ~/.profile
   ```

## Notes spécifiques à POSIX / Dash

- `local` n'est **pas** utilisé ici pour une compatibilité maximale. Toutes les variables sont limitées à une fonction par convention uniquement ; ils sont techniquement globaux en sh POSIX strict.
- `$@` est préféré à `$*` lors de la transmission d'arguments aux commandes, afin de préserver une séparation correcte des mots avec les arguments cités.
- `bash` est remplacé par `sh` lors de l'exécution du script d'assistance Kiwix pour rester dans la chaîne d'outils POSIX.
- Ce fichier de configuration est mieux placé dans `~/.profile`, qui provient des shells de connexion. Pour les shells interactifs sans connexion, votre distribution peut utiliser `~/.shrc` — consultez la documentation de votre système.

## Caractéristiques

- **Chemins dynamiques** : recherche automatiquement la racine du projet via le fichier de marqueur `/tmp`.
- **Auto-Restart** : si le backend est en panne, il tente d'exécuter `start_service` et les services Wikipédia locaux.
- **Smart Timeouts** : essaie d'abord une réponse rapide de 2 secondes, puis revient à un mode de traitement approfondi de 70 secondes.