# SL5 Aura – Audio-Regressionstests: Statusbericht

**Datum:** 2026-03-14  
**Datei:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. Was wurde gebaut

Ein Testsystem das:
1. Ein Audio-Segment aus einem YouTube-Video herunterlädt (via `yt-dlp` + `ffmpeg`)
2. Den automatisch generierten YouTube-Transcript für dasselbe Segment abruft (via `youtube-transcript-api`)
3. Das Audio durch Vosk transkribiert
4. Optional das Ergebnis durch die **volle Aura-Pipeline** schickt (`process_text_in_background`)
5. Die Word Error Rate (WER) zwischen Aura-Output und YouTube-Transcript berechnet
6. Per `pytest` als automatischer Regressionstest läuft

Alle Downloads werden gecacht (`scripts/py/func/checks/fixtures/youtube_clips/`), sodass Folgetests schnell laufen.

---

## 2. Dateien

| Datei | Zweck |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Haupttestdatei |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Gecachte Audio-Clips |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Gecachte Transcripts |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Cache aus Git ausschließen |
| `conftest.py` (Repo-Root) | Setzt PYTHONPATH für pytest |

---

## 3. Test-Modi

### Modus A – Vosk only (Baseline)
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
Testet nur Vosk-Qualität. Kein Aura. Schnell.

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

### Modus C – Volle Aura-Pipeline, exakter Output
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
Für Segmente wo ein bekannter Befehl gesprochen wird. Schärfster Test.

---

## 4. Was wird getestet — was nicht

| Was | Getestet? |
|---|---|
| Vosk STT-Qualität | ✅ |
| FuzzyMap Pre-Regeln | ✅ (wenn Aura läuft) |
| LanguageTool-Korrekturen | ✅ (wenn LT läuft) |
| FuzzyMap Post-Regeln | ✅ (wenn Aura läuft) |
| Keyboard-Output (AutoHotkey/CopyQ) | ❌ bewusst — OS-Ebene, keine Logik |
| Vosk-Modell-Loading | ❌ — Aura liest Output-Datei, lädt kein Modell neu |

Der Output wird aus `tts_output_*.txt` im Temp-Verzeichnis gelesen — genau so wie Aura es intern macht, nicht aus dem Terminal.

---

## 5. Startbefehle

### Normaler Testlauf (Aura muss bereits laufen):
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

### Mit vollem Log:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

### Nur bestimmte Tests:
```bash
# Nur Aura-Tests
.venv/bin/pytest ... -k "aura"

# Nur Vosk-Baseline
.venv/bin/pytest ... -k "not aura"

# Einen spezifischen Test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

### Aura + LT zuerst starten:
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # prüfen ob LT läuft
```

---

## 6. Wichtige Konfiguration

### Sprachcodes — zwei verschiedene Systeme!

| System | Code | Beispiel |
|---|---|---|
| Vosk-Modell-Ordner | `de` | `models/vosk-model-de-0.21` |
| Aura FuzzyMap-Ordner | `de-DE` | `config/maps/.../de-DE/` |
| YouTube Transcript API | `de` | `api.fetch(..., languages=["de"])` |

**Lösung im Code:** `language="de-DE"` setzen. Der Code macht automatisch:
- Für Vosk: `"de-DE"` → `"de"` (split auf `-`)
- Für YouTube: `"de-DE"` → `"de"` (split auf `-`)
- Für Aura: `"de-DE"` direkt

