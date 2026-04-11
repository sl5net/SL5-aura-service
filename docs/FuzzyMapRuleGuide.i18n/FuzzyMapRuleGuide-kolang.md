# FUZZY_MAP 규칙 가이드

## 규칙 형식

```python
('replacement', r'regex_pattern', threshold, {'flags': re.IGNORECASE})
```

| 위치 | 이름 | 설명 |
|---|---|---|
| 1 | 교체 | 규칙이 일치한 후의 출력 텍스트 |
| 2 | 패턴 | 일치시킬 정규식 또는 퍼지 문자열 |
| 3 | 임계값 | 정규식 규칙에서는 무시됩니다. 퍼지 일치에 사용됩니다(0–100) |
| 4 | 플래그 | 대소문자를 구분하지 않는 경우 `{'flags': re.IGNORECASE}`, 대소문자를 구분하는 경우 `0` |

## 파이프라인 로직

- 규칙은 **하향식**으로 처리됩니다.
- **모든** 일치 규칙이 적용됩니다(누적).
- **fullmatch**(`^...$`)는 파이프라인을 즉시 중지합니다.
- 이전 규칙이 이후 규칙보다 우선합니다.

## 일반적인 패턴

### 단일 단어 일치(단어 경계)
```python
('Python', r'\bpython\b', 0, {'flags': re.IGNORECASE})
```

### 여러 변형 일치
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'flags': re.IGNORECASE})
```

### Fullmatch – 파이프라인을 중지합니다.
```python
('hello koan', r'^.*$', 0, {'flags': re.IGNORECASE})
```
⚠️ **모든 항목**과 일치합니다. 파이프라인은 여기서 멈춥니다. 이전 규칙은 여전히 우선순위를 갖습니다.

### 입력 시작 일치
```python
('Note: ', r'^notiz\b', 0, {'flags': re.IGNORECASE})
```

### 정확한 구문 일치
```python
('New York', r'\bnew york\b', 0, {'flags': re.IGNORECASE})
```

## 파일 위치

| 파일 | 단계 | 설명 |
|---|---|---|
| `FUZZY_MAP_pre.py` | 사전 언어 도구 | 맞춤법 검사 전에 적용됨 |
| `FUZZY_MAP.py` | 포스트 언어 도구 | 맞춤법 검사 후 적용 |
| PUNCTUATION_MAP.py` | 사전 언어 도구 | 구두점 규칙 |

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
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'flags': re.IGNORECASE}),
]
```

## 첫 번째 규칙 — 단계별

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
    ('My Rule', r'my rule', 0, {'flags': re.IGNORECASE}),
]
# ============================================================
# Longer explanations, task descriptions, notes...
# can be as long as needed — they go AFTER the rules.
# ============================================================
```

**이유는 무엇입니까?** Aura의 Auto-Fix는 파일의 처음 ~1KB만 검사합니다.
규칙이 긴 헤더 뒤에 나타나는 경우 자동 수정에서는 해당 규칙을 찾거나 복구할 수 없습니다.
1행의 경로 주석도 권장됩니다. 이는 사람이 파일을 빠르게 식별하는 데 도움이 됩니다.