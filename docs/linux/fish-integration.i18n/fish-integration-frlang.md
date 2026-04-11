# Intégration de coquilles de poisson

Pour faciliter l'interaction avec la CLI STT (Speech-to-Text), vous pouvez ajouter une fonction de raccourci à votre configuration Fish. Cela vous permet de taper simplement « votre question » dans le terminal.

## Instructions de configuration

Fish Shell stocke les fonctions sous forme de fichiers individuels. L'approche recommandée consiste à créer un fichier de fonction dédié.

1. Créez le fichier fonction (le répertoire sera créé automatiquement s'il n'existe pas) :
   ```fish
   mkdir -p ~/.config/fish/functions
   nano ~/.config/fish/functions/s.fish
   ```

2. Collez le bloc suivant dans le fichier :

```fish
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

3. La fonction est disponible immédiatement dans toutes les nouvelles sessions Fish. Pour le charger dans la session en cours sans ouvrir un nouveau terminal :
   ```fish
   source ~/.config/fish/functions/s.fish
   ```

## Notes spécifiques aux poissons

- Fish utilise `set VAR value` au lieu de `VAR=value` pour l'affectation des variables.
- Les conditions utilisent les blocs `test` et `end` au lieu de `[ ]` et `fi`.
- `$argv` remplace `$*` / `$@` pour le passage d'arguments.
- `$status` remplace `$?` pour les codes de sortie.
- `or` / `and` remplace `||` / `&&` dans les expressions conditionnelles.
- Fish n'utilise **pas** « local » — toutes les variables à l'intérieur des fonctions sont locales par défaut.

## Caractéristiques

- **Chemins dynamiques** : recherche automatiquement la racine du projet via le fichier de marqueur `/tmp`.
- **Auto-Restart** : si le backend est en panne, il tente d'exécuter `start_service` et les services Wikipédia locaux.
- **Smart Timeouts** : essaie d'abord une réponse rapide de 2 secondes, puis revient à un mode de traitement approfondi de 70 secondes.