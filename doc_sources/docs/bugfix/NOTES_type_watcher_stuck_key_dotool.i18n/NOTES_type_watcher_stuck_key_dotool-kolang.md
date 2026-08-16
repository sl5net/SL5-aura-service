# 참고: type_watcher.sh 키 고정 문제(dotool)

## 증상
Manjaro 재부팅 직후 'sl5net Aura' 이후 첫 번째 받아쓰기에서
자동 시작, 단일 문자가 멈춰 무한 반복됨
(예: "n"이 수백 번 반복됨) 트리거 키를 누를 때까지
다시 수동 해결 방법으로.

2026-07-21 ~09:44(화) 1회 관찰, 텍스트: "Die Ideen niemand wird
mehr gefragt, aber es soll trotzdem genauso sein wie...nnnnn...".

## 타임라인(로그를 통해 입증됨)
- 09:29:17 - `type_watcher.sh` 시작됨(log/type_watcher.log)
- 09:41:56 - "ideen niemand wird mehr gefragt..." 받아쓰기 수신
(로그/aura_engine.log, 스레드-13/14)
- 09:42:03 - 텍스트 처리 완료(`최고의 퍼지 점수:0%`),
아마도 `tts_output_*.txt` 파일에 기록되었을 것입니다.
- ~09:42:04-09:42:09 - `type_watcher.sh` 충돌(추론: watchdog)
폴링 간격은 5초입니다. 아래 참조)
- 09:42:09 - 감시 로그(log/type_watcher_keep_alive.log):
"WATCHDOG: 'type_watcher.sh'가 실행되고 있지 않습니다. 지금 시작합니다."
- 09:42:13 - `type_watcher.sh` 다시 시작됨(log/type_watcher.log)
- "ideen niemand..." 파일에 대한 'typed content of ...' 항목이 없습니다.
log/type_watcher.log에서 발견된 적 있음 — 해당 특정 항목의 입력
텍스트가 완료/기록되지 않았습니다.

## 근본 원인 상태
- 확인됨: 'type_watcher.sh'가 텍스트 마무리 사이에 충돌했습니다.
처리(09:42:03) 및 워치독이 실행되지 않는 것으로 감지
(09:42:09). 워치독(`type_watcher_keep_alive.sh`)은 오직 킬만 합니다.
구성 파일 타임스탬프 변경(`ts1`/`ts2`,
이 사건에서 변경되지 않은 것으로 확인됨) 또는 다음과 같은 경우 자동으로 다시 시작됩니다.
`pgrep -f "type_watcher.sh"`는 프로세스를 찾지 못했습니다. 즉, 이는 매우
외부 살해가 아닌 자체 충돌 가능성이 높습니다.
- 가설(증명되지 않음): `set -euo Pipefail`(type_watcher.sh 라인 5)
내부의 0이 아닌 일부 종료 코드에서 스크립트가 종료되도록 했습니다.
파이프라인, 아마도 `do_type()`의 `dotool` 파이프(라인 125)가
내의 한복판. `dotool`로 스트리밍하는 동안 bash 프로세스가 종료되면,
별도의 `dotoold` 데몬(독립적으로 계속 실행됨)
일치하는 "위" 상태가 없는 "아래" 상태의 키를 그대로 둘 수 있습니다.
수신되어 OS 수준 키 반복이 발생합니다.
- 아직 입증되지 않음: 0이 아닌 오류를 발생시킨 정확한 명령/줄
'set -euo Pipefail'로 종료하세요. 충돌로 인한 stderr 없음
`type_watcher.sh` 프로세스가 캡처되었습니다(워치독이 이를 호출함).
출력 리디렉션 없이 `type_watcher_keep_alive.sh` 라인 79).
- 영향을 받은 키가 항상 다른 키에 걸쳐 동일한 문자는 아니었습니다.
이 버그 발생(사용자 신고: 이전에는 "t"도 포함)

## 이미 조사되어 배제되었습니다.
- 구성 변경으로 인한 재시작이 아님(사용자가 확인함: config)
변경되지 않았으며 `ts1_old != ts1_new` 검사는 "구성 변경됨"을 기록합니다).
- `type_watcher.sh`의 자동 시작이 중복되지 않음
(충돌이 발생하기 전에 단 하나의 "Hello from Watcher" 항목만 발생함)
- `do_type()`의 `dotool type` 호출은 호출마다 원자적이며
자체적으로 문자별 키를 아래/위로 보내지 않음 — `type_watcher.sh` 제외
정상 상태에서 고정된 키의 직접적인 소스인 애플리케이션 로직
(충돌하지 않는) 작업.

## 수정 사항이 이미 적용되었습니다(근본 원인 수정이 아닌 대체/완화).
`type_watcher.sh`의 `cleanup()`과 `do_cleanup()` 모두
`keep-keys-up.sh`는 이전에 수정자 키(shift, ctrl,
alt 등) `dotool`/`xdotool`을 통해. 이것은 붙어있는 정규병에게는 아무 것도 하지 못했습니다.
키(문자, 숫자, 구두점).

- `type_watcher.sh`: `cleanup()`은 이제 `dotool key <name>:up`을 전송합니다.
모든 문자, 숫자 및 일반적인 구두점/공백 키는 제외됩니다.
그냥 수정자.
- `type_watcher.sh`: `INPUT_METHOD`는 이제 감지 후 내보내집니다.
다른 스크립트는 어떤 백엔드(`dotool` / `xdotool`)가 활성화되어 있는지 확인할 수 있습니다.
- `keep-keys-up.sh`: `do_cleanup()`이 `dotool` 브랜치를 얻었습니다(
'keyup' 동사, 키별 지연 없음, 성능을 위해) 다음 경우에만 활성화됩니다.
`INPUT_METHOD=dotool`, 기존 `xdotool keyup` 호출 미러링
수정자용.

이는 `type_watcher.sh`의 기본 충돌을 수정하지 않습니다. 그것뿐
충돌이 다시 발생하면 고정된 키가 해제됩니다.
다음 정리 단계(`--cleanup`, `do_type()`마다 호출됨, 그리고
반복하는 대신 `트랩 정리 EXIT INT TERM` 핸들러를 통해)
수동으로 트리거 키를 누를 때까지 무기한.

## 이런 일이 다시 발생하면 다음 단계
- 충돌 시 `type_watcher.sh`의 표준 오류를 캡처합니다. 현재
`type_watcher_keep_alive.sh` 79행에서는 리디렉션 없이 이를 호출하므로
모든 bash 오류 메시지는 손실됩니다(워치독의 메시지로 이동).
stdout/stderr(자동 시작 메커니즘에 의해 지시되는 모든 곳).
- 디버그 모드를 고려하세요. `bash -x 스크립트/type_watcher/type_watcher.sh
2>> log/type_watcher_debug.log`, 다음과 같은 env var를 통해 전환됨
`TYPE_WATCHER_DEBUG=1`, 다음 행에서 정확한 실패 행을 캡처합니다.
충돌.
- Manjaro 부팅 시 `type_watcher_keep_alive.sh`가 시작되는 항목을 확인하세요.
(자동 시작 `.desktop` 파일, systemd `--user` 유닛 등) 및 여부
해당 stdout/stderr은 어디에서나 캡처됩니다.
- 재현 가능한 경우 충돌이 다음과 상관관계가 있는지 테스트합니다.
`dotoold`는 부팅 직후 여전히 초기화 중입니다(`sleep 0.1` 참조).
type_watcher.sh 라인 8 및 `dotoold` 시작 루프 라인
102-110).