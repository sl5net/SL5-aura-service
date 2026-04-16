# Integración POSIX sh/Dash

Para facilitar la interacción con la CLI STT (Voz a Texto), puede agregar una función de acceso directo a su perfil de shell. Esto le permite simplemente escribir "su pregunta" en la terminal.

> **Nota:** Dash y otros shells POSIX estrictos (`/bin/sh` en Debian/Ubuntu es Dash de forma predeterminada) **no** admiten la palabra clave `local` en todos los contextos, sustitución de procesos o matrices. La siguiente función está escrita para ser totalmente compatible con POSIX.

## Instrucciones de configuración

1. Abra su perfil de shell con un editor que le guste:
   ```sh
   nano ~/.profile
   # or, if your system uses ~/.shrc for interactive shells:
   nano ~/.shrc
   ```

2. Pegue el siguiente bloque al final del archivo:

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

3. Vuelva a cargar su configuración:
   ```sh
   . ~/.profile
   ```

## POSIX / Notas específicas de Dash

- `local` **no** se utiliza aquí para máxima compatibilidad. Todas las variables tienen un alcance funcional únicamente por convención; son técnicamente globales en estricto POSIX sh.
- Se prefiere `$@` a `$*` al pasar argumentos a comandos, para preservar la división adecuada de palabras con argumentos entre comillas.
- `bash` se reemplaza por `sh` al ejecutar el script auxiliar de Kiwix para permanecer dentro de la cadena de herramientas POSIX.
- Este archivo de configuración se ubica mejor en `~/.profile`, que se obtiene mediante shells de inicio de sesión. Para shells interactivos sin inicio de sesión, su distribución puede usar `~/.shrc`; consulte la documentación de su sistema.

## Características

- **Rutas dinámicas**: busca automáticamente la raíz del proyecto a través del archivo de marcador `/tmp`.
- **Reinicio automático**: si el backend no funciona, intenta ejecutar `start_service` y los servicios locales de Wikipedia.
- **Tiempos de espera inteligentes**: primero intenta una respuesta rápida de 2 segundos y luego vuelve a un modo de procesamiento profundo de 70 segundos.