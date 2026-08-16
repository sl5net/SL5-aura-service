# 로그 필터 프로필

활성 로그 필터는 항상 `config/filters/settings_local_log_filter.py`입니다.

## 프로필

사전 정의된 프로필은 `config/filters/.backlock/`에 저장됩니다.

| 프로필 | 설명 |
|---|---|
| `첫 번째_실행` | 최소 출력 — 오류 및 상태만. 처음 시작할 때 자동으로 적용됩니다. |
| '정상' | 매일 사용하는 표준 필터입니다. |

## 수동으로 프로필 전환

```bash
cp config/filters/.backlock/first_run/settings_local_log_filter.py config/filters/settings_local_log_filter.py
cp config/filters/.backlock/normal/settings_local_log_filter.py config/filters/settings_local_log_filter.py
```

## 사용자 정의 프로필 추가

1. `config/filters/.backlock/my_profile/` 아래에 새 폴더를 만듭니다.
2. 기존 `settings_local_log_filter.py`를 복사하고 필요에 맞게 편집하세요.
3. 위와 같이 `cp`로 적용합니다.

## 자동 프로필 전환

처음 시작할 때 Aura는 'log/' 디렉터리가 아직 존재하지 않음을 감지하고
`first_run` 프로필을 활성 필터로 자동 복사합니다.