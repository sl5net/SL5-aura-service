# Audio Regression Tests – YouTube Transcript Comparison

This directory contains a lightweight, grow-as-you-go regression suite that
verifies SL5 Aura's Vosk STT quality against **real audio from your own
YouTube videos**.

---

## Directory Layout

```
scripts/py/func/checks/
├── test_youtube_audio_regression.py   ← the test file (add cases here)
└── fixtures/
    └── youtube_clips/                 ← auto-created, git-ignored cache
        ├── my_test_id.wav
        └── my_test_id.transcript.json
```

---

## How a Single Test Works

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

Add to `requirements-dev.txt`:
```
yt-dlp
youtube-transcript-api
vosk
jiwer
pytest
```

---

## Running the Tests

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

## Adding a New Test Case

Open `test_youtube_audio_regression.py` and append to `YOUTUBE_TEST_CASES`:

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

That's it. No other files to touch.

---

## Cache & Git

The `fixtures/youtube_clips/` directory should be **git-ignored** (add to
`.gitignore` if needed). The cached `.wav` and `.transcript.json` files are
purely local artefacts that speed up re-runs.

---

## Threshold Guidance

| Scenario                      | Suggested `wer_threshold` |
|-------------------------------|--------------------------|
| Clean studio speech, English  | 0.10 – 0.15              |
| Casual speech, English        | 0.20 – 0.30              |
| German speech                 | 0.15 – 0.25              |
| Noisy background              | 0.30 – 0.45              |

Start loose (0.35) and tighten once you see what Vosk actually produces.

---

## Why YouTube Transcripts as Ground Truth?

YouTube's auto-captions are not perfect, but they are:
- **Always available** for your own videos
- **Free** – no manual labelling needed
- **Good enough** to catch serious regressions
- Produced by a different (Google) ASR engine → independent reference

The WER comparison catches regressions where a code change makes Vosk
significantly worse on real audio, without needing to manually transcribe
anything.
