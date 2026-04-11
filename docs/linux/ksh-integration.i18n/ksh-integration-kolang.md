# Ksh(Korn Shell) 통합

STT(Speech-to-Text) CLI와 더 쉽게 상호작용하려면 `~/.kshrc`에 바로가기 기능을 추가하면 됩니다. 이렇게 하면 터미널에 '질문'을 입력하기만 하면 됩니다.

## 설정 지침

1. 원하는 편집기를 사용하여 Ksh 구성을 엽니다.
   ```bash
   nano ~/.kshrc
   kate ~/.kshrc
   ```

2. 파일 끝에 다음 블록을 붙여넣습니다.

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

3. Ksh가 구성 파일을 로드하는지 확인하세요. `~/.profile`에 이를 추가하거나 확인하세요.
   ```ksh
   export ENV="$HOME/.kshrc"
   ```

4. 구성을 다시 로드합니다.
   ```ksh
   . ~/.kshrc
   ```

## Ksh 관련 참고 사항

- Ksh는 `function name { }` 및 `name() { }` 구문을 모두 지원합니다. 여기서는 명확성을 위해 'function' 키워드를 사용했습니다.
- `local`은 모든 Ksh 변형(예: `ksh88`)에서 지원되지 **않습니다**. 따라서 위 함수의 변수는 `local` 없이 선언됩니다. `mksh` 또는 `ksh93`을 사용하는 경우 `typeset`을 대신 사용할 수 있습니다: `typeset TEMP_FILE=$(mktemp)`.
- `ENV` 변수는 `.bashrc`와 유사하게 대화형 세션을 위한 파일 Ksh 소스를 제어합니다.

## 특징

- **동적 경로**: `/tmp` 마커 파일을 통해 프로젝트 루트를 자동으로 찾습니다.
- **자동 재시작**: 백엔드가 다운되면 'start_service' 및 로컬 Wikipedia 서비스 실행을 시도합니다.
- **스마트 타임아웃**: 먼저 빠른 2초 응답을 시도한 다음 70초 심층 처리 모드로 돌아갑니다.