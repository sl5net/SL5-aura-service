# SL5 Aura – Audio-Regressionstests: Statusbericht

**Datum:** 2026-03-14  
**Datei:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. Was wurde gebaut

Ein Testsystem das:
1. Ein Audio-Segment aus einem YouTube-Video herunterlädt (via `yt-dlp` + `ffmpeg`)
2. Das automatisch generierte YouTube-Transcript für dasselbe Segment abruft (via `youtube-transcript-api`)
3. Das Audio durch Vosk transkribiert
4. Optional wird das Ergebnis durch die **volle Aura-Pipeline** gesendet (`process_text_in_background`)
5. Die Word Error Rate (WER) zwischen Aura-Output und YouTube-Transcript berechnet
6. Per `pytest` wird automatischer Regressionstest ausgeführt

Alle Downloads werden gespeichert (`scripts/py/func/checks/fixtures/youtube_clips/`), sodass Folgetests schnell laufen.

---

## 2. Dateien

| Datei | Zweck |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Haupttestdatei |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Gecachte Audio-Clips |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Gecachte Transkripte |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Cache aus Git ausschließen |
| `conftest.py` (Repo-Root) | Setzt PYTHONPATH für pytest |

---

## 3. Testmodi

### Modus A – nur Vosk (Grundlinie)
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
Getestet nur Vosk-Qualität. Keine Aura. Schnell.

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
Für Segmente wird ein bekannter Befehl gesprochen. Schärfster-Test.

---

## 4. Was wird getestet — was nicht

| War | Getestet? |
|---|---|
| Vosk STT-Qualität | ✅ |
| FuzzyMap-Vorregeln | ✅ (wenn Aura läuft) |
| LanguageTool-Korrekturen | ✅ (wenn LT läuft) |
| FuzzyMap Post-Regeln | ✅ (wenn Aura läuft) |
| Tastatur-Ausgabe (AutoHotkey/CopyQ) | ❌ bewusst – OS-Ebene, keine Logik |
| Vosk-Modell-Loading | ❌ — Aura liest Output-Datei, lädt kein Modell neu |

Der Output wird aus `tts_output_*.txt` im Temp-Verzeichnis gelesen – genau so wie Aura es intern macht, nicht aus dem Terminal.

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

### Sprachcodes – zwei verschiedene Systeme!

| System | Code | Beispiel |
|---|---|---|
| Vosk-Modell-Ordner | `de` | `models/vosk-model-de-0.21` |
| Aura FuzzyMap-Ordner | `de-DE` | `config/maps/.../de-DE/` |
| YouTube-Transkript-API | `de` | `api.fetch(..., language=["de"])` |

**Lösung im Code:** `Sprache="de-DE"` setzen. Der Code macht automatisch:
- Für Vosk: „de-DE“ → „de“ (aufgeteilt auf „-“)
- Für YouTube: „de-DE“ → „de“ (aufgeteilt auf „-“)
- Für Aura: „de-DE“ direkt

