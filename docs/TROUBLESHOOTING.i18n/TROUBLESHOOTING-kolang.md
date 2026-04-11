# SL5 Aura 문제 해결

## 빠른 진단

항상 여기서 시작하세요:

```bash
# Check the main log:
tail -50 log/aura_engine.log

# Is Aura running?
pgrep -a -f aura_engine.py

# Is the file watcher running?
pgrep -a type_watcher
```

---

## 문제: Aura가 시작되지 않습니다.

**증상:** 시작 소리가 나지 않고 'pgrep'에 프로세스가 표시되지 않습니다.

**로그를 확인하세요:**
```bash
tail -30 log/aura_engine.log
```

**일반적인 원인:**

| 로그 오류 | 수정 |
|---|---|
| `ModuleNotFoundError` | 설정 스크립트를 다시 실행하십시오: `bash setup/manjaro_arch_setup.sh` |
| `'objgraph'라는 모듈이 없습니다` | `.venv`가 다시 생성되었습니다 — 다시 설치: `pip install -r 요구 사항.txt` |
| `이미 사용 중인 주소` | 기존 프로세스 종료: `pkill -9 -f aura_engine` |
| '모델을 찾을 수 없음' | 누락된 모델을 다운로드하려면 설정을 다시 실행하세요. |
| `pygame.mixer를 사용할 수 없음` | 아래의 "시작 시 소리가 나지 않음"을 참조하세요 |

---

## 문제: 시작 시 소리가 나지 않음(pygame.mixer)

**증상:** `pygame.mixer`에 대한 경고 또는 오류를 사용할 수 없습니다. 아우라가 시작된다
하지만 소리가 나지 않습니다.

**원인:** 시스템의 파이게임 빌드에 오디오 지원 또는 SDL2가 포함되어 있지 않습니다.
오디오 라이브러리가 없습니다.

**Arch/Manjaro 수정:**
```bash
sudo pacman -S sdl2_mixer
pip install pygame-ce --upgrade
```

**Ubuntu/Debian 수정:**
```bash
sudo apt install libsdl2-mixer-2.0-0
pip install pygame-ce --upgrade
```

Aura는 소리 없이 계속 작동합니다. 이는 치명적인 오류가 아닙니다.

---

## 문제: 첫 번째 받아쓰기 후 Aura가 충돌합니다.

**증상:** 한 번 작동한 후 자동으로 종료됩니다.

**표준 오류 확인:**
```bash
cat /tmp/aura_stderr.log | tail -30
```

**`Segmentation Fault` 또는 `double free`가 표시되는 경우:**

이는 glibc 2.43+(CachyOS, 최신 Arch)가 설치된 시스템에서 알려진 문제입니다.

```bash
sudo pacman -S mimalloc
```

mimalloc은 설치된 경우 시작 스크립트에 의해 자동으로 사용됩니다. 활성화되어 있는지 확인하세요. 시작 시 다음이 표시되어야 합니다.
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

---

## 문제: 트리거 키가 아무 것도 하지 않습니다.

**증상:** 단축키를 눌렀지만 아무 일도 일어나지 않습니다. 소리도 없고 텍스트도 없습니다.

**파일 감시자가 실행 중인지 확인하세요.**
```bash
pgrep -a type_watcher
```

아무것도 나타나지 않으면 Aura를 다시 시작하십시오.
```bash
./scripts/restart_venv_and_run-server.sh
```

**트리거 파일이 생성되고 있는지 확인하세요.**
```bash
ls -la /tmp/sl5_record.trigger
```

파일이 생성되지 않으면 단축키가 작동하지 않는 것입니다. 아래를 참조하세요.

---

## 문제: Wayland에서 단축키가 작동하지 않습니다.

**증상:** CopyQ가 설치 및 구성되었지만 단축키를 누르면
Wayland 세션에는 아무것도 없습니다.

**원인:** CopyQ 글로벌 단축키는 다음이 없으면 Wayland에서 안정적으로 작동하지 않습니다.
추가 구성. 이는 KDE Plasma, GNOME 및 기타 항목에 영향을 미칩니다.
Wayland 컴포지터.

### 옵션 1: KDE 시스템 설정(KDE 플라즈마에 권장)

1. **시스템 설정 → 바로가기 → 사용자 정의 바로가기**를 엽니다.
2. **명령/URL** 유형의 새 바로가기를 만듭니다.
3. 명령을 다음과 같이 설정합니다.
   ```bash
   touch /tmp/sl5_record.trigger
   ```
4. 원하는 키 조합을 지정하세요(예: `F9` 또는 `Ctrl+Alt+Space`)

### 옵션 2: dotool(모든 Wayland 컴포지터에서 작동)

