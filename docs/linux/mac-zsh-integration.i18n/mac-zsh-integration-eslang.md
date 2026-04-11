# Integración de macOS Zsh Shell

> **Shell predeterminado desde macOS Catalina (10.15).** Si tienes macOS Mojave o una versión anterior, consulta la guía [macOS Bash Integration](.././mac-bash-integration.i18n/mac-bash-integration-eslang.md).

Para facilitar la interacción con la CLI STT (Voz a Texto), puede agregar una función de acceso directo a su `~/.zshrc`. Esto le permite simplemente escribir "su pregunta" en la terminal.

## Instrucciones de configuración

1. Abra su configuración de Zsh con un editor que le guste:
   ```zsh
   nano ~/.zshrc
   open -e ~/.zshrc   # opens in TextEdit
   ```

2. Pegue el siguiente bloque al final del archivo:

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

3. Vuelva a cargar su configuración:
   ```zsh
   source ~/.zshrc
   ```

## Notas específicas de macOS

- **`timeout` no está integrado en macOS.** Instálalo a través de Homebrew antes de usar esta función:
  ```zsh
  brew install coreutils
  ```
Después de la instalación, "timeout" está disponible como "gtimeout". Agregue un alias o reemplace `timeout` con `gtimeout` en la función anterior:
  ```zsh
  alias timeout=gtimeout
  ```
Agregue el alias encima de la función `s()` en su `~/.zshrc`.

- **`pgrep`** está disponible en macOS de forma predeterminada.

- **Ruta de Python**: asegúrese de que su entorno virtual esté configurado en `$PROJECT_ROOT/.venv`. Si administra Python con `pyenv` o `conda`, ajuste `PY_EXEC` en consecuencia.

## Características

- **Rutas dinámicas**: busca automáticamente la raíz del proyecto a través del archivo de marcador `/tmp`.
- **Reinicio automático**: si el backend no funciona, intenta ejecutar `start_service` y los servicios locales de Wikipedia.
- **Tiempos de espera inteligentes**: primero intenta una respuesta rápida de 2 segundos y luego vuelve a un modo de procesamiento profundo de 70 segundos.