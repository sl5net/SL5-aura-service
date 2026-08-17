Este documento resume a configuração Zsh final e verificada para interagir com seu serviço Python por meio da linha de comando.

A configuração fornece três métodos distintos para acessar o serviço, desde a saída segura até a execução imediata.

## Resumo da configuração da linha de comando Zsh

### 1. Arquivo de configuração

Todo o código abaixo deve ser colado em seu arquivo **`~/.zshrc`**. Lembre-se de **`source ~/.zshrc`** ou abra uma nova sessão de terminal após fazer alterações.

### 2. O bloco de código final

Este bloco define as três funções necessárias. Inclui os comandos `unalias` necessários para evitar o erro de conflito que encontramos anteriormente.

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

### 3. Uso dos Três Comandos

| Comando | Funcionalidade | Nível de segurança | Exemplo |
| :--- | :--- | :--- | :--- |
| **`sl`** | **Saída padrão:** Executa o serviço e imprime toda a saída diretamente no console. | **SEGURO** | `sl O que é uma casa` (Imprime: "Uma casa é...") |
| **`slz`** | **Preparação para Execução Segura:** Executa o serviço e cola a saída (por exemplo, um comando shell) na linha de entrada Zsh, pronta para revisão ou execução. | **SEGURO/PREP** | `slz git` (Cola: `git add . && git commit...` **mas não executa**.) |
| **`slxXsoidfuasdzof`** | **Execução Imediata:** Executa o serviço e executa imediatamente a saída como um comando shell. Use o nome enigmático como medida de segurança. | **PERIGOSO** | `slxXsoidfuasdzof git` (Executa o comando `git add...` imediatamente.) |