# Integração macOS Bash Shell

> **Shell padrão antes do macOS Catalina (10.15).** Desde o Catalina, o macOS vem com Zsh como shell padrão. Se você estiver em um Mac moderno e não tiver alterado seu shell, consulte o guia [macOS Zsh Integration](.././mac-zsh-integration.i18n/mac-zsh-integration-ptlang.md).
>
> Você pode verificar seu shell atual com:
> ```bash
> echo $SHELL
> ```

Para facilitar a interação com a CLI STT (Speech-to-Text), você pode adicionar uma função de atalho ao seu `~/.bash_profile`. Isso permite que você simplesmente digite `s "sua pergunta"` no terminal.

## Instruções de configuração

1. Abra sua configuração do Bash com um editor de sua preferência:
   ```bash
   nano ~/.bash_profile
   open -e ~/.bash_profile   # opens in TextEdit
   ```

2. Cole o seguinte bloco no final do arquivo:

```bash

please read newest updates in zsh - verson


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

3. Recarregue sua configuração:
   ```bash
   source ~/.bash_profile
   ```

## Notas específicas do macOS

- **`timeout` não está integrado no macOS.** Instale-o via Homebrew antes de usar esta função:
__CODE_BLOCO_3__
Após a instalação, `timeout` está disponível como `gtimeout`. Adicione um alias ou substitua `timeout` por `gtimeout` na função acima:
  ```bash
  brew install coreutils
  ```
Adicione o alias acima da função `s()` em seu `~/.bash_profile`.

- **macOS usa `~/.bash_profile` para shells de login** (Terminal.app abre shells de login por padrão), enquanto o Linux normalmente usa `~/.bashrc`. Se quiser que a função esteja disponível em todos os contextos, você pode obter um do outro:
__CODE_BLOCO_5__

- **macOS vem com Bash 3.2** (devido à licença GPLv3). Esta função é totalmente compatível com Bash 3.2+. Se você precisar do Bash 5, instale-o via Homebrew:
  ```bash
  alias timeout=gtimeout
  ```

- **Caminho Python**: Certifique-se de que seu ambiente virtual esteja configurado em `$PROJECT_ROOT/.venv`. Se você gerencia Python com `pyenv` ou `conda`, ajuste `PY_EXEC` de acordo.

## Características

- **Caminhos Dinâmicos**: Encontra automaticamente a raiz do projeto através do arquivo marcador `/tmp`.
- **Auto-Restart**: Se o backend estiver inativo, ele tenta executar o `start_service` e os serviços locais da Wikipedia.
- **Tempos limite inteligentes**: primeiro tenta uma resposta rápida de 2 segundos e depois volta para um modo de processamento profundo de 70 segundos.