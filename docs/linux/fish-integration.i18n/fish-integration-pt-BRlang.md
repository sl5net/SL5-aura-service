# Integração com casca de peixe

Para facilitar a interação com a CLI STT (Speech-to-Text), você pode adicionar uma função de atalho à configuração do Fish. Isso permite que você simplesmente digite `s "sua pergunta"` no terminal.

## Instruções de configuração

A casca do peixe armazena funções como arquivos individuais. A abordagem recomendada é criar um arquivo de função dedicado.

1. Crie o arquivo de função (o diretório será criado automaticamente caso não exista):
   ```fish
   mkdir -p ~/.config/fish/functions
   nano ~/.config/fish/functions/s.fish
   ```

2. Cole o seguinte bloco no arquivo:

```fish


please newest updates in zsh - verson


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

3. A função está disponível imediatamente em todas as novas sessões do Fish. Para carregá-lo na sessão atual sem abrir um novo terminal:
   ```fish
   source ~/.config/fish/functions/s.fish
   ```

## Notas específicas sobre peixes

- Fish usa `set VAR value` em vez de `VAR=value` para atribuição de variáveis.
- As condições usam blocos `test` e `end` em vez de `[ ]` e `fi`.
- `$argv` substitui `$*` / `$@` para passagem de argumento.
- `$status` substitui `$?` para códigos de saída.
- `or` / `and` substitua `||` / `&&` em expressões condicionais.
- Fish **não** usa `local` — todas as variáveis dentro das funções são locais por padrão.

## Características

- **Caminhos Dinâmicos**: Encontra automaticamente a raiz do projeto através do arquivo marcador `/tmp`.
- **Auto-Restart**: Se o backend estiver inativo, ele tenta executar o `start_service` e os serviços locais da Wikipedia.
- **Tempos limite inteligentes**: primeiro tenta uma resposta rápida de 2 segundos e depois volta para um modo de processamento profundo de 70 segundos.