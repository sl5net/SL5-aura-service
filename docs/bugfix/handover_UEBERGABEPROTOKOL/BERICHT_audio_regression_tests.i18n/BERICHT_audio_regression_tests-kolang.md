# SL5 Aura – 오디오 회귀 테스트: Statusbericht

**데이텀:** 2026-03-14XSPACEbreakX
**날짜:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. Wurde gebaut 였나요?

테스트 시스템의 내용:
1. Ein Audio-Segment aus einem YouTube-Video herunterlädt(`yt-dlp` + `ffmpeg`를 통해)
2. 갑자기 생성된 YouTube-Transcript for dasselbe Segment(`youtube-transcript-api`를 통해)
3. Vosk 번역을 위한 Das Audio
4. 옵션 das Ergebnis durch die **volle Aura-Pipeline** schickt (`process_text_in_Background`)
5. WER(다이 워드 오류율) zwischen Aura-Output 및 YouTube-Transcript berechnet
6. Automatischer Regressionstest läuft와 같은 'pytest'에 따라

모두 다운로드 werden gecacht (`scripts/py/func/checks/fixtures/youtube_clips/`), Sodass Folgetests schnell laufen.

---

## 2. 다테엔

| 다테이 | 즈베크 |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Haupttestdatei |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Gecachte 오디오 클립 |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Gecachte 성적표 |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Git으로 캐시 사용 |
| `conftest.py`(Repo-Root) | pytest에 대한 PYTHONPATH 설정 |

---

## 3. 테스트-모디

### Modus A – Vosk 전용(기준)
```python
YoutubeAudioTestCase(
    test_id       = "mein_test_vosk",
    video_id      = "XXXXXXXXXXX",
    start_sec     = 10,
    end_sec       = 25,
    language      = "de-DE",
    wer_threshold = 0.40,
)
```
Testet nur Vosk-Qualität. 케인 아우라. 슈넬.

### Modus B – Volle Aura-Pipeline, WER-Vergleich
```python
YoutubeAudioTestCase(
    test_id            = "mein_test_aura",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 10,
    end_sec            = 25,
    language           = "de-DE",
    wer_threshold      = 0.35,   # strenger — Aura soll besser sein als Vosk
    test_aura_pipeline = True,
)
```
Schickt Vosk-Output durch FuzzyMap Pre → LanguageTool → FuzzyMap Post.

### Modus C – Volle Aura-Pipeline, 출력 강화
```python
YoutubeAudioTestCase(
    test_id            = "befehl_terminal_oeffnen",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 42,
    end_sec            = 45,
    language           = "de-DE",
    test_aura_pipeline = True,
    expected_output    = "terminal öffnen",  # Aura muss genau das ausgeben
)
```
Für Segmente wo ein bekannter Befehl gesprochen wird. Schärfster 테스트.

---

## 4. Was wird getestet — was nicht

| 였다 | Getestet? |
|---|---|
| Vosk STT 품질 | ✅ |
| FuzzyMap 사전 등록 | ✅ (wenn Aura lauft) |
| LanguageTool-Korrekturen | ✅ (wenn LT läuft) |
| FuzzyMap 포스트 레겔른 | ✅ (wenn Aura lauft) |
| 키보드 출력(AutoHotkey/CopyQ) | ❌ bewusst — OS-Ebene, keine Logik |
| Vosk 모델 로딩 | ❌ — Aura liest Output-Datei, lädt kein Modell neu |

Der Output wird aus `tts_output_*.txt` im Temp-Verzeichnis gelesen — genau so wie Aura es intern macht, nicht aus dem Terminal.

---

## 5. 시작하기

### Normaler Testlauf(Aura Muss bereits laufen):
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

### Mit vollem 로그:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

### 가장 좋은 테스트:
```bash
# Nur Aura-Tests
.venv/bin/pytest ... -k "aura"

# Nur Vosk-Baseline
.venv/bin/pytest ... -k "not aura"

# Einen spezifischen Test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

### Aura + LT 시작 시작:
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # prüfen ob LT läuft
```

---

## 6. 위치 구성

### Sprachcodes — zwei verschiedene Systeme!

| 시스템 | 코드 | 바이스피엘 |
|---|---|---|
| 보스크-모델-오르드너 | '데' | `모델/vosk-model-de-0.21` |
| Aura FuzzyMap-Ordner | `드-DE` | `config/maps/.../de-DE/` |
| YouTube 대본 API | '데' | `api.fetch(..., 언어=["de"])` |

**Lösung 메신저 코드:** `언어="de-DE"` setzen. Der Code macht automatisch:
- Für Vosk: `"de-DE"` → `"de"`(auf `-` 분할)
- YouTube용: ``de-DE"` → ``de"` (split auf `-`)
- Für Aura: ``de-DE"` 직접

