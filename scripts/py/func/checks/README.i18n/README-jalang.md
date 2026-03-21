# オーディオ回帰テスト – YouTube トランスクリプトの比較

このディレクトリには、軽量で成長に応じて成長する回帰スイートが含まれています。
SL5 Aura の Vosk STT 品質を**実際のオーディオと比較して検証します
YouTube ビデオ**。

---

## ディレクトリのレイアウト

```
scripts/py/func/checks/
├── test_youtube_audio_regression.py   ← the test file (add cases here)
└── fixtures/
    └── youtube_clips/                 ← auto-created, git-ignored cache
        ├── my_test_id.wav
        └── my_test_id.transcript.json
```

---

## 単一のテストの仕組み

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

## インストール

```bash
# Python dependencies
pip install yt-dlp youtube-transcript-api vosk jiwer pytest

# System dependency (must be on PATH)
sudo apt install ffmpeg        # Debian/Ubuntu
# or: brew install ffmpeg      # macOS
# or: choco install ffmpeg     # Windows
```

`requirements-dev.txt` に以下を追加します。
```
yt-dlp
youtube-transcript-api
vosk
jiwer
pytest
```

---

## テストの実行

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

## 新しいテスト ケースの追加

「test_youtube_audio_regression.py」を開き、「YOUTUBE_TEST_CASES」に追加します。

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

それでおしまい。他に触れるファイルはありません。

---

## キャッシュと Git

`fixtures/youtube_clips/` ディレクトリは **git-ignored** である必要があります (追加
必要に応じて `.gitignore` を追加します)。キャッシュされた `.wav` および `.transcript.json` ファイルは次のとおりです。
再実行を高速化する純粋にローカルなアーティファクト。

---

## しきい値のガイダンス

|シナリオ |推奨される `wer_threshold` |
|----------------------------|--------------------------|
|クリーンスタジオでのスピーチ、英語 | 0.10 – 0.15 |
|カジュアルスピーチ、英語 | 0.20 – 0.30 |
|ドイツ語のスピーチ | 0.15 – 0.25 |
|騒々しい背景 | 写真 騒々しい背景0.30 – 0.45 |

まずは緩め（0.35）から始めて、Vosk が実際に生成するものを確認したら締めてください。

---

## YouTube トランスクリプトをグラウンド トゥルースとして使用する理由

YouTube の自動字幕は完璧ではありませんが、次のとおりです。
- **自分のビデオでいつでも利用可能**
- **無料** – 手動でラベルを付ける必要はありません
- **深刻な後退を検出するには十分**
- 別の (Google) ASR エンジンによって生成 → 独立したリファレンス

WER 比較は、コード変更により Vosk が変更される回帰を検出します。
実際の音声では大幅に悪化し、手動で文字起こしする必要はありません
何でも。