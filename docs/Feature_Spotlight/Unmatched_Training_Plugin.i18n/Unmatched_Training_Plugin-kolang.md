# 일치하지 않는 교육 플러그인(`1_collect_unmatched_training`)

## 목적

이 플러그인은 인식되지 않은 음성 입력을 자동으로 수집하여 추가합니다.
퍼지 맵 정규식의 새로운 변형입니다. 이를 통해 시스템은 "자체 훈련"을 할 수 있습니다.
시간이 지남에 따라 비교할 수 없는 인식 결과를 통해 학습합니다.

## 작동 방식

1. `COLLECT_UNMATCHED` 포괄 규칙은 일치하는 다른 규칙이 없을 때 실행됩니다.
2. `collect_unmatched.py`는 일치하는 텍스트와 함께 `on_match_exec`를 통해 호출됩니다.
3. `FUZZY_MAP_pre.py` 호출의 정규식은 자동으로 확장됩니다.

## 용법

학습시키려는 `FUZZY_MAP_pre.py` 끝에 다음 포괄 규칙을 추가하세요.
```python
from pathlib import Path
import os
PROJECT_ROOT = Path(os.environ["SL5NET_AURA_PROJECT_ROOT"])

FUZZY_MAP_pre = [
    # 1. Your rule to optimize (result first!)
    ('Blumen orchestrieren',
     r'^(Blumen giesen|Blumen gessen|Blumen essen)$', 100,
     {'flags': re.IGNORECASE}
    ),

    #################################################
    # 2. Activate this rule (place it after the rule you want to optimize)
    (f'{str(__file__)}', r'^(.*)$', 10,
     {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################
]
```

`f'{str(__file__)}'` 라벨은 `collect_unmatched.py`에 정확히 무엇을 알려줍니다.
업데이트할 `FUZZY_MAP_pre.py` — 규칙은 모든 플러그인에서 이식 가능합니다.

## 플러그인 비활성화

충분한 훈련 데이터를 수집한 후 다음 중 하나를 수행하여 비활성화하십시오.

- 포괄 규칙에 대한 주석 처리
- 잘못된 이름으로 폴더 이름 바꾸기(예: 공백 추가)
- `maps` 디렉토리에서 플러그인 폴더 제거

## 파일 구조
```
1_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Example with catch-all rule
```

## 메모

플러그인은 런타임에 `FUZZY_MAP_pre.py`를 수정합니다. 업데이트된 내용을 커밋
수집된 훈련 데이터를 보존하기 위해 정기적으로 파일을 제출하세요.