> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../matrix_threema_relay-README.md).*

# 요소 ↔ 세마 베타 GUI 릴레이

**Element Desktop** (Matrix)와 같은 메시지를 미러링하는 작은 데몬
**삼 베타 ** (삼 바탕 화면 클라이언트) Linux / X11에서 모두 운전
사용자처럼 Windows : 키보드 단축키, 클립 보드 및 몇 개의 마우스 클릭.

API 없음, 토큰 없음, 추가 Python 라이브러리 없음. 표준 X11 명령 줄 도구 만.

## 무엇 그것

| 오시는 길 | 오시는길 |
|---|---|
| **Element → 세마 ** | 마지막 메시지 *you*는 엘리먼트에 썼고, 새로운 경우, Threema Beta에 붙여 넣었습니다. |
| **삼 → 요소** | 오픈 세마 채팅의 마지막 *incoming* 메시지는 컨텍스트 메뉴를 통해 복사되며, 엘리먼트로 새롭고 전송됩니다. |

일반적인 사용: dictate 또는 type into the Element room (Aura의 예)
Speech-to-text) 텍스트가 Threema 채팅에 도착하고,
세마 답글은 같은 요소 방에 나타납니다.

Windows 모두 열리고, 로그인하고, 릴레이를 원하는 채팅/방을 표시합니다.

## 루프 보호

네이티브 두 방향 미러는 모든 메시지를 다시 반송하고 영원히. 릴레이
짧은 역사 (`relay_history.py`)로 이것을 방지합니다.

1. 모든 텍스트 릴레이 전달은 기억됩니다 ** ** 그것은 전송됩니다, 180 초.
2. 텍스트가이 역사에 있는 다른 쪽에 보여줍니다 경우, 그것은 우리의 자신입니다
   echo: 보이지만 ** 다시 전달됩니다.
3. 새로운 *and* 알 수없는 텍스트는 정품 메시지이며 전달됩니다.

텍스트는 흰색 공간 붕괴와 비교, 그래서 라인 브레이크 차이에서
copy/paste는 감시를 패배하지 않습니다. 항목이 죽기 때문에, 보낼 수 있습니다
같은 텍스트 (예를 들어 "ok") 창이 통과 한 후 다시.

각 측면의 현재 마지막 메시지 시작은 **베이스 라인**으로 읽습니다.
*not* 앞으로. 시작 후 도착한 메시지 만 릴레이됩니다.

## 요구 사항

- ** X11** (`echo $XDG_SESSION_TYPE`는 `x11`를 인쇄해야 함)를 가진 리눅스. Wayland는 지원되지 않습니다.
- `xdotool`, `xclip`, `wmctrl` 및 `xset` (옵션, 화면을 비활성화하는 데 사용)
- 요소 데스크탑 (WM 클래스 `element.Element`)
- 세마 베타 (WM 클래스 `threema beta.Threema Beta`, 예를 들어 Flatpak)
  `ch.threema.threema-desktop`)
- Python 3 프로젝트의 virtualenv
- 한 번 교정 스크립트 `zsh`

## 설정: 한 번 교정

Threema Beta는 키보드로 작동할 수 없는 자체 컨텍스트 메뉴를 그릴 수 있습니다.
그래서 릴레이 클릭 "Copy Message" 와 마우스 위치에 관계
세마 창. 그들을 한 번 측정 :

```zsh
scripts/py/func/threema/threema-relay.zsh calibrate
```

스크립트는 세 개의 마우스 위치를 요청, 각 카운트 다운 (도 접촉하지 않음)
키보드, 이동하거나 창을 크기를 바꾸지 마십시오:

1. **Right-click** 마지막 *incoming* 메시지 (왼쪽에 거품) 및 휴가
   메뉴가 열립니다.
2. 마우스를 이동, 클릭하지 않고, **"Copy Message"**.
3. **message 입력 필드에 마우스를 이동합니다 **.

결과는 `~/.config/threema-relay.conf`에 저장됩니다:

| 키 | 의미 |
|---|---|
| `FX` | 창폭의 분수로 수평 클릭 위치 |
| `BOTTOM` | 위치, 창의 밑 가장자리의 픽셀|
| `DX`, `DY` | 클릭 시점에서 "쿠폰"으로 상쇄 |
| `INPUT_FX`, `INPUT_BOTTOM` | 메시지 입력 필드의 위치 |
| `DELAY_MENU`, `DELAY_COPY` | 초(기본 0.30 / 0.20)의 선택적 대기 |

마지막 채팅 메시지로 새로 들어오는 메시지로 보정 상태를 확인하세요:

```zsh
scripts/py/func/threema/threema-relay.zsh test
```

복사한 텍스트를 전달하지 않고 출력합니다. 보정은 창에 의존합니다.
기하학: Threema 창 크기를 많이 변경하면 다시 보정하세요.

## 사용법

저장소 루트에서:

```zsh
PYTHONPATH=. .venv/bin/python3 scripts/py/func/threema/matrix_threema_relay.py
```

옵션:

| 옵션 | 효과 |
|---|---|
| `--poll SECONDS` | 폴링 간격 (기본값 `2.0`) |
| `--no-threema-to-element` | 릴레이 전용 요소 → Threema |
| `--no-element-enter` | Threema 메시지를 Element 입력 필드에 붙여넣지만 **보내지는 마세요** (안전 테스트 모드) |

