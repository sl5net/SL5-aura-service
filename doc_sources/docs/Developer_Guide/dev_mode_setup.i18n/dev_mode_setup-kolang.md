# DEV_MODE 설정 가이드

## 문제

Weyland와 호환되므로 로깅에 `threading.Lock`을 사용합니다.

이제(21.3.'26 Sat) 로깅 규칙이 변경되었습니다. Manjaro에서는 문제가 없었습니다.

`DEV_MODE = 1`이 활성화되면 Aura는 초당 수백 개의 로그 항목을 생성합니다.
여러 스레드에서. 이로 인해 `SafeStreamToLogger`가 교착 상태에 빠질 수 있습니다.
첫 번째 받아쓰기가 트리거된 후 Aura가 중단됩니다.

## 해결 방법: LOG_ONLY 필터 사용

`DEV_MODE = 1`로 개발하는 경우 **반드시** 다음에서 로그 필터를 구성해야 합니다.
`config/filters/settings_local_log_filter.py`

### DEV_MODE에 대한 최소 작동 필터:
```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"Title",
    r"window",
    r":st:",
]
LOG_EXCLUDE = []
```

## settings_local.py에 대한 한 줄
DEV_MODE 설정 옆에 알림으로 이 설명을 추가하세요.
```python
DEV_MODE = 1  # ⚠️ Requires LOG_ONLY filter! See docs/dev_mode_setup.md
```

## 근본 원인
`SafeStreamToLogger`는 `threading.Lock`을 사용하여 stdout 쓰기를 보호합니다.
높은 로그 로드(DEV_MODE)에서 잠금 경합으로 인해 시스템에 교착 상태가 발생함
공격적인 스레드 스케줄링(예: 최신 커널/glibc를 사용하는 CachyOS)