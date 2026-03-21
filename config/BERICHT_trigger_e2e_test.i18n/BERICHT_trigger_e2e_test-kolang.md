# Abschlussbericht: SL5 Aura – 엔드투엔드 테스트 트리거

**데이텀:** 2026-03-15XSPACEbreakX
**날짜:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. 계획

Ein echter End-to-End Test der das bekannte 문제 해결 방법:
**Bei manchen Aufnahmen fehlt das letzte Wort im Output.**

테스트 항목:
1. Eine WAV-Datei als德lles Mikrofon einspeisen
2. Aura per `touch /tmp/sl5_record.trigger` starten — genau wie im echten Betrieb
3. 미트 zweitem 트리거 스톱펜
4. YouTube 대본을 통해 출력
5. Feststellen ob ein Wort am Ende fehlt

---

## 2. erreicht wurde ✅

- Aura reagiert auf den Trigger korrekt
- LT läuft und ist erreichbar (`http://127.0.0.1:8082`)
- `_wait_for_output()` findet die `tts_output_*.txt` Datei
- `_fetch_yt_transcript_segment()` holt den Referenz-Text korrekt
- Der grundlegende Testaufbau ist solide und funktioniert konzeptionell

---

## 3. Das ungelöste 문제 🔴

### Kern 문제: `manage_audio_routing` 모든 항목에 대해

Beim Session-Start ruft Aura intern auf:
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

Diese Funktion은 먼저 다음과 같이 설명합니다.
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

**Sie löscht jeden Sink den wir vorher erstellt haben.**

Danach erstellt sie keinen neuen Sink weil `mode == 'SYSTEM_DEFAULT'` (nicht `MIC_AND_DESKTOP`).

### Versuchte Lösungen

| 베르수치 | 문제 |
|---|---|
| PulseAudio 가상 소스 제공 | PipeWire는 '모듈-가상 소스'를 무시합니다 |
| `settings_local.py` auf `MIC_AND_DESKTOP` setzen | Datei wurde mit mehrfachen Einträgen korrumpiert |
| Markierten Override-Block 및 Ende schreiben | Aura lädt 설정 nicht schnell genug neu bevor Trigger kommt |
| `_create_mic_and_desktop_sink()` 직접 테스트 | `manage_audio_routing`을 통해 Session-Start gelöscht |
| `pw-루프백` | Erscheint als Source aber Aura hört nicht darauf |

### Warum `settings_local.py` nicht funktioniert 재정의

`dynamic_settings.py` überwacht die Datei und lädt sie nach — aber mit einem Intervall. Der Trigger kommt zu schnell nach dem Schreiben. Aura는 'SYSTEM_DEFAULT' 세션 시작 시 시작됩니다.

Außerdem: selbst wenn Aura `MIC_AND_DESKTOP` lädt, erstellt es den Sink erst beim **nächsten** Session-Start — nicht sofort.

---

## 4. Mögliche Lösungswege

### 옵션 A — Längeres Warten nach 설정-änderung
```python
_set_audio_input_device("MIC_AND_DESKTOP")
time.sleep(5.0)   # statt 1.5s — mehr Zeit für dynamic_settings reload
TRIGGER_FILE.touch()
```
Risiko: Nicht zuverlässig, timing-abhängig.

### 옵션 B — Aura neu starten nach 설정-änderung
```python
_set_audio_input_device("MIC_AND_DESKTOP")
subprocess.run(["./scripts/restart_venv_and_run-server.sh"])
time.sleep(60)   # warten bis LT bereit
TRIGGER_FILE.touch()
```
밤: 1분 동안 테스트를 진행하세요. Aber zuverlässig.

