# Bash 쉘 통합

STT(Speech-to-Text) CLI와 더 쉽게 상호작용하려면 `~/.bashrc`에 바로가기 기능을 추가하면 됩니다. 이렇게 하면 터미널에 '질문'을 입력하기만 하면 됩니다.

## 설정 지침

1. 원하는 편집기로 Bash 구성을 엽니다.
   ```bash
   nano ~/.bashrc
   kate ~/.bashrc
   ```

2. 파일 끝에 다음 블록을 붙여넣습니다.

```bash
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
    # 2. Timeout (124) == OR success (0)
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
   source ~/.bashrc
   ```

> **참고:** Bash를 로그인 셸로 사용하는 경우(예: SSH를 통해) 동일한 블록을 `~/.bash_profile`에 추가하거나 여기에서 `~/.bashrc` 소스를 추가하세요.
>``배쉬
> [ -f ~/.bashrc ] && 소스 ~/.bashrc
>````

## 특징

- **동적 경로**: `/tmp` 마커 파일을 통해 프로젝트 루트를 자동으로 찾습니다.
- **자동 재시작**: 백엔드가 다운되면 'start_service' 및 로컬 Wikipedia 서비스 실행을 시도합니다.
- **스마트 타임아웃**: 먼저 빠른 2초 응답을 시도한 다음 70초 심층 처리 모드로 돌아갑니다.