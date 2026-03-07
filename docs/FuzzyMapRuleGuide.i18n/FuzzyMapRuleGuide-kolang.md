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
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'flags': re.IGNORECASE}),
]
```