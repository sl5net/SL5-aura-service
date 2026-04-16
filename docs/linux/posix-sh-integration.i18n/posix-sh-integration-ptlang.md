# Integração POSIX sh/Dash

Para facilitar a interação com a CLI STT (Speech-to-Text), você pode adicionar uma função de atalho ao seu perfil de shell. Isso permite que você simplesmente digite `s "sua pergunta"` no terminal.

> **Nota:** Dash e outros shells POSIX estritos (`/bin/sh` no Debian/Ubuntu é Dash por padrão) **não** suportam a palavra-chave `local` em todos os contextos, substituição de processos ou arrays. A função abaixo foi escrita para ser totalmente compatível com POSIX.

## Instruções de configuração

1. Abra seu perfil shell com um editor de sua preferência:
   ```sh
   nano ~/.profile
   # or, if your system uses ~/.shrc for interactive shells:
   nano ~/.shrc
   ```

2. Cole o seguinte bloco no final do arquivo:

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

3. Recarregue sua configuração:
   ```sh
   . ~/.profile
   ```

## Notas específicas do POSIX / Dash

- `local` **não** é usado aqui para máxima compatibilidade. Todas as variáveis têm escopo de função apenas por convenção; eles são tecnicamente globais em estrito POSIX sh.
- `$@` é preferível a `$*` ao passar argumentos para comandos, para preservar a divisão adequada de palavras com argumentos entre aspas.
- `bash` é substituído por `sh` ao executar o script auxiliar Kiwix para permanecer dentro do conjunto de ferramentas POSIX.
- Este arquivo de configuração é melhor colocado em `~/.profile`, que é originado por shells de login. Para shells interativos sem login, sua distribuição pode usar `~/.shrc` — verifique a documentação do sistema.

## Características

- **Caminhos Dinâmicos**: Encontra automaticamente a raiz do projeto através do arquivo marcador `/tmp`.
- **Auto-Restart**: Se o backend estiver inativo, ele tenta executar o `start_service` e os serviços locais da Wikipedia.
- **Tempos limite inteligentes**: primeiro tenta uma resposta rápida de 2 segundos e depois volta para um modo de processamento profundo de 70 segundos.