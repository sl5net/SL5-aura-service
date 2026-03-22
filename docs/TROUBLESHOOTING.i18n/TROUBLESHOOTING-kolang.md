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
| `'objgraph'라는 모듈이 없습니다` | `.venv`가 다시 생성되었습니다 — 다시 설치: `pip install -r 요구사항.txt` |
| `이미 사용 중인 주소` | 기존 프로세스 종료: `pkill -9 -f aura_engine` |
| '모델을 찾을 수 없음' | 누락된 모델을 다운로드하려면 설치를 다시 실행하세요. |

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

파일이 생성되지 않으면 단축키 구성(CopyQ/AHK)이 작동하지 않는 것입니다.
[README.md](../../README.i18n/README-kolang.md#configure-your-hotkey)의 단축키 설정 섹션을 참조하세요.

---

## 문제: 텍스트가 나타나지만 수정 사항이 없습니다.

**증상:** 받아쓰기가 작동하지만 모든 내용이 소문자로 유지되고 문법 수정이 이루어지지 않습니다.

**LanguageTool이 실행 중인지 확인하세요.**
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

**증상:** CPU 100%, 팬이 최고 속도로 작동 중, 'plugins.zip'이 멈추지 않고 커집니다.

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