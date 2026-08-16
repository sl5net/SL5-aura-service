Este documento resume la configuración final y verificada de Zsh para interactuar con su servicio Python a través de la línea de comando.

La configuración proporciona tres métodos distintos para acceder al servicio, que van desde la salida segura hasta la ejecución inmediata.

## Resumen de configuración de la línea de comandos de Zsh

### 1. Archivo de configuración

Todo el código siguiente debe pegarse en su archivo **`~/.zshrc`**. Recuerde **`source ~/.zshrc`** o abra una nueva sesión de terminal después de realizar cambios.

### 2. El bloque de código final

Este bloque define las tres funciones requeridas. Incluye los comandos `unalias` necesarios para evitar el error de conflicto que encontramos anteriormente.

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

### 3. Uso de los Tres Comandos

| Comando | Funcionalidad | Nivel de seguridad | Ejemplo |
| :--- | :--- | :--- | :--- |
| **`sl`** | **Salida estándar:** Ejecuta el servicio e imprime el resultado completo directamente en la consola. | **SEGURO** | `sl ¿Qué es una casa? (Impresiones: "Una casa es...") |
| **`slz`** | **Preparación para la ejecución segura:** Ejecuta el servicio y pega la salida (por ejemplo, un comando de shell) en la línea de entrada de Zsh, lista para su revisión o ejecución. | **SEGURO/PREPARACIÓN** | `slz git` (Pega: `git add . && git commit...` **pero no lo ejecuta**.) |
| **`slxXsoidfuasdzof`** | **Ejecución inmediata:** Ejecuta el servicio e inmediatamente ejecuta la salida como un comando de shell. Utilice el nombre críptico como medida de seguridad. | **PELIGROSO** | `slxXsoidfuasdzof git` (Ejecuta el comando `git add...` inmediatamente.) |