# dotool – 설치 및 구성 (Manjaro / Arch 기반)

## 개요
`dotool`은 저수준 입력 시뮬레이션 유틸리티입니다. 'xdotool'과 달리 'uinput'을 통해 Linux 커널과 직접 상호작용하므로 **X11 및 Wayland**와 모두 호환됩니다.

---

## 설치 (만자로/아치)

### 1. 패키지 설치
```bash
pamac build dotool
# or via yay: yay -S dotool
```

### 2. 권한 및 udev 규칙
`dotool`이 루트 권한 없이 입력을 시뮬레이션하도록 허용하려면 사용자가 `input` 그룹의 일부여야 하고 udev 규칙이 활성화되어 있어야 합니다.

1. **그룹에 사용자 추가:** `sudo gpasswd -a $USER 입력`
2. **udev 규칙 생성:**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **udev 규칙을 다시 로드합니다:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**중요:** 그룹 변경 사항을 적용하려면 **로그아웃했다가 다시 로그인**해야 합니다.

---

## 프로젝트 구성(`config/settings.py`)

```python
# Override X11 default to use dotool (recommended for better layout stability)
x11_input_method_OVERRIDE = "dotool"

# Delay between keystrokes in milliseconds
# 2ms = Default, reliable for special characters and Umlauts
# 0ms = Maximum speed (Instant mode)
dotool_typedelay = 2
```

---

## 스크립트 구현

### 성능 최적화(FIFO)
모든 단어에 대해 새로운 `dotool` 인스턴스를 시작하는 것은 느립니다(~100ms 대기 시간). "인스턴트" 타이핑을 달성하기 위해 스크립트는 FIFO 파이프에서 읽는 지속적인 백그라운드 프로세스를 사용합니다.

```bash
# Setup in the main script
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

### 타이핑 기능
```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        # Pipe commands directly into the running background process
        printf 'typedelay %s\ntype %s\n' "$DOTOOL_TYPEDELAY" "$text" > /tmp/dotool_fifo
    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

---

## 문제 해결 및 참고 사항
- **누락된 문자:** 특수 문자(예: 움라우트)를 건너뛴 경우 `dotool_typedelay`를 5 또는 10으로 늘립니다.
- **애플리케이션 호환성:** 일부 앱(Electron, 브라우저)은 빠른 입력을 올바르게 등록하기 위해 더 높은 지연이 필요할 수 있습니다.
- **Wayland 지원:** `dotool`은 Wayland에 필요한 백엔드입니다. `xdotool`은 이를 지원하지 않습니다.
- **자동 대체:** `dotool`이 설치되지 않았거나 올바르게 구성되지 않은 경우 스크립트가 자동으로 `xdotool`로 대체됩니다.