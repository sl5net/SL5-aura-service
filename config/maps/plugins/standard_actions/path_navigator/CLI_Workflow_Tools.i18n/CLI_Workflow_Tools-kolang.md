# CLI 워크플로 도구 설치 가이드

경로 탐색기 플러그인의 일부 작업은 외부 명령줄 유틸리티를 사용하여 퍼지 검색을 수행하고, 파일을 나열하고, 클립보드를 조작합니다. 이러한 도구가 없으면 시스템 콘솔에 경고가 표시됩니다.

다음은 지원되는 각 운영 체제에 대한 설치 지침입니다.

## 필수 유틸리티

* **`fzf`**: 범용 명령줄 퍼지 파인더.
* **`find`** (또는 `fd`): 표준 파일 검색 유틸리티.
* **클립보드 도구**: 출력을 시스템 클립보드로 직접 파이프하는 데 사용됩니다.
* **Linux:** `xclip`(X11 환경 필요).
* **macOS:** `pbcopy`(사전 설치됨).
* **Windows:** `clip`(사전 설치됨).
* **`file`**: 전체 터미널 미리보기에 대한 파일 형식을 결정합니다.

---

## 설치 지침

### 1. 리눅스(아치/만자로)
시스템이 Manjaro에서 실행되므로 'pacman'을 사용하여 필요한 패키지를 설치할 수 있습니다.

```bash
sudo pacman -S fzf findutils xclip file
```



## 1. 빠른 파일 선택(Aura Command)

`path_navigator` 작업은 다음 Git 인식 `fzf` 명령을 사용합니다. 그 목적은 파일 경로를 시스템 클립보드에 직접 출력하는 것입니다.

**명령 논리:**
- Git 저장소 내에서 `git ls-files`를 사용합니다(무시된 파일 제외).
- 'find'로 돌아갑니다. - Git 저장소 외부에 f`를 입력하세요.
- `xclip -selectionclipboard`를 사용하여 선택한 경로를 클립보드에 출력합니다.

## 2. 빠른 파일 실행('k' 함수)

루프를 완료하려면 사용자 정의 셸 함수 'k'가 사용됩니다. 이 기능은 클립보드에서 경로를 가져와 즉시 `kate`에서 파일을 엽니다.

### 구현

셸의 구성 파일(예: `~/.bashrc`, `~/.zshrc`)에 다음 기능을 추가합니다.

```bash
# Function to open a file path from the system clipboard in Kate
function k {
    # Check if xclip is available
    if ! command -v xclip &> /dev/null; then
        echo "Error: xclip is required but not installed."
        return 1
    fi
    
    # 1. Get clipboard content
    CLIPBOARD_CONTENT=$(xclip -selection clipboard -o 2>/dev/null)
    
    # Check if clipboard is empty
    if [ -z "${CLIPBOARD_CONTENT}" ]; then
        echo "Error: Clipboard is empty. Nothing to open."
        return 1
    fi

    # 2. Check for multiline content (ensures only a single file path is used)
    LINE_COUNT=$(echo "${CLIPBOARD_CONTENT}" | wc -l)
    
    if [ "${LINE_COUNT}" -gt 1 ]; then
        echo "Error: Clipboard contains ${LINE_COUNT} lines. Only single-line file paths are supported."
        return 1
    fi
    
    # 3. Print the command before execution (User Feedback)
    echo "kate \"${CLIPBOARD_CONTENT}\""
    
    # 4. Final Execution
    # The double quotes around the content handle filenames with spaces correctly.
    # The '&' runs the command in the background, freeing the terminal.
    kate "${CLIPBOARD_CONTENT}" &
}
```

### 용법

1. 'path_navigator' 명령을 사용합니다(예: 트리거 도구에 'search file' 입력).
2. 원하는 파일(예: `src/main/config.py`)을 찾아 선택합니다.
3. 터미널에 'k'를 입력하고 **ENTER**를 누르세요.
4. 파일이 Kate에서 즉시 열립니다.
__CODE_BLOCK_2__