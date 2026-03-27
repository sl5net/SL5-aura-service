# 일치하지 않는 교육 플러그인(`a_collect_unmatched_training`)

## 목적

이 플러그인은 인식되지 않은 음성 입력을 자동으로 수집하여 추가합니다.
퍼지 맵 정규식의 새로운 변형입니다. 이를 통해 시스템은 "자체 훈련"을 할 수 있습니다.
시간이 지남에 따라 비교할 수 없는 인식 결과를 통해 학습합니다.

## 작동 방식

1. `FUZZY_MAP_pre.py`의 `COLLECT_UNMATCHED` 포괄 규칙은 다음과 같은 경우에 실행됩니다.
음성 입력과 일치하는 다른 규칙은 없습니다.
2. `collect_unmatched.py`는 일치하는 텍스트와 함께 `on_match_exec`를 통해 호출됩니다.
3. 'unmatched_list.txt'(파이프 구분)에 텍스트가 추가됩니다.
4. `FUZZY_MAP_pre.py`의 정규식은 새로운 변형으로 자동 확장됩니다.

## 플러그인 비활성화

충분한 훈련 데이터를 수집한 후 다음 중 하나를 수행하여 이 플러그인을 비활성화하십시오.

- Aura 설정에서 비활성화
- `maps` 디렉토리에서 플러그인 폴더 제거
- 잘못된 이름으로 폴더 이름 바꾸기(예: 공백 추가: `a_collect unmatched_training`)

## 파일 구조
```
a_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Catch-all rule + growing regex variants
```

## 메모

플러그인은 런타임에 `FUZZY_MAP_pre.py`를 수정합니다. 꼭 커밋하세요
수집된 훈련 데이터를 보존하기 위해 파일을 정기적으로 업데이트합니다.