```bash
# Install dotool:
sudo pacman -S dotool        # Arch/Manjaro
# or
sudo apt install dotool      # Ubuntu (if available)
```

그런 다음 데스크탑의 바로 가기 관리자를 사용하여 다음을 실행하십시오.
```bash
touch /tmp/sl5_record.trigger
```

### 옵션 3: ydotool

```bash
sudo pacman -S ydotool
sudo systemctl enable --now ydotool
```

그런 다음 실행되도록 바로가기를 구성합니다.
```bash
touch /tmp/sl5_record.trigger
```

### 옵션 4: GNOME(dconf / GNOME 설정 사용)

1. **설정 → 키보드 → 사용자 정의 단축키**를 엽니다.
2. 다음 명령을 사용하여 새 바로가기를 추가합니다.
   ```bash
   touch /tmp/sl5_record.trigger
   ```
3. 키 조합 지정

### 옵션 5: Wayland 수정 사항이 포함된 CopyQ

일부 Wayland 합성기는 다음과 같이 시작하면 CopyQ가 작동하도록 허용합니다.
```bash
QT_QPA_PLATFORM=xcb copyq
```

이로 인해 CopyQ는 글로벌 단축키를 지원하는 XWayland를 사용하게 됩니다.

---

## 문제: 텍스트가 나타나지만 수정 사항이 없습니다.

**증상:** 받아쓰기가 작동하지만 모든 내용이 소문자로 유지되고 문법 수정이 이루어지지 않습니다.

**LanguageTool이 실행 중인지 확인:**
```bash
curl -s http://127.0.0.1:8082/v2/languages | head -5
```

오류가 반환되면 LanguageTool이 실행되고 있지 않은 것입니다. 아우라가 시작해야 해
자동으로 - LanguageTool과 관련된 오류 로그를 확인하십시오.

```bash
grep -i "languagetool\|LT\|8082" log/aura_engine.log | tail -10
```

**LanguageTool 로그 확인:**
```bash
cat log/languagetool_server.log | tail -20
```

---

## 문제: DEV_MODE에서 Aura가 중단됩니다.

**증상:** `DEV_MODE = 1`인 경우 Aura가 첫 번째 트리거 이후 멈추고 중지됩니다.
응답.

**원인:** 여러 스레드의 높은 로그 볼륨으로 인해 로깅 시스템이 과부하됩니다.

**수정:** `config/filters/settings_local_log_filter.py`에 로그 필터를 추가하세요.

```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"window_title",
    r":st:",
]
LOG_EXCLUDE = []
```

파일 저장 — Aura는 필터를 자동으로 다시 로드합니다. 다시 시작할 필요가 없습니다.

---

## 문제: 플러그인.zip이 끝없이 증가함/높은 CPU

**증상:** 100% CPU, 팬이 최고 속도로 작동 중, 'plugins.zip'이 멈추지 않고 커집니다.

**원인:** 보안 패커가 무한 루프에서 파일을 다시 패키지하고 있습니다.

**수정:** `.blob` 및 `.zip` 파일이 타임스탬프 스캔에서 제외되는지 확인하세요.
86행 주위의 `scripts/py/func/secure_packer_lib.py`를 확인하세요.

```python
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
    continue
```

이 줄이 누락된 경우 추가하세요.

---

## 문제: 규칙이 실행되지 않음

**증상:** 트리거 문구를 지시했지만 규칙이 아무 작업도 수행하지 않습니다.

**체크리스트:**

1. 규칙이 올바른 파일에 있습니까? (`FUZZY_MAP_pre.py` = LanguageTool 이전,
`FUZZY_MAP.py` = 이후)
2. 지도 파일이 저장되어 있나요? 저장 시 Aura가 다시 로드됩니다. 로그를 확인하세요.
'성공적으로 다시 로드되었습니다'.
3. 패턴이 Vosk가 실제로 기록한 것과 일치합니까? 로그를 확인하세요.
원시 전사:
   ```bash
   grep "Yielding chunk" log/aura_engine.log | tail -5
   ```
4. `only_in_windows`가 설정되어 있는데 잘못된 창이 활성화되어 있습니까?
5. 보다 일반적인 규칙이 먼저 일치합니까? 규칙은 위에서 아래로 처리됩니다.
일반적인 규칙보다 구체적인 규칙을 두십시오.

---

## 버그 신고를 위한 로그 수집

문제를 보고할 때 다음을 포함하십시오.

```bash
# Last 100 lines of main log:
tail -100 log/aura_engine.log

# Crash output:
cat /tmp/aura_stderr.log

# System info:
uname -a
python3 --version
```

게시 대상: [GitHub Issues](https://github.com/sl5net/SL5-aura-service/issues)