### 자동 번역기 사용 가능 테스트:
```bash
# Backup wiederherstellen (deaktiviert Auto-Translator):
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
Sonst übersetzt Aura deutschen Text ins Englische — das verfälscht den WER.

---

## 7. Bekannte 문제 및 Lösungen

| 문제 | 우르사케 | 뢰성 |
|---|---|---|
| '건너뛰기' 소프트 | YouTube 대본 nicht gefunden | `api.list('video_id')` aufrufen um verfügbare Sprachen zu sehen |
| `SKIPPED` nach 오디오 | Vosk-Modell nicht gefunden | `언어.split("-")[0]` 대체 메신저 코드 |
| `FUZZY_MAP_pre 규칙 0개 발견` | Falscher Sprachcode 및 Aura | ``de-DE"` statt ``de"` 버전 |
| '연결이 거부되었습니다 8010' | LT nicht gestartet | Aura zuerst starten, 60s warten |
| `zsh: 종료됨` | X11-Watchdog 킬트 Prozess | `SDL_VIDEODRIVER=dummy` 확인; Watchdog-Schwellenwert erhöhen |
| YouTube `>>` 마커 | Zweitsprecher im 성적 증명서 | `re.sub(r'>>', '', text)` — nur `>>` entfernen, Wörter behalten |
| `속성 오류: get_transcript` | youtube-transcript-api v1.x | `api = YouTubeTranscriptApi(); api.fetch(...)` statt Klassenmethod |
| 캐시 사용 가능 텍스트 | Alter Lauf mit kaputtem Regex | `rm 설비/youtube_clips/*.transcript.json` |

---

## 8. 에르게브니스 비스 제트츠

### 동영상: `sOjRNICiZ7Q`(Deutsch), 세그먼트 5~20초

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

**베오바흐퉁겐:**
- Aura hat eine Regel angewende: `zehn 손가락` → `10 손가락` ✅
- LT-Status während dieses Laufs unklar — Verbindung wurde verweigert
- Hoher WER liegt am 세그먼트: YouTube-Transcript Beginnt mit Wörtern die Vosk nicht hört(Sprecher noch nicht am Mikro)
- **Empfehlung:** 세그먼트 verschieben auf einen Bereich wo klar gesprochen wird

---

## 9. Empfehlungen für nächste Schritte

1. **Besseres Segment wählen** — `ffplay` nutzen um die genaue Sekunde zu finden wo klar gesprochen wird
2. **LT-Status im Test prüfen** — `curl http://localhost:8010/v2/언어s` vor dem Test
3. **Modus C 테스트 hinzufügen** — Segmente wo bekannte Befehle gesprochen werden (`expected_output`)

---
---

# SL5 Aura – 오디오 회귀 테스트: 상태 보고서

**날짜:** 2026-03-14XSPACEbreakX
**파일:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. 무엇이 만들어졌는가

테스트 시스템은 다음과 같습니다.
1. YouTube 동영상에서 오디오 세그먼트를 다운로드합니다(`yt-dlp` + `ffmpeg`를 통해).
2. 동일한 세그먼트에 대해 자동 생성된 YouTube 스크립트를 가져옵니다(`youtube-transcript-api`를 통해).
3. Vosk를 통해 오디오를 텍스트로 변환합니다.
4. 선택적으로 **전체 Aura 파이프라인**(`process_text_in_Background`)을 통해 결과를 전달합니다.
5. Aura 출력과 YouTube 스크립트 사이의 WER(단어 오류율)을 계산합니다.
6. `pytest`를 통해 자동 회귀 테스트로 실행됩니다.

모든 다운로드는 캐시(`scripts/py/func/checks/fixtures/youtube_clips/`)되므로 후속 실행이 빠릅니다.

---

## 2. 파일

| 파일 | 목적 |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | 메인 테스트 파일 |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | 캐시된 오디오 클립 |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | 캐시된 성적표 |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Git에서 캐시 제외 |
| `conftest.py`(repo 루트) | pytest에 대한 PYTHONPATH를 설정합니다 |

---

## 3. 테스트 모드

### 모드 A – Vosk 전용(기준)
```python
YoutubeAudioTestCase(
    test_id       = "my_test_vosk",
    video_id      = "XXXXXXXXXXX",
    start_sec     = 10,
    end_sec       = 25,
    language      = "de-DE",
    wer_threshold = 0.40,
)
```
Vosk 품질만 테스트합니다. 아우라가 없습니다. 빠른.

### 모드 B – 전체 Aura 파이프라인, WER 비교
```python
YoutubeAudioTestCase(
    test_id            = "my_test_aura",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 10,
    end_sec            = 25,
    language           = "de-DE",
    wer_threshold      = 0.35,   # stricter — Aura should improve on Vosk
    test_aura_pipeline = True,
)
```
FuzzyMap Pre → LanguageTool → FuzzyMap Post를 통해 Vosk 출력을 보냅니다.

### 모드 C – 전체 Aura 파이프라인, 정확한 출력 일치
```python
YoutubeAudioTestCase(
    test_id            = "command_open_terminal",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 42,
    end_sec            = 45,
    language           = "de-DE",
    test_aura_pipeline = True,
    expected_output    = "terminal öffnen",   # Aura must produce exactly this
)
```
알려진 음성 명령이 포함된 세그먼트의 경우. 가장 엄격한 테스트 모드.