### Auto-Translator vor Tests deaktivieren:
```bash
# Backup wiederherstellen (deaktiviert Auto-Translator):
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
Sonst übersetzt Aura deutschen Text ins Englische – das verfälscht den WER.

---

## 7. Bekannte Probleme & Lösungen

| Problem | Ursache | Lösung |
|---|---|---|
| `SKIPPED` sofort | YouTube-Transkript nicht gefunden | `api.list('video_id')` Aufrufen einer verfügbaren Sprache zu sehen |
| `SKIPPED` nach Audio | Vosk-Modell nicht gefunden | `Sprache.split("-")[0]` Fallback im Code |
| „0 FUZZY_MAP_pre-Regeln gefunden“ | Falscher Sprachcode an Aura | `"de-DE"` statt `"de"` verwenden |
| `Verbindung abgelehnt 8010` | LT nicht gestartet | Aura zuerst starten, 60er Jahre warten |
| `zsh: beendet` | X11-Watchdog killt Prozess | `SDL_VIDEODRIVER=dummy` verwenden; Watchdog-Schwellenwert erhöht |
| YouTube-Markierung „>>“ | Zweitsprecher im Transcript | `re.sub(r'>>', '', text)` — nur `>>` entfernen, Wörter behalten |
| `AttributeError: get_transcript` | youtube-transcript-api v1.x | `api = YouTubeTranscriptApi(); api.fetch(...)` statt Klassenmethod |
| Cache enthält leeren Text | Alter Lauf mit kaputtem Regex | `rm Fixtures/youtube_clips/*.transcript.json` |

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

1. **Besseres Segment wählen** — `ffplay` nutzt um die genaue Sekunde zu finden, wo klar gesprochen wird
2. **LT-Status im Test prüfen** — `curl http://localhost:8010/v2/linguals` vor dem Test
3. **Modus C Tests hinzufügen** – Segmente, in denen bekannte Befehle gesprochen werden (`expected_output`)

---
---

# SL5 Aura – Audio-Regressionstests: Statusbericht

**Datum:** 14.03.2026  
**Datei:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. Was gebaut wurde

Ein Testsystem, das:
1. Lädt ein Audiosegment von einem YouTube-Video herunter (über „yt-dlp“ + „ffmpeg“)
2. Ruft das automatisch generierte YouTube-Transkript für dasselbe Segment ab (über „youtube-transcript-api“)
3. Transkribiert das Audio über Vosk
4. Leitet das Ergebnis optional durch die **vollständige Aura-Pipeline** („process_text_in_background“).
5. Berechnet die Wortfehlerrate (WER) zwischen der Aura-Ausgabe und dem YouTube-Transkript
6. Läuft als automatisierter Regressionstest über „pytest“.

Alle Downloads werden zwischengespeichert (`scripts/py/func/checks/fixtures/youtube_clips/`), sodass nachfolgende Ausführungen schnell erfolgen.

---

## 2. Dateien

| Datei | Zweck |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Haupttestdatei |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Zwischengespeicherte Audioclips |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Zwischengespeicherte Transkripte |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Cache von Git ausschließen |
| `conftest.py` (Repo-Root) | Legt PYTHONPATH für pytest | fest

---

## 3. Testmodi

### Modus A – nur Vosk (Baseline)
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
Testet nur die Vosk-Qualität. Keine Aura. Schnell.

### Modus B – Vollständige Aura-Pipeline, WER-Vergleich
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
Sendet die Vosk-Ausgabe über FuzzyMap Pre → LanguageTool → FuzzyMap Post.

### Modus C – Vollständige Aura-Pipeline, exakte Ausgabeübereinstimmung
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
Für Segmente, die einen bekannten Sprachbefehl enthalten. Strengster Testmodus.

---

## 4. Was wird getestet – was nicht

| Was | Getestet? |
|---|---|
| Vosk STT-Qualität | ✅ |
| FuzzyMap Pre-Regeln | ✅ (wenn Aura läuft) |
| LanguageTool-Korrekturen | ✅ (bei laufendem LT) |
| FuzzyMap-Beitragsregeln | ✅ (wenn Aura läuft) |
| Tastaturausgabe (AutoHotkey/CopyQ) | ❌ absichtlich – Betriebssystemebene, keine Logik |
| Neuladen des Vosk-Modells | ❌ – Aura liest die Ausgabedatei, lädt das Modell nicht neu |

Die Ausgabe wird aus „tts_output_*.txt“ in einem temporären Verzeichnis gelesen – genau wie Aura es intern tut, nicht vom Terminal.

---

## 5. Startbefehle

### Normaler Testlauf (Aura muss bereits laufen):
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

### Mit vollständigem Protokoll:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

### Nur spezifische Tests:
```bash
# Only Aura tests
.venv/bin/pytest ... -k "aura"

# Only Vosk baseline
.venv/bin/pytest ... -k "not aura"

# One specific test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

### Zuerst Aura + LT starten:
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # verify LT is up
```

---

## 6. Wichtige Konfiguration

### Sprachcodes – zwei verschiedene Systeme!

| System | Code | Beispiel |
|---|---|---|
| Vosk-Modellordner | `de` | `models/vosk-model-de-0.21` |
| Aura FuzzyMap-Ordner | `de-DE` | `config/maps/.../de-DE/` |
| YouTube-Transkript-API | `de` | `api.fetch(..., language=["de"])` |

**Lösung im Code:** setze `Sprache="de-DE"`. Der Code verarbeitet automatisch Folgendes:
- Für Vosk: „de-DE“ → „de“ (aufgeteilt auf „-“)
- Für YouTube: „de-DE“ → „de“ (aufgeteilt in „-“)
- Für Aura: direkt „de-DE“.

### Autoübersetzer vor Tests deaktivieren:
```bash
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
Andernfalls übersetzt Aura deutschen Text ins Englische – was die WER-Messung verfälscht.

---

## 7. Bekannte Probleme und Lösungen

| Problem | Ursache | Fix |
|---|---|---|
| `SKIPPED` sofort | YouTube-Transkript nicht gefunden | Rufen Sie „api.list('video_id')“ auf, um die verfügbaren Sprachen anzuzeigen |
| `SKIPPED` nach Audio | Vosk-Modell nicht gefunden | `Sprache.split("-")[0]` Fallback im Code |
| „0 FUZZY_MAP_pre-Regeln gefunden“ | Falscher Sprachcode an Aura übergeben | Verwenden Sie „de-DE“ und nicht „de“ |
| `Verbindung abgelehnt 8010` | LT nicht gestartet | Zuerst Aura starten, 60 Sekunden warten |
| `zsh: beendet` | X11-Watchdog beendet Prozess | Verwenden Sie „SDL_VIDEODRIVER=dummy“; Watchdog-Schwelle erhöhen |
| YouTube-Markierungen „>>“ | Zweiter Redner im Transkript | `re.sub(r'>>', '', text)` – nur „>>“ entfernen, Wörter | behalten
| `AttributeError: get_transcript` | youtube-transcript-api v1.x | Verwenden Sie „api = YouTubeTranscriptApi(); api.fetch(...)` |
| Cache enthält leeren Text | Alter Lauf mit defekter Regex | `rm Fixtures/youtube_clips/*.transcript.json` |

---

## 8. Bisherige Ergebnisse

### Video: „sOjRNICiZ7Q“ (Deutsch), Segment 5–20s

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

**Beobachtungen:**
- Aura hat eine Regel angewendet: „zehn Finger“ → „10 Finger“ ✅
- LT-Status während dieses Laufs unklar – Verbindung wurde abgelehnt
- Hoher WER ist auf Segmentwahl zurückzuführen: YouTube-Transkript beginnt mit Wörtern, die Vosk nicht hören kann (Sprecher noch nicht am Mikrofon)
- **Empfehlung:** Verschieben Sie das Segment in einen Abschnitt mit klarer Sprache

---

## 9. Empfohlene nächste Schritte

1. **Wählen Sie ein besseres Segment** – verwenden Sie „ffplay“, um genau die Sekunde zu finden, in der die Sprache klar ist
2. **Überprüfen Sie den LT-Status vor dem Test** – „curl http://localhost:8010/v2/linguals“ vor der Ausführung
3. **Modus-C-Tests hinzufügen** – Segmente mit bekannten Sprachbefehlen („expected_output“)