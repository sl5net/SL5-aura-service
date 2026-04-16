# Integración de Ksh (Korn Shell)

Para facilitar la interacción con la CLI STT (Voz a Texto), puede agregar una función de acceso directo a su `~/.kshrc`. Esto le permite simplemente escribir "su pregunta" en la terminal.

## Instrucciones de configuración

1. Abra su configuración de Ksh con un editor que le guste:
   ```bash
   nano ~/.kshrc
   kate ~/.kshrc
   ```

2. Pegue el siguiente bloque al final del archivo:

```ksh

please newest updates in zsh - verson

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

3. Asegúrese de que Ksh cargue su archivo de configuración. Agregue o verifique esto en `~/.profile`:
   ```ksh
   export ENV="$HOME/.kshrc"
   ```

4. Vuelva a cargar su configuración:
   ```ksh
   . ~/.kshrc
   ```

## Notas específicas de Ksh

- Ksh admite la sintaxis de `nombre de función { }` y `nombre() { }`; La palabra clave "función" se utiliza aquí para mayor claridad.
- `local` **no** es compatible con todas las variantes de Ksh (por ejemplo, `ksh88`). Por lo tanto, las variables de la función anterior se declaran sin "local". Si está utilizando `mksh` o `ksh93`, se puede usar `typeset` en su lugar: `typeset TEMP_FILE=$(mktemp)`.
- La variable `ENV` controla qué archivos de fuentes Ksh para sesiones interactivas, similar a `.bashrc`.

## Características

- **Rutas dinámicas**: busca automáticamente la raíz del proyecto a través del archivo de marcador `/tmp`.
- **Reinicio automático**: si el backend no funciona, intenta ejecutar `start_service` y los servicios locales de Wikipedia.
- **Tiempos de espera inteligentes**: primero intenta una respuesta rápida de 2 segundos y luego vuelve a un modo de procesamiento profundo de 70 segundos.