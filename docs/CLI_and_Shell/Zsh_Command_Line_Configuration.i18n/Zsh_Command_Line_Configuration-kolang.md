이 문서에는 명령줄을 통해 Python 서비스와 상호 작용하기 위한 최종적이고 검증된 Zsh 구성이 요약되어 있습니다.

구성은 안전한 출력부터 즉시 실행까지 서비스에 액세스하기 위한 세 가지 고유한 방법을 제공합니다.

## Zsh 명령줄 구성 요약

### 1. 구성 파일

아래의 모든 코드를 **`~/.zshrc`** 파일에 붙여넣어야 합니다. 변경 후 **`source ~/.zshrc`**를 수행하거나 새 터미널 세션을 여는 것을 잊지 마세요.

### 2. 최종 코드 블록

이 블록은 세 가지 필수 기능을 정의합니다. 여기에는 이전에 발생한 충돌 오류를 방지하는 데 필요한 'unalias' 명령이 포함되어 있습니다.

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

### 3. 세 가지 명령어의 사용법

| 명령 | 기능성 | 안전수준 | 예 |
| :--- | :--- | :--- | :--- |
| **`sl`** | **표준 출력:** 서비스를 실행하고 전체 출력을 콘솔에 직접 인쇄합니다. | **안전** | `sl 집이란 무엇인가`(인쇄: "집은...") |
| **`slz`** | **안전 실행 준비:** 서비스를 실행하고 출력(예: 셸 명령)을 검토 또는 실행할 준비가 된 Zsh 입력 줄에 붙여넣습니다. | **안전/준비** | `slz git` (붙여넣기: `git add . && git commit...` **그러나 실행하지는 않습니다**.) |
| **`slxXsoidfuasdzof`** | **즉시 실행:** 서비스를 실행하고 출력을 즉시 셸 명령으로 실행합니다. 보안 조치로 비밀스러운 이름을 사용하십시오. | **위험** | `slxXsoidfuasdzof git`(`git add...` 명령을 즉시 실행합니다.) |