`Ctrl+C`를 멈추세요.

추천 첫 실행: `--no-element-enter`를 사용하고, Threema에서 자신에게 메시지를 보내세요
그리고 그것이 요소의 입력 필드에 나타나는지 확인하세요. 그런 다음 옵션 없이 실행하세요.

예시 로그:

```
[INFO] Initial Element baseline: 'Test'
[INFO] Initial Threema baseline: 'kaa'
[INFO] New Element message -> Threema: 'Hallo Welt'
[INFO] New Threema message -> Element: 'müsli'
[INFO] Element shows our own relayed text - not sending back.
```

## 어떻게 작동합니까?

```
every poll interval
├─ Element:  focus window (wmctrl) → Up, Ctrl+A, Ctrl+C, Escape (xdotool) → read clipboard (xclip)
│            new + unknown  → paste into Threema + Return, remember text
│            new + known    → echo, ignore
└─ Threema:  focus window → right-click last incoming bubble → click "Copy Message"
                          → click input field (restores focus) → read clipboard
             new + unknown  → paste into Element (+ Return), remember text
             new + known    → echo, ignore
```

- * Element's composer에서 *Ctrl+A/Ctrl+C* 복사
  그것과 *Escape*는 편집 형태를 떠납니다. 이것은 왜 단지 ** 자신 ** 마지막 요소
  메시지는 Threema에 릴레이됩니다.
- Threema a**sentinel string** 는 클립보드에 먼저 삽입됩니다. 아직
  그 후, 아무것도 복사되지 않았다 (예를 들어 자신의 메시지가
  마지막과 클릭은 거품이 없습니다) 그리고 시도는 무시됩니다.

## 파일

| 파일 | 목적 |
|---|---|
| `matrix_threema_relay.py` | 메인 루프, CLI, 결정 논리(`classify_candidate`) |
| `read_last_element_message.py` | 읽는 요소의 마지막 메시지 |
| `send_to_threema_window.py` | 세마 베타로 텍스트를 붙여 넣기 |
| `read_last_threema_message.py` | 세마의 마지막 수신 메시지, 부하 보정 |
| `send_to_element_window.py` | 붙여넣기 텍스트 |
| `relay_history.py` | 루프 보호 |
| `threema-relay.zsh` | 교정 및 매뉴얼 테스트 도구(`calibrate`, `test`) |
| `test_threema_relay.py` | 단위 테스트(X11 필요) |

다음과 함께 테스트를 실행하세요:

```zsh
PYTHONPATH=. .venv/bin/python3 -m unittest scripts.py.func.threema.test_threema_relay
```

## 제한

- ** 릴레이는 마우스와 키보드 초점을 사용합니다. 호텔지도 각 설문 조사에서 삼마와
  Element Windows는 집중하고 마우스는 간단히 점프합니다 (그것은 복원됩니다). 하지 마십시오
  설문조사가 실행되거나 더 긴 `--poll`를 사용합니다.
- 각 설문 조사에 클립보드를 덮습니다.
- **3MA에서 마지막 메시지 : ** 자신의 메시지가 Threema에서 마지막 때
  채팅, 그 전에 도착한 대답은 본 적이 없습니다.
- ** 마지막 메시지**는 설문 조사에 읽습니다. 여러 메시지가 하나 안에 도착하면
  간격은, 가장 새로운 릴레이됩니다.
- ** 텍스트 만. ** 이미지, 파일, 반응 및 편집은 릴레이되지 않습니다.
- ** 한 채팅 쌍. ** 각 창에서 어떤 채팅 / 룸이 열려 있습니다.
- ** Element의 입력 필드의 초안 ** 다음 붙여 넣을 수 있습니다
  이름 *
- ** X11 만. ** Wayland 블록 합성 입력 및 창 초점 변경.
- 릴레이는 시작 (`xset s off -dpms`);에 X11 screensaver와 DPMS를 비활성화합니다.
  당신은 그들을 재 활성화하거나 다시 로그인 할 때까지 유지.

## 문제 해결

| 증상 | 자주 묻는 질문 |
|---|---|
| `Threema window ... not found` | `xdotool search --class "Threema Beta"` 및 `xprop WM_CLASS`를 확인해주세요. |
| `Nothing copied` / no Threema → Element | Re-run `calibrate`; 마지막 메시지로 `test`를 실행합니다. `DELAY_MENU`/`DELAY_COPY`가 느린 기계에 구성합니다. |
| 문자는 세마에 도착하지만 전송되지 않습니다 | 입력 필드는 집중되지 않습니다. 보정에서 `INPUT_FX`/`INPUT_BOTTOM`를 확인하십시오. |
| 세마 텍스트가 엘리먼트에 나타날 수 없습니다 | 릴레이는 `--no-element-enter`로 시작되었습니다. |
| 구성의 `0,9353`와 같은 소수 번호 | 독일어 로컬에서 오래된 스크립트 버전에 의해 작성되었습니다. 파이썬 코드는 그(것)들을 받아들입니다; 현재 스크립트로 다시 캘리브레이션은 점을 씁니다. ·
