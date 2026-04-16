# macOS Bash 쉘 통합

> **macOS Catalina(10.15) 이전의 기본 셸.** Catalina 이후 macOS에서는 기본 셸로 Zsh가 함께 제공됩니다. 최신 Mac을 사용하고 있고 셸을 변경하지 않은 경우 대신 [macOS Zsh Integration](.././mac-zsh-integration.i18n/mac-zsh-integration-kolang.md) 가이드를 참조하세요.
>
> 다음을 사용하여 현재 쉘을 확인할 수 있습니다.
>``배쉬
> $SHELL을 에코합니다.
>````

STT(Speech-to-Text) CLI와 더 쉽게 상호작용하려면 `~/.bash_profile`에 바로가기 기능을 추가하면 됩니다. 이렇게 하면 터미널에 '질문'을 입력하기만 하면 됩니다.

## 설정 지침

1. 원하는 편집기로 Bash 구성을 엽니다.
   ```bash
   nano ~/.bash_profile
   open -e ~/.bash_profile   # opens in TextEdit
   ```

2. 파일 끝에 다음 블록을 붙여넣습니다.

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

3. 구성을 다시 로드합니다.
   ```bash
   source ~/.bash_profile
   ```

## macOS 관련 참고 사항

- **`timeout`은 macOS에 내장되어 있지 않습니다.** 이 기능을 사용하기 전에 Homebrew를 통해 설치하세요.
  ```bash
  brew install coreutils
  ```
설치 후 `timeout`은 `gtimeout`으로 사용 가능합니다. 별칭을 추가하거나 위 함수에서 `timeout`을 `gtimeout`으로 바꾸세요.
  ```bash
  alias timeout=gtimeout
  ```
`~/.bash_profile`의 `s()` 함수 위에 별칭을 추가하세요.

- **macOS는 로그인 셸에 `~/.bash_profile`을 사용합니다**(Terminal.app은 기본적으로 로그인 셸을 엽니다). 반면 Linux는 일반적으로 `~/.bashrc`를 사용합니다. 모든 컨텍스트에서 기능을 사용할 수 있도록 하려면 다른 컨텍스트에서 하나를 소싱할 수 있습니다.
  ```bash
  # Add to ~/.bash_profile:
  [ -f ~/.bashrc ] && source ~/.bashrc
  ```

- **macOS는 Bash 3.2와 함께 제공됩니다**(GPLv3 라이센스로 인해). 이 기능은 Bash 3.2+와 완벽하게 호환됩니다. Bash 5가 필요한 경우 Homebrew를 통해 설치하세요.
  ```bash
  brew install bash
  ```

- **Python 경로**: 가상 환경이 `$PROJECT_ROOT/.venv`에 설정되어 있는지 확인하세요. `pyenv` 또는 `conda`로 Python을 관리하는 경우 그에 따라 `PY_EXEC`를 조정하세요.

## 특징

- **동적 경로**: `/tmp` 마커 파일을 통해 프로젝트 루트를 자동으로 찾습니다.
- **자동 재시작**: 백엔드가 다운되면 'start_service' 및 로컬 Wikipedia 서비스 실행을 시도합니다.
- **스마트 타임아웃**: 먼저 빠른 2초 응답을 시도한 다음 70초 심층 처리 모드로 돌아갑니다.