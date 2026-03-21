# Audio-Regressionstests – Vergleich von YouTube-Transkripten

Dieses Verzeichnis enthält eine schlanke Regressionssuite, die jederzeit wächst
Verifiziert die Vosk STT-Qualität des SL5 Aura im Vergleich zu **echtem Audio von Ihrem eigenen Gerät
YouTube-Videos**.

---

## Verzeichnislayout

```
scripts/py/func/checks/
├── test_youtube_audio_regression.py   ← the test file (add cases here)
└── fixtures/
    └── youtube_clips/                 ← auto-created, git-ignored cache
        ├── my_test_id.wav
        └── my_test_id.transcript.json
```

---

## So funktioniert ein einzelner Test

```
YouTube video URL
      │
      ▼
  yt-dlp + ffmpeg          → trims & converts to 16 kHz mono WAV  (cached)
      │
      ├──► youtube-transcript-api  → fetches auto-captions for the same
      │                              time window                   (cached)
      │
      ▼
   Vosk model               → transcribes the WAV
      │
      ▼
   jiwer WER                → compares Vosk output vs YT transcript
      │
      ▼
  pytest assert WER ≤ threshold
```

---

## Installation

```bash
# Python dependencies
pip install yt-dlp youtube-transcript-api vosk jiwer pytest

# System dependency (must be on PATH)
sudo apt install ffmpeg        # Debian/Ubuntu
# or: brew install ffmpeg      # macOS
# or: choco install ffmpeg     # Windows
```

Zu „requirements-dev.txt“ hinzufügen:
```
yt-dlp
youtube-transcript-api
vosk
jiwer
pytest
```

---

## Ausführen der Tests

```bash
# All audio regression tests
pytest scripts/py/func/checks/test_youtube_audio_regression.py -v

# One specific test case by ID
pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -k "sl5_aura_demo_en_v1"

# Re-fetch transcripts (delete cache first)
rm scripts/py/func/checks/fixtures/youtube_clips/*.json
pytest scripts/py/func/checks/test_youtube_audio_regression.py -v
```

---

## Einen neuen Testfall hinzufügen

Öffnen Sie „test_youtube_audio_regression.py“ und hängen Sie an „YOUTUBE_TEST_CASES“ an:

```python
YoutubeAudioTestCase(
    test_id       = "my_video_segment_01",   # unique slug → used as cache filename
    video_id      = "XXXXXXXXXXX",           # YouTube ID from ?v=... in the URL
    start_sec     = 30,                      # clip start (seconds)
    end_sec       = 45,                      # clip end   (seconds)
    language      = "en",                    # "en" or "de" (must match a Vosk model)
    wer_threshold = 0.25,                    # allow up to 25% word errors
    notes         = "Short description of what this segment tests",
)
```

Das ist es. Keine anderen Dateien zum Anfassen.

---

## Cache und Git

Das Verzeichnis „fixtures/youtube_clips/“ sollte **git-ignored** sein (hinzufügen zu
`.gitignore` bei Bedarf). Die zwischengespeicherten Dateien „.wav“ und „.transcript.json“ sind
rein lokale Artefakte, die Wiederholungen beschleunigen.

---

## Schwellenwert-Anleitung

| Szenario | Vorgeschlagener „wer_threshold“ |
|----------------|------------|
| Saubere Studiorede, Englisch | 0,10 – 0,15 |
| Lässige Rede, Englisch | 0,20 – 0,30 |
| Deutsche Rede | 0,15 – 0,25 |
| Lauter Hintergrund | 0,30 – 0,45 |

Beginnen Sie locker (0,35) und ziehen Sie es fest, sobald Sie sehen, was Vosk tatsächlich produziert.

---

## Warum YouTube-Transkripte als Ground Truth?

Die automatischen Untertitel von YouTube sind nicht perfekt, aber sie sind:
- **Immer verfügbar** für Ihre eigenen Videos
- **Kostenlos** – keine manuelle Etikettierung erforderlich
- **Gut genug**, um ernsthafte Rückschritte zu erkennen
- Produziert von einer anderen (Google) ASR-Engine → unabhängige Referenz

Der WER-Vergleich erfasst Regressionen, bei denen eine Codeänderung zu Vosk führt
deutlich schlechter bei echtem Audio, ohne dass eine manuelle Transkription erforderlich ist
irgendetwas.