### 옵션 C - `manage_audio_routing` 직접 테스트 aufrufen
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing
manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
```
Sink가 Trigger kommt — 및 `manage_audio_routing`에 존재하여 Session-Start erkennt `is_mic_and_desktop_sink_active() == True` 및 überspringt das Setup에 존재합니다.

Das ist wahrscheinlich die **sauberste Lösung**.

### 옵션 D — `process_text_in_Background` direkt aufrufen(kein Trigger)
`test_youtube_audio_regression.py`의 Wie — 파이프라인 übergeben, ohne den echten Trigger-Mechanismus의 Vosk-Output 방향입니다. Dann testet man die Pipeline aber nicht das Abschneiden des letzten Wortes.

### 옵션 E — Aura mit `run_mode_override=TEST` 시작
Falls Aura einen Test-Modus hat der das Audio-Routing überspringt.

---

## 5. 엠펠룽

**옵션 C** zuerst probieren — einen 가져오기 테스트 기계:

```bash
python3 -c "from scripts.py.func.manage_audio_routing import manage_audio_routing; print('OK')"
```

Wenn das 기능:
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

Aura는 Session-Start `is_mic_and_desktop_sink_active() == True`를 실행하고 Ruhe에서 가장 적은 싱크를 시작했습니다.

---

## 6. 테스트 결과가 langfristig로 바뀌었나요?

Sobald er lauft, kann man:
- `SPEECH_PAUSE_TIMEOUT` Werte testen (1.0, 2.0, 4.0s) and sehen ob das letzte Wort abgeschnitten wird
- `transcribe_audio_with_feedback.py` 매개변수 최적화
- Regressionen erkennen wenn sich das Audio-Handling ändert
- Beweisen dass ein Fix wirklich hilft

---

---

# 최종 보고서: SL5 Aura – 트리거 엔드투엔드 테스트

**날짜:** 2026-03-15XSPACEbreakX
**파일:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. 계획

알려진 문제를 조사하기 위한 실제 엔드투엔드 테스트:
**일부 녹음에서는 출력의 마지막 단어가 잘립니다.**

테스트는 다음을 수행해야 합니다.
1. WAV 파일을 가상 마이크로 피드
2. `touch /tmp/sl5_record.trigger`를 통해 Aura를 시작합니다. 실제 사용법과 똑같습니다.
3. 두 번째 트리거로 중지
4. 출력물을 YouTube 스크립트와 비교
5. 끝에 단어가 누락되었는지 감지

---

## 2. 달성한 성과 ✅

- Aura가 트리거에 올바르게 반응합니다.
- LT가 실행 중이고 연결 가능합니다(`http://127.0.0.1:8082`).
- `_wait_for_output()`은 `tts_output_*.txt` 파일을 찾습니다.
- `_fetch_yt_transcript_segment()`는 참조 텍스트를 올바르게 가져옵니다.
- 기본 테스트 구조가 견고하고 개념적으로 작동합니다.

---

## 3. 해결되지 않은 문제 🔴

### 핵심 문제: `manage_audio_routing`이 모든 것을 덮어씁니다.

세션 시작 시 Aura는 내부적으로 다음을 호출합니다.
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

이 함수는 먼저 다음을 수행합니다.
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

**이전에 생성한 싱크가 모두 삭제됩니다.**

그런 다음 `mode == 'SYSTEM_DEFAULT'`(`MIC_AND_DESKTOP` 아님) 때문에 새 싱크를 생성하지 않습니다.

### 시도한 솔루션

| 시도 | 문제 |
|---|---|
| PulseAudio 가상 소스 생성 | PipeWire가 `module-virtual-source`를 무시합니다 |
| `settings_local.py`를 `MIC_AND_DESKTOP`으로 설정 | 파일이 여러 항목으로 인해 손상되었습니다 |
| 표시된 대체 블록을 파일 끝에 쓰기 | Aura가 트리거가 실행되기 전에 충분히 빠르게 설정을 다시 로드하지 않음 |
| 테스트에서 직접 `_create_mic_and_desktop_sink()` | 세션 시작 시 `manage_audio_routing`에 의해 삭제됨 |
| `pw-루프백` | 소스로 나타나지만 Aura는 이를 듣지 않습니다 |

---

## 4. 권장되는 다음 단계

트리거 전 테스트에서 직접 `manage_audio_routing`을 호출하세요.

```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

Aura는 세션을 시작할 때 'is_mic_and_desktop_sink_active()'를 확인합니다. 'True'인 경우 설정을 건너뛰고 싱크만 그대로 둡니다. 이것이 가장 깨끗한 솔루션입니다.

---

## 5. 이 테스트를 통해 장기적으로 실현할 수 있는 것

일단 실행하면:
- `SPEECH_PAUSE_TIMEOUT` 값(1.0, 2.0, 4.0s)을 테스트하고 단어 끊김을 감지합니다.
- `transcribe_audio_with_feedback.py` 매개변수 최적화
- 오디오 처리 변경 시 회귀를 포착합니다.
- 수정사항이 실제로 작동하는지 증명