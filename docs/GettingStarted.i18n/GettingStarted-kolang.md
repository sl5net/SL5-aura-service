# SL5 Aura 시작하기

> **전제 조건:** 설정 스크립트를 완료하고 단축키를 구성했습니다.
> 그렇지 않은 경우 [Installation section in README.md](../../README.i18n/README-kolang.md#installation)를 참조하세요.

---

## 0단계: 단축키 구성

플랫폼을 선택하세요:

**Linux/macOS** — [CopyQ](https://github.com/hluk/CopyQ)를 설치하고 전역 단축키를 사용하여 명령을 만듭니다.
```bash
touch /tmp/sl5_record.trigger
```

**Windows** — [AutoHotkey v2](https://www.autohotkey.com/) 또는 CopyQ를 사용합니다. 설치 스크립트는 두 가지를 모두 자동으로 설치합니다.
트리거 파일은 `c:\tmp\sl5_record.trigger`입니다.

> 전체 세부정보: [README.md#configure-your-hotkey](../../README.i18n/README-kolang.md#configure-your-hotkey)

## 1단계: 첫 번째 받아쓰기

1. Aura를 시작합니다(아직 실행 중이 아닌 경우).
   ```bash
   ./scripts/restart_venv_and_run-server.sh
   ```
시작음이 들릴 때까지 기다립니다. 이는 Aura가 준비되었음을 의미합니다.

2. 텍스트 필드(편집기, 브라우저, 터미널)를 클릭합니다.
3. 단축키를 누르고 **"Hello World"**라고 말한 후 단축키를 다시 누릅니다.
4. 텍스트가 나타나는지 확인하세요.

> **아무 일도 일어나지 않았나요?** `log/aura_engine.log`에서 오류를 확인하세요.
> CachyOS/Arch에 대한 일반적인 수정: `sudo pacman -S mimalloc`

---

## 2단계: 첫 번째 규칙 작성

개인 규칙을 추가하는 가장 빠른 방법:

1. `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`를 엽니다.
2. `FUZZY_MAP_pre = [...]` 안에 규칙을 추가합니다.
   ```python
   ('Hello World', r'hello world', 0, {'flags': re.IGNORECASE})
   #  ^ output        ^ pattern        ^ threshold (ignored for regex)
   ```
3. **저장** — Aura가 자동으로 다시 로드됩니다. 다시 시작할 필요가 없습니다.
4. 'hello world'를 받아쓰고 'Hello World'가 되는 것을 지켜보세요.

> 전체 규칙 참조는 `docs/FuzzyMapRuleGuide.md`를 참조하세요.

### Oma-Modus(초보자 지름길)

아직 정규식을 모르시나요? 괜찮아요.

1. 샌드박스에서 빈 `FUZZY_MAP_pre.py`를 엽니다.
2. 한 줄에 일반 단어만 작성합니다(따옴표나 튜플 없음).
   ```
   raspberry
   ```
3. 저장 - 자동 수정 시스템이 간단한 단어를 감지하여 자동으로
이를 유효한 규칙 항목으로 변환합니다.
4. 그런 다음 대체 텍스트를 수동으로 편집할 수 있습니다.

이를 **Oma-Modus**라고 하며, 없이 결과를 원하는 사용자를 위해 설계되었습니다.
정규식을 먼저 배우세요.

---

## 3단계: Koans로 배우기

Koans는 각각 하나의 개념을 가르치는 작은 연습입니다.
그들은 `configmaps/koans deutsch/`와 `configmaps/koans english/`에 살고 있습니다.

여기에서 시작하세요:

| 폴더 | 당신이 배우는 것 |
|---|---|
| `00_koan_oma-modus` | 자동 수정, 정규식 없는 첫 번째 규칙 |
| `01_koan_erste_schritte` | 첫 번째 규칙, 파이프라인 기본 |
| `02_koan_listen` | 목록 작업 |
| `03_koan_schwierige_namen` | 인식하기 어려운 이름에 대한 퍼지 매칭 |
| `04_koan_kleine_helfer` | 유용한 단축키 |

각 koan 폴더에는 주석이 달린 예제가 포함된 `FUZZY_MAP_pre.py`가 포함되어 있습니다.
규칙의 주석 처리를 제거하고, 저장하고, 트리거 문구를 지시하면 완료됩니다.

---

## 4단계: 더 나아가

| 무엇 | 어디 |
|---|---|
| 전체 규칙 참조 | `docs/FuzzyMapRuleGuide.md` |
| 나만의 플러그인 만들기 | `docs/CreatingNewPluginModules.md` |
| 규칙에서 Python 스크립트 실행 | `docs/advanced-scripting.md` |
| DEV_MODE + 로그 필터 설정 | `docs/Developer_Guide/dev_mode_setup.md` |
| 컨텍스트 인식 규칙(`only_in_windows`) | `docs/FuzzyMapRuleGuide.md` |