# Integração Ksh (Korn Shell)

Para facilitar a interação com a CLI STT (Speech-to-Text), você pode adicionar uma função de atalho ao seu `~/.kshrc`. Isso permite que você simplesmente digite `s "sua pergunta"` no terminal.

## Instruções de configuração

1. Abra sua configuração Ksh com um editor de sua preferência:
   ```bash
   nano ~/.kshrc
   kate ~/.kshrc
   ```

2. Cole o seguinte bloco no final do arquivo:

```ksh
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

3. Certifique-se de que o Ksh carregue seu arquivo de configuração. Adicione ou verifique isso em `~/.profile`:
   ```ksh
   export ENV="$HOME/.kshrc"
   ```

4. Recarregue sua configuração:
__CODE_BLOCO_3__

## Notas específicas do Ksh

- Ksh suporta a sintaxe `nome da função { }` e `nome() { }`; a palavra-chave `function` é usada aqui para maior clareza.
- `local` **não** é suportado em todas as variantes do Ksh (por exemplo, `ksh88`). As variáveis na função acima são, portanto, declaradas sem `local`. Se você estiver usando `mksh` ou `ksh93`, `typeset` pode ser usado: `typeset TEMP_FILE=$(mktemp)`.
- A variável `ENV` controla quais arquivos são fontes Ksh para sessões interativas, semelhante a `.bashrc`.

## Características

- **Caminhos Dinâmicos**: Encontra automaticamente a raiz do projeto através do arquivo marcador `/tmp`.
- **Auto-Restart**: Se o backend estiver inativo, ele tenta executar o `start_service` e os serviços locais da Wikipedia.
- **Tempos limite inteligentes**: primeiro tenta uma resposta rápida de 2 segundos e depois volta para um modo de processamento profundo de 70 segundos.