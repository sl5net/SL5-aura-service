# 개발자 팁: 콘솔 출력을 클립보드에 자동으로 복사

**범주:** Linux/셸 생산성XSPACEbreakX
**플랫폼:** Linux(zsh + Konsole/KDE)

---

## 문제

AI 도우미와 작업할 때 터미널 출력을 복사하여 채팅에 붙여넣어야 하는 경우가 많습니다. 이는 일반적으로 다음을 의미합니다.
1. 명령 실행
2. 마우스로 출력 선택
3. 복사
4. 브라우저로 전환
5. 붙여넣기

너무 많은 단계입니다.

---

## 해결책: `preexec` / `precmd`를 통한 자동 캡처

이것을 `~/.zshrc`에 추가하세요:

```bash
# === AUTO-OUTPUT LOGGER ===
# Automatically saves console output to ~/t.txt and copies to clipboard.
# Toggle: set AUTO_CLIPBOARD=true/false
AUTO_CLIPBOARD=true

# Redirect stdout+stderr to ~/t.txt before each command
preexec() {
    case "$1" in
        sudo*|su*) return ;;
        *) exec > >(tee ~/t.txt) 2>&1 ;;
    esac
}


precmd() {
    exec >/dev/tty 2>&1
    if [ "$AUTO_CLIPBOARD" = "true" ] && [ -s ~/t.txt ]; then
        cleaned=$(cat ~/t.txt \
            | sed 's/\][0-9]*;[^]]*\][0-9]*;//g; s/^[0-9]*;//g' \
            | sed "s|$HOME|~|g" \
            | sed 's/[^[:print:]]//g' \
            | grep -v '^$')
        if [ -n "$cleaned" ]; then
            echo "$cleaned" | xclip -selection clipboard
            echo "[📋 In Zwischenablage kopiert]"
        fi
    fi
}

```

그런 다음 다시 로드하십시오.
```bash
source ~/.zshrc
```

### 결과

모든 명령 후 출력이 자동으로 클립보드에 저장되므로 **Ctrl+V**를 사용하여 AI 채팅에 붙여넣을 수 있습니다.

출력은 참조용으로 항상 `~/t.txt`에 저장됩니다.

---

## 작동 방식

| 부품 | 그것이 하는 일 |
|------|-------------|
| `preexec()` | 각 명령 전에 실행되고 출력을 `~/t.txt`로 리디렉션 |
| `precmd()` | 각 명령 후에 실행되고, stdout을 복원하고 클립보드에 복사합니다. |
| `티 ~/t.txt` | 터미널에 계속 표시하면서 출력을 파일에 저장 |
| `sed '...'` | KDE Konsole 제목 이스케이프 시퀀스(`]2;...` `]1;`)를 제거합니다.
| `xclip` | 정리된 출력을 클립보드에 복사 |

---

## 요구사항

```bash
# Install xclip if not present
sudo pacman -S xclip       # Manjaro/Arch
sudo apt install xclip     # Ubuntu/Debian
```

---

## ⚠️ 하지 말아야 할 일

`fc -ln -1 |을 사용하지 **마세요** bash`를 사용하여 마지막 명령을 다시 실행하세요.

```bash
# ❌ DANGEROUS - do not use!
precmd() {
    output=$(fc -ln -1 | bash 2>&1)  # Re-executes last command!
    echo "$output" | xclip -selection clipboard
}
```

이렇게 하면 모든 명령이 완료된 후 다시 실행되어 파괴적인 부작용이 발생할 수 있습니다. 예를 들어 파일 덮어쓰기, `git commit` 다시 실행, `sed -i` 다시 실행 등이 있습니다.

위의 `preexec`/`precmd` 접근 방식은 **실행 중** 출력을 캡처하여 안전하고 안정적입니다.