---

## 4. 테스트되는 것 — 테스트되지 않는 것

| 무엇 | 테스트를 거쳤나요? |
|---|---|
| 보스크 STT 품질 | ✅ |
| FuzzyMap 사전 규칙 | ✅ (Aura 실행 시) |
| LanguageTool 수정 | ✅ (LT 실행 시) |
| FuzzyMap 게시 규칙 | ✅ (Aura 실행 시) |
| 키보드 출력(AutoHotkey/CopyQ) | ❌ 의도적 — OS 수준, 논리 없음 |
| Vosk 모델 다시 로드 | ❌ — Aura는 출력 파일을 읽고 모델을 다시 로드하지 않습니다 |

출력은 임시 디렉터리의 `tts_output_*.txt`에서 읽혀집니다. 이는 Aura가 터미널이 아닌 내부적으로 수행하는 것과 똑같습니다.

---

## 5. 시작 명령

### 일반 테스트 실행(Aura가 이미 실행 중이어야 함):
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

### 전체 로그 사용:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

### 특정 테스트에만 해당:
```bash
# Only Aura tests
.venv/bin/pytest ... -k "aura"

# Only Vosk baseline
.venv/bin/pytest ... -k "not aura"

# One specific test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

### Aura + LT를 먼저 시작하세요.
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # verify LT is up
```

---

## 6. 중요 구성

### 언어 코드 — 두 가지 다른 시스템!

| 시스템 | 코드 | 예 |
|---|---|---|
| Vosk 모델 폴더 | '데' | `모델/vosk-model-de-0.21` |
| Aura FuzzyMap 폴더 | `드-DE` | `config/maps/.../de-DE/` |
| YouTube 대본 API | '데' | `api.fetch(..., 언어=["de"])` |

**코드의 해결 방법:** `언어="de-DE"`를 설정하세요. 코드는 다음을 자동으로 처리합니다.
- Vosk의 경우: `"de-DE"` → `"de"`(`-`로 분할)
- YouTube의 경우: `"de-DE"` → `"de"`(`-`로 분할)
- Aura의 경우: `"de-DE"` 직접

### 테스트 전에 자동 번역기를 비활성화합니다.
```bash
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
그렇지 않으면 Aura는 독일어 텍스트를 영어로 번역하므로 WER 측정이 손상됩니다.

---

## 7. 알려진 문제 및 해결 방법

| 문제 | 원인 | 수정 |
|---|---|---|
| 즉시 '건너뛰기' | YouTube 스크립트를 찾을 수 없습니다 | 사용 가능한 언어를 보려면 `api.list('video_id')`를 호출하세요 |
| 오디오 후 '건너뛰기' | Vosk 모델을 찾을 수 없습니다 | `언어.split("-")[0]` 코드 대체 |
| `FUZZY_MAP_pre 규칙 0개 발견` | Aura에 잘못된 언어 코드가 전달되었습니다 | `"de"`가 아닌 `"de-DE"`를 사용하세요 |
| '연결이 거부되었습니다 8010' | LT가 시작되지 않음 | Aura를 먼저 시작하고 60초 동안 기다립니다 |
| `zsh: 종료됨` | X11 워치독이 프로세스를 종료합니다 | `SDL_VIDEODRIVER=dummy`를 사용하세요. 감시 임계값 높이기 |
| YouTube `>>` 마커 | 성적표의 두 번째 발표자 | `re.sub(r'>>', '', text)` — `>>`만 제거하고 단어는 유지 |
| `속성 오류: get_transcript` | youtube-transcript-api v1.x | `api = YouTubeTranscriptApi();를 사용하세요. api.fetch(...)` |
| 캐시에 빈 텍스트가 포함되어 있습니다 | 깨진 정규식을 사용하여 이전 실행 | `rm 설비/youtube_clips/*.transcript.json` |

---

## 8. 지금까지의 결과

### 동영상: `sOjRNICiZ7Q`(독일어), 세그먼트 5~20초

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

**관찰:**
- 아우라는 규칙을 적용했습니다: `zehn Finger` → `10 Finger` ✅
- 이 실행 중 LT 상태가 불분명함 - 연결이 거부되었습니다.
- 높은 WER은 세그먼트 선택으로 인한 것입니다. YouTube 스크립트는 Vosk가 들을 수 없는 단어로 시작됩니다(화자는 아직 마이크에 있지 않음).
- **권장사항:** 세그먼트를 명확한 음성이 나오는 섹션으로 이동하세요.

---

## 9. 권장되는 다음 단계

1. **더 나은 세그먼트 선택** - `ffplay`를 사용하여 음성이 명확한 정확한 순간을 찾습니다.
2. **테스트 전 LT 상태 확인** — 실행 전 `curl http://localhost:8010/v2/언어s`
3. **모드 C 테스트 추가** — 알려진 음성 명령이 포함된 세그먼트(`expected_output`)