### Auto-Translator deaktivieren vor Tests:
```bash
# Backup wiederherstellen (deaktiviert Auto-Translator):
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
Sonst übersetzt Aura deutschen Text ins Englische — das verfälscht den WER.

---

## 7. Bekannte Probleme & Lösungen

| Problem | Ursache | Lösung |
|---|---|---|
| `SKIPPED` sofort | YouTube-Transcript nicht gefunden | `api.list('video_id')` aufrufen um verfügbare Sprachen zu sehen |
| `SKIPPED` nach Audio | Vosk-Modell nicht gefunden | `language.split("-")[0]` Fallback im Code |
| `Found 0 FUZZY_MAP_pre rules` | Falscher Sprachcode an Aura | `"de-DE"` statt `"de"` verwenden |
| `Connection refused 8010` | LT nicht gestartet | Aura zuerst starten, 60s warten |
| `zsh: terminated` | X11-Watchdog killt Prozess | `SDL_VIDEODRIVER=dummy` verwenden; Watchdog-Schwellenwert erhöhen |
| YouTube `>>` Marker | Zweitsprecher im Transcript | `re.sub(r'>>', '', text)` — nur `>>` entfernen, Wörter behalten |
| `AttributeError: get_transcript` | youtube-transcript-api v1.x | `api = YouTubeTranscriptApi(); api.fetch(...)` statt Klassenmethod |
| Cache enthält leeren Text | Alter Lauf mit kaputtem Regex | `rm fixtures/youtube_clips/*.transcript.json` |

---

## 8. Ergebnisse bis jetzt

### Video: `sOjRNICiZ7Q` (Deutsch), Segment 5–20s

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

**Beobachtungen:**
- Aura hat eine Regel angewendet: `zehn finger` → `10 finger` ✅
- LT-Status während dieses Laufs unklar — Verbindung wurde verweigert
- Hoher WER liegt am Segment: YouTube-Transcript beginnt mit Wörtern die Vosk nicht hört (Sprecher noch nicht am Mikro)
- **Empfehlung:** Segment verschieben auf einen Bereich wo klar gesprochen wird

---

## 9. Empfehlungen für nächste Schritte

1. **Besseres Segment wählen** — `ffplay` nutzen um die genaue Sekunde zu finden wo klar gesprochen wird
2. **LT-Status im Test prüfen** — `curl http://localhost:8010/v2/languages` vor dem Test
3. **Modus C Tests hinzufügen** — Segmente wo bekannte Befehle gesprochen werden (`expected_output`)

---
---

# SL5 Aura – Audio Regression Tests: Status Report

**Date:** 2026-03-14  
**File:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. What was built

A test system that:
1. Downloads an audio segment from a YouTube video (via `yt-dlp` + `ffmpeg`)
2. Fetches the auto-generated YouTube transcript for the same segment (via `youtube-transcript-api`)
3. Transcribes the audio through Vosk
4. Optionally passes the result through the **full Aura pipeline** (`process_text_in_background`)
5. Computes Word Error Rate (WER) between Aura output and YouTube transcript
6. Runs as an automated regression test via `pytest`

All downloads are cached (`scripts/py/func/checks/fixtures/youtube_clips/`) so subsequent runs are fast.

---

## 2. Files

| File | Purpose |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Main test file |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Cached audio clips |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Cached transcripts |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Exclude cache from Git |
| `conftest.py` (repo root) | Sets PYTHONPATH for pytest |

---

## 3. Test Modes

### Mode A – Vosk only (Baseline)
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
Tests Vosk quality only. No Aura. Fast.

### Mode B – Full Aura pipeline, WER comparison
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
Sends Vosk output through FuzzyMap Pre → LanguageTool → FuzzyMap Post.

### Mode C – Full Aura pipeline, exact output match
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
For segments containing a known voice command. Strictest test mode.

---

## 4. What is tested — what is not

| What | Tested? |
|---|---|
| Vosk STT quality | ✅ |
| FuzzyMap Pre rules | ✅ (when Aura running) |
| LanguageTool corrections | ✅ (when LT running) |
| FuzzyMap Post rules | ✅ (when Aura running) |
| Keyboard output (AutoHotkey/CopyQ) | ❌ intentional — OS level, no logic |
| Vosk model re-loading | ❌ — Aura reads output file, does not reload model |

Output is read from `tts_output_*.txt` in a temp directory — exactly as Aura does it internally, not from the terminal.

---

## 5. Start Commands

### Normal test run (Aura must already be running):
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

### With full log:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

### Specific tests only:
```bash
# Only Aura tests
.venv/bin/pytest ... -k "aura"

# Only Vosk baseline
.venv/bin/pytest ... -k "not aura"

# One specific test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

### Start Aura + LT first:
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # verify LT is up
```

---

## 6. Important Configuration

### Language codes — two different systems!

| System | Code | Example |
|---|---|---|
| Vosk model folder | `de` | `models/vosk-model-de-0.21` |
| Aura FuzzyMap folder | `de-DE` | `config/maps/.../de-DE/` |
| YouTube Transcript API | `de` | `api.fetch(..., languages=["de"])` |

**Solution in code:** set `language="de-DE"`. The code automatically handles:
- For Vosk: `"de-DE"` → `"de"` (split on `-`)
- For YouTube: `"de-DE"` → `"de"` (split on `-`)
- For Aura: `"de-DE"` directly

### Disable auto-translator before tests:
```bash
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
Otherwise Aura translates German text to English — which corrupts the WER measurement.

---

## 7. Known Issues & Solutions

| Problem | Cause | Fix |
|---|---|---|
| `SKIPPED` immediately | YouTube transcript not found | Call `api.list('video_id')` to see available languages |
| `SKIPPED` after audio | Vosk model not found | `language.split("-")[0]` fallback in code |
| `Found 0 FUZZY_MAP_pre rules` | Wrong language code passed to Aura | Use `"de-DE"` not `"de"` |
| `Connection refused 8010` | LT not started | Start Aura first, wait 60s |
| `zsh: terminated` | X11 watchdog kills process | Use `SDL_VIDEODRIVER=dummy`; raise watchdog threshold |
| YouTube `>>` markers | Second speaker in transcript | `re.sub(r'>>', '', text)` — remove `>>` only, keep words |
| `AttributeError: get_transcript` | youtube-transcript-api v1.x | Use `api = YouTubeTranscriptApi(); api.fetch(...)` |
| Cache contains empty text | Old run with broken regex | `rm fixtures/youtube_clips/*.transcript.json` |

---

## 8. Results so far

### Video: `sOjRNICiZ7Q` (German), segment 5–20s

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

**Observations:**
- Aura applied a rule: `zehn finger` → `10 finger` ✅
- LT status during this run unclear — connection was refused
- High WER is due to segment choice: YouTube transcript begins with words Vosk cannot hear (speaker not yet at mic)
- **Recommendation:** shift segment to a section with clear speech

---

## 9. Recommended Next Steps

1. **Choose a better segment** — use `ffplay` to find the exact second where speech is clear
2. **Verify LT status before test** — `curl http://localhost:8010/v2/languages` before running
3. **Add Mode C tests** — segments containing known voice commands (`expected_output`)
