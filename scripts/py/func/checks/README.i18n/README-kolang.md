# 오디오 회귀 테스트 - YouTube 대본 비교

이 디렉토리에는 경량의 성장에 따른 회귀 제품군이 포함되어 있습니다.
**실제 오디오와 비교하여 SL5 Aura의 Vosk STT 품질을 확인합니다.
YouTube 동영상**.

---

## 디렉토리 레이아웃

```
scripts/py/func/checks/
├── test_youtube_audio_regression.py   ← the test file (add cases here)
└── fixtures/
    └── youtube_clips/                 ← auto-created, git-ignored cache
        ├── my_test_id.wav
        └── my_test_id.transcript.json
```

---

## 단일 테스트 작동 방식

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

## 설치

```bash
# Python dependencies
pip install yt-dlp youtube-transcript-api vosk jiwer pytest

# System dependency (must be on PATH)
sudo apt install ffmpeg        # Debian/Ubuntu
# or: brew install ffmpeg      # macOS
# or: choco install ffmpeg     # Windows
```

`requirements-dev.txt`에 추가:
```
yt-dlp
youtube-transcript-api
vosk
jiwer
pytest
```

---

## 테스트 실행

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

## 새 테스트 케이스 추가

`test_youtube_audio_regression.py`를 열고 `YOUTUBE_TEST_CASES`에 추가합니다.

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

그게 다야. 다른 파일을 건드릴 수 없습니다.

---

## 캐시 & Git

`fixtures/youtube_clips/` 디렉토리는 **git-무시**되어야 합니다(추가
필요한 경우 `.gitignore`). 캐시된 `.wav` 및 `.transcript.json` 파일은 다음과 같습니다.
재실행 속도를 높이는 순전히 로컬 인공물입니다.

---

## 임계값 지침

| 시나리오 | 'wer_threshold' 제안 |
|------------------|-------------|
| 클린 스튜디오 스피치, 영어 | 0.10 – 0.15 |
| 캐주얼 스피치, 영어 | 0.20 – 0.30 |
| 독일어 연설 | 0.15 – 0.25 |
| 시끄러운 배경 | 0.30 – 0.45 |

느슨하게(0.35) 시작하고 Vosk가 실제로 생산하는 것을 확인한 후에 조이세요.

---

## YouTube 스크립트를 Ground Truth로 사용하는 이유는 무엇인가요?

YouTube의 자동 캡션은 완벽하지는 않지만 다음과 같습니다.
- 자신의 동영상에 **항상 사용 가능**
- **무료** – 수동 라벨링이 필요하지 않습니다.
- **심각한 회귀를 포착하기에 충분함**
- 다른 (Google) ASR 엔진으로 제작 → 독립적인 참조

WER 비교는 코드 변경으로 인해 Vosk가
수동으로 전사할 필요 없이 실제 오디오에서는 훨씬 더 나쁩니다.
아무것.