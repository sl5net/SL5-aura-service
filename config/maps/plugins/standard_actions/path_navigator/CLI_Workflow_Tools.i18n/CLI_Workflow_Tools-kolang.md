### 마크다운 문서: `STT/settings/maps/plugins/standard_actions/path_navigator/CLI_Workflow_Tools.md`

```markdown
CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY

# CLI Workflow Tools: FZF to Kate Integration

This document describes a high-efficiency command-line workflow that leverages the fuzzy file search implemented in the `path_navigator` plugin to quickly open files in the Kate editor.

## 1. Fast File Selection (Aura Command)

The `path_navigator` action uses the following Git-aware `fzf` command. Its purpose is to output a file path directly into the system clipboard.

**Command Logic:**
- Uses `git ls-files` inside a Git repository (excludes ignored files).
- Falls back to `find . -type f` outside a Git repository.
- Outputs the selected path to the clipboard using `xclip -selection clipboard`.

## 2. Fast File Execution (The 'k' Function)

To complete the loop, the custom shell function `k` is used. This function takes the path from the clipboard and instantly opens the file in `kate`.

### Implementation

Add the following function to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
# Kate에서 시스템 클립보드의 파일 경로를 여는 기능
함수 k {
# xclip이 사용 가능한지 확인
만약에 ! 명령 -v xclip &> /dev/null; 그 다음에
echo "오류: xclip이 필요하지만 설치되지 않았습니다."
1을 반환
fi
XSPACEbreakX
# 1. 클립보드 콘텐츠 가져오기
CLIPBOARD_CONTENT=$(xclip -선택 클립보드 -o 2>/dev/null)
XSPACEbreakX
# 클립보드가 비어 있는지 확인
if [ -z "${CLIPBOARD_CONTENT}" ]; 그 다음에
echo "오류: 클립보드가 비어 있습니다. 열 수 있는 항목이 없습니다."
1을 반환
fi

# 2. 여러 줄 내용 확인(단일 파일 경로만 사용되는지 확인)
LINE_COUNT=$(echo "${CLIPBOARD_CONTENT}" | wc -l)
XSPACEbreakX
if [ "${LINE_COUNT}" -gt 1 ]; 그 다음에
echo "오류: 클립보드에 ${LINE_COUNT}줄이 포함되어 있습니다. 한 줄 파일 경로만 지원됩니다."
1을 반환
fi
XSPACEbreakX
# 3. 실행 전 명령을 인쇄합니다(User Feedback)
echo "케이트 \"${CLIPBOARD_CONTENT}\""
XSPACEbreakX
# 4. 최종 실행
# 콘텐츠 주위의 큰따옴표는 공백이 포함된 파일 이름을 올바르게 처리합니다.
# '&'는 백그라운드에서 명령을 실행하여 터미널을 해제합니다.
케이트 "${CLIPBOARD_CONTENT}" &
}
```

### Usage

1.  Use the `path_navigator` command (e.g., type `search file` in your trigger tool).
2.  Find and select the desired file (e.g., `src/main/config.py`).
3.  In your terminal, type `k` and press **ENTER**.
4.  The file opens instantly in Kate.
```