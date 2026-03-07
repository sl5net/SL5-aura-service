# 자동 수정 모듈(빠른 규칙 입력 모드)

## 기능

지도 파일에 일반 단어(따옴표나 Python 구문 제외)를 입력하는 경우
`FUZZY_MAP_pre.py`와 같이 시스템은 이를 자동으로 유효한 규칙으로 변환합니다.

이는 새로운 규칙을 생성하는 가장 빠른 방법입니다. 형식을 기억할 필요가 없습니다.

## 예

`FUZZY_MAP_pre.py`에 다음을 입력합니다.

```
oma
```

자동 수정 모듈이 `NameError`(단순한 단어, 유효한 Python이 아님)를 감지합니다.
파일을 자동으로 다음으로 변환합니다.

```python
# config/maps/.../de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('oma', 'oma'),
]
```

이제 실제로 필요한 대로 규칙을 편집합니다.

```python
('Oma', 'oma'),              # capitalize
('Großmutter', 'oma'),       # synonym
('Thomas Müller', 'thomas'), # from a phone book
```

## 작동 방식

`scripts/py/func/auto_fix_module.py` 모듈이 자동으로 트리거됩니다.
Aura가 지도 파일을 로드하는 동안 'NameError'를 감지한 경우.

그런 다음:
1. 올바른 파일 경로 헤더를 추가합니다.
2. 누락된 경우 `import re`를 추가합니다.
3. `FUZZY_MAP_pre = [` 목록 정의를 추가합니다.
4. 순수 단어를 `('word', 'word'),` 튜플로 변환합니다.
5. `]`로 목록을 닫습니다.

## 규칙 및 제한

- **1KB**(안전 제한)보다 작은 파일에서만 작동합니다.
- 적용 대상: `FUZZY_MAP.py`, `FUZZY_MAP_pre.py`, `PUNCUATION_MAP.py`
- 파일은 유효한 언어 폴더에 있어야 합니다(예: `de-DE/`)
- 한 번에 여러 단어에 대해 작동합니다(예: 전화번호부 목록에서).

## `# too<-from` 주석

이 설명은 규칙 방향을 상기시키기 위해 자동으로 추가됩니다.

```
too <- from
```

의미: **출력**(역시) ← **입력**(으로부터). 교체가 먼저입니다.

`PUNCTUATION_MAP.py`의 경우 방향이 반대입니다: `# from->too`

## 목록에서 대량 입력

한 번에 여러 단어를 붙여넣을 수 있습니다.

```
thomas
maria
berlin
```

각각의 단어는 고유한 규칙이 됩니다.

```python
('thomas', 'thomas'),
('maria', 'maria'),
('berlin', 'berlin'),
```

그런 다음 필요에 따라 각 교체를 편집합니다.

## 파일: `scripts/py/func/auto_fix_module.py`