# Wayland의 dotool — 설정 및 문제 해결

Aura가 Wayland의 다른 애플리케이션에 텍스트를 입력하려면 'dotool'이 필요합니다.
`xdotool`과 달리 `uinput`을 통해 Linux 커널과 직접 통신합니다.
**X11과 Wayland** 모두에서 작동합니다.

X11에서는 `xdotool`이 기본적으로 사용됩니다. `dotool`은 X11에서는 선택 사항이지만
더 나은 레이아웃 안정성을 위해 권장됩니다(특히 Umlauts의 경우).

---

## 1. dotool 설치

**아치/만자로/CachyOS(AUR):**
```bash
yay -S dotool
# or:
pamac build dotool
```

**Ubuntu/Debian(저장소에서 사용 가능한 경우):**
```bash
sudo apt install dotool
```

**저장소에 없는 경우 — 소스에서 빌드:**
```bash
sudo pacman -S go        # or: sudo apt install golang
git clone https://git.sr.ht/~geb/dotool
cd dotool
make
sudo make install
```

---

## 2. dotool이 루트 없이 실행되도록 허용(필수)

`dotool`은 `/dev/uinput`에 액세스해야 합니다. 이것이 없으면 자동으로 실패합니다.

```bash
# Add your user to the input group:
sudo gpasswd -a $USER input

# Create the udev rule:
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules

# Reload rules:
sudo udevadm control --reload-rules && sudo udevadm trigger
```

그룹 변경 후 적용을 위해서는 **재로그인**이 필요합니다.

---

## 3. 설치 확인

```bash
# Test that dotool can type (focus a text field first):
echo "type hello" | dotool

# Check that the input group is active in your session:
groups | grep input
```

`groups`에 `input`이 표시되지 않으면 로그아웃했다가 다시 로그인(또는 재부팅)하세요.

---

## 4. Aura가 dotool을 사용하는 방법

Aura의 `type_watcher.sh`는 자동으로 다음을 수행합니다.

- `$WAYLAND_DISPLAY`를 통해 Wayland를 감지하고 `dotool`을 선택합니다.
- `dotoold` 데몬이 존재하고 실행되고 있지 않으면 백그라운드에서 시작합니다.
- `dotool`이 설치되지 않은 경우 `xdotool`로 대체됩니다(X11에만 해당)
- 활성 Vosk 모델에서 키보드 레이아웃을 설정합니다(예: `de` → `XKB_DEFAULT_LAYOUT=de`)

수동 데몬 관리가 필요하지 않습니다. Aura가 시작 시 이를 처리합니다.

---

## 5. 문제 해결

**Aura는 내용을 기록하지만 텍스트가 나타나지 않습니다.**
```bash
# Check if dotool is installed:
command -v dotool

# Check group membership:
groups | grep input

# Test manually (focus a text field first):
echo "type hello" | dotool

# Check the watcher log:
tail -30 log/type_watcher.log
```

**누락되거나 왜곡된 문자(특히 움라우트):**

`config/settings_local.py`에서 입력 지연을 늘립니다.
```python
dotool_typedelay = 5   # default is 2, try 5 or 10
```

**dotool은 터미널에서는 작동하지만 Aura에서는 작동하지 않습니다.**

새 터미널뿐만 아니라 데스크톱 세션에서 `input` 그룹이 활성화되어 있는지 확인하세요.
`gpasswd` 후에는 전체 재로그인이 필요합니다.

**X11에서 강제 dotool**(선택 사항, 더 나은 레이아웃 안정성을 위해):
```python
# config/settings_local.py
x11_input_method_OVERRIDE = "dotool"
```

---

## 6. dotool을 설치할 수 없는 경우 대체

시스템에서 `dotool`을 사용할 수 없는 경우 Aura는 X11의 `xdotool`로 대체됩니다.
`dotool`이 없는 Wayland에서는 입력이 **지원되지 않습니다** — 이것은 Wayland입니다
보안 제한은 Aura 제한이 아닙니다.

특정 합성기에서 작동할 수 있는 대체 도구:

| 도구 | 작업 |
|---|---|
| `xdotool` | X11 전용 |
| `dotool` | X11 + Wayland(권장) |
| `ydotool` | X11 + Wayland(대체) |

수동 해결 방법으로 `ydotool`을 사용하려면:
```bash
sudo pacman -S ydotool    # or: sudo apt install ydotool
sudo systemctl enable --now ydotool
```
참고: Aura는 `ydotool`을 기본적으로 통합하지 않습니다. 수동 구성이 필요합니다.