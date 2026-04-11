# Integración de conchas de pescado

Para facilitar la interacción con la CLI STT (Voz a Texto), puede agregar una función de acceso directo a su configuración de Fish. Esto le permite simplemente escribir "su pregunta" en la terminal.

## Instrucciones de configuración

Los almacenes de conchas de pescado funcionan como archivos individuales. El enfoque recomendado es crear un archivo de función dedicado.

1. Cree el archivo de función (el directorio se creará automáticamente si no existe):
   ```fish
   mkdir -p ~/.config/fish/functions
   nano ~/.config/fish/functions/s.fish
   ```

2. Pegue el siguiente bloque en el archivo:

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

3. La función está disponible inmediatamente en todas las sesiones nuevas de Fish. Para cargarlo en la sesión actual sin abrir una nueva terminal:
   ```fish
   source ~/.config/fish/functions/s.fish
   ```

## Notas específicas sobre peces

- Fish usa `establecer valor VAR` en lugar de `VAR=valor` para la asignación de variables.
- Las condiciones utilizan bloques `test` y `end` en lugar de `[ ]` y `fi`.
- `$argv` reemplaza `$*` / `$@` para pasar argumentos.
- `$status` reemplaza `$?` para los códigos de salida.
- `o` / `y` reemplaza `||` / `&&` en expresiones condicionales.
- Fish **no** usa `local`: todas las variables dentro de las funciones son locales de forma predeterminada.

## Características

- **Rutas dinámicas**: busca automáticamente la raíz del proyecto a través del archivo de marcador `/tmp`.
- **Reinicio automático**: si el backend no funciona, intenta ejecutar `start_service` y los servicios locales de Wikipedia.
- **Tiempos de espera inteligentes**: primero intenta una respuesta rápida de 2 segundos y luego vuelve a un modo de procesamiento profundo de 70 segundos.