# FUZZY_MAP 규칙 가이드

## 규칙 형식

```python
('replacement', r'regex_pattern', threshold, {'command_flags': re.IGNORECASE})
```

| 위치 | 이름 | 설명 |
|---|---|---|
| 1 | 교체 | 규칙이 일치한 후의 출력 텍스트 |
| 2 | 패턴 | 일치시킬 정규식 또는 퍼지 문자열 |
| 3 | 임계값 | 정규식 규칙의 경우: 무시됩니다. 퍼지 규칙의 경우: 최소 일치 점수(0–100) |
| 4 | 옵션 | 선택적 사전(아래 "옵션 참조" 참조). 기본값으로 `0`을 사용하거나 생략 |
### 원시 교체
기본적으로(`False`) 대체 문자열은 Python의 `re.sub()`에 의해 처리됩니다. 이는 `\1` 또는 `\2`와 같은 정규식 역참조를 사용하여 캡처된 그룹을 삽입하는 것을 지원합니다(예: `(r'\1', r'(\d)\s+(?=\d)', 95)`).
대체 항목이 여러 줄 문자열이거나 이스케이프되지 않은 백슬래시(예: 코드 템플릿 또는 경로)를 포함하고 있는 그대로 정확하게 보존해야 하는 경우 옵션 사전에서 `'raw_replacement': True`를 활성화하세요.
```python
(System_Instructions, r'^(system instructions)$', 10, {'command_flags': re.IGNORECASE, 'raw_replacement': True})
```

### 사용 가능한 사용자 구성 옵션:

* **`command_flags`** (정수): 패턴 컴파일 중에 사용되는 정규식 플래그입니다.
*예:* `{'command_flags': re.IGNORECASE}`
* **`raw_replacement`** (부울): `True`인 경우 대체 텍스트는 순수 문자열 리터럴로 처리되고 Python의 `re.sub` 백슬래시 구문 분석을 통해 무시됩니다. 이스케이프 처리되지 않은 백슬래시(`\`)가 있는 문자열이나 여러 줄 프롬프트에 매우 중요합니다.
*예:* `{'raw_replacement': True}`
* **`cache`** (부울): AURA 결과 캐시를 토글합니다. 동적 출력(예: 현재 시간, 무작위 농담)을 생성하는 규칙에 대해 'False'로 설정하면 모든 일치에서 새로 평가됩니다.
*예:* `{'캐시': 거짓}`
* **`skip_list`** (문자열 목록): 이 규칙이 일치할 때 건너뛸 후처리 파이프라인 모듈을 지정합니다.
*예:* `{'skip_list': ['LanguageTool']}`(문법 검사 건너뛰기)
* **`only_in_windows`**(정규식 문자열 목록): 활성 창 제목이 지정된 패턴 중 하나와 일치하는 경우에만 트리거되도록 규칙을 제한합니다.
*예:* `{'only_in_windows': [r'^Mozilla Firefox$', r'Chrome']}`
* **`exclude_windows`** (정규식 문자열 목록): 활성 창 제목이 지정된 패턴 중 하나와 일치하는 경우 규칙이 트리거되지 않도록 합니다.
*예:* `{'exclude_windows': [r'Terminal', r'Claude']}`
* **`window_ignore_case`** (부울): 창 일치(`only_in_windows` / `exclude_windows`)가 대소문자를 구분하지 않고(`True`) 또는 대소문자를 구분하여(`False`) 평가되는지 여부를 제어합니다. 생략하면 `config/settings.py`의 전역 설정 `LOWERCASE_WINDOW_TITLES`로 대체됩니다.
*예:* `{'window_ignore_case': False}`
* **`on_match_exec`** (경로/문자열 개체 목록): 이 규칙이 일치할 때 실행되어야 하는 스크립트/플러그인에 대한 경로입니다(포괄 규칙과 폴백 규칙에서 많이 사용됨).
*예:* `{'on_match_exec': [PROJECT_ROOT / 'scripts' / 'custom_action.py']}`

## 파이프라인 로직
- 규칙은 **하향식**으로 처리됩니다.


## 파이프라인 로직

- 규칙은 **하향식**으로 처리됩니다.
- **모든** 일치 규칙이 적용됩니다(누적).
- **fullmatch**(`^...$`)는 파이프라인을 즉시 중지합니다.
- 이전 규칙이 이후 규칙보다 우선합니다.

## 일반적인 패턴

### 단일 단어 일치(단어 경계)
```python
('Python', r'\bpython\b', 0, {'command_flags': re.IGNORECASE})
```

### 여러 변형 일치
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'command_flags': re.IGNORECASE})
```

### Fullmatch – 파이프라인을 중지합니다.
```python
('hello koan', r'^.*$', 0, {'command_flags': re.IGNORECASE})
```
⚠️ **모든 항목**과 일치합니다. 파이프라인은 여기서 멈춥니다. 이전 규칙은 여전히 우선순위를 갖습니다.

### 입력 시작 일치
```python
('Note: ', r'^notiz\b', 0, {'command_flags': re.IGNORECASE})
```

### 정확한 구문 일치
```python
('New York', r'\bnew york\b', 0, {'command_flags': re.IGNORECASE})
```

## 파일 위치

| 파일 | 단계 | 설명 |
|---|---|---|
| `FUZZY_MAP_pre.py` | 사전 언어 도구 | 맞춤법 검사 전에 적용됨 |
| `FUZZY_MAP.py` | 포스트 언어 도구 | 맞춤법 검사 후 적용 |
| 'PUNCTUATION_MAP.py' | 사전 언어 도구 | 구두점 규칙 |

## 팁

- **일반** 규칙 앞에 **특정** 규칙을 추가하세요.
- 추가 처리를 모두 중지하려는 경우에만 `^...$` 전체 일치를 사용하세요.
- `FUZZY_MAP_pre.py`는 철자 검사 전 수정에 이상적입니다.
- Aura 콘솔에서 `s your test input`을 사용하여 규칙을 테스트합니다.
- 백업은 '.peter_backup'으로 자동 생성됩니다.

## 예

```python
FUZZY_MAP_pre = [
    # Correct a common STT mistake
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'command_flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'command_flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'command_flags': re.IGNORECASE}),
]
```

## 첫 번째 규칙 - 단계별

1. `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`를 엽니다.
2. `FUZZY_MAP_pre = [...]` 안에 규칙을 추가하세요.
3. 저장 - Aura가 자동으로 다시 로드되므로 다시 시작할 필요가 없습니다.
4. 트리거 문구를 받아쓰고 실행되는 것을 지켜보세요.


## 권장 파일 구조

긴 댓글 블록 **앞에** 규칙을 입력하세요.
```python
# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re  # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('My Rule', r'my rule', 0, {'command_flags': re.IGNORECASE}),
]
# ============================================================
# Longer explanations, task descriptions, notes...
# can be as long as needed — they go AFTER the rules.
# ============================================================
```

**이유는 무엇입니까?** Aura의 Auto-Fix는 파일의 처음 ~1KB만 검사합니다.
규칙이 긴 헤더 뒤에 나타나는 경우 자동 수정에서는 해당 규칙을 찾거나 복구할 수 없습니다.
1행의 경로 주석도 권장됩니다. 이는 사람이 파일을 빠르게 식별하는 데 도움이 됩니다.