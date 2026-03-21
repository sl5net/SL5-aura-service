# اختبارات الانحدار الصوتي – مقارنة نص YouTube

يحتوي هذا الدليل على مجموعة انحدار خفيفة الوزن ومتطورة
يتحقق من جودة Vosk STT الخاصة بـ SL5 Aura مقابل الصوت الحقيقي الخاص بك
                                       مقاطع فيديو يوتيوب **.

                                                                          ---

                                                   ## تخطيط الدليل

```
scripts/py/func/checks/
├── test_youtube_audio_regression.py   ← the test file (add cases here)
└── fixtures/
    └── youtube_clips/                 ← auto-created, git-ignored cache
        ├── my_test_id.wav
        └── my_test_id.transcript.json
```

                                                                          ---

                                     ## كيف يعمل اختبار واحد

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

                                                                ## تثبيت

```bash
# Python dependencies
pip install yt-dlp youtube-transcript-api vosk jiwer pytest

# System dependency (must be on PATH)
sudo apt install ffmpeg        # Debian/Ubuntu
# or: brew install ffmpeg      # macOS
# or: choco install ffmpeg     # Windows
```

                                        أضف إلى `requirements-dev.txt`:
```
yt-dlp
youtube-transcript-api
vosk
jiwer
pytest
```

                                                                          ---

                                           ## تشغيل الاختبارات

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

                               ## إضافة حالة اختبار جديدة

افتح `test_youtube_audio_regression.py` وألحقه بـ `YOUTUBE_TEST_CASES`:

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

              هذا كل شيء. لا توجد ملفات أخرى للمس.

                                                                          ---

                           ## ذاكرة التخزين المؤقت وجيت

يجب أن يكون الدليل `fixtures/youtube_clips/` **git-ignored** (إضافة إلى
`.gitignore` إذا لزم الأمر). الملفات ".wav" و".transcript.json" المخزنة مؤقتًا موجودة
المصنوعات اليدوية المحلية البحتة التي تسرع عمليات إعادة التشغيل.

                                                                          ---

                                               ## إرشادات العتبة

                          | السيناريو | اقترح `wer_threshold` |
                  |-----------------------------------------------|---------|
| خطاب الاستوديو النظيف، الإنجليزية | 0.10 – 0.15 |
               | خطاب عارضة، الإنجليزية | 0.20 – 0.30 |
                                    | خطاب ألماني | 0.15 – 0.25 |
                                    | خلفية صاخبة | 0.30 – 0.45 |

ابدأ فضفاضًا (0.35) وشد بمجرد رؤية ما ينتجه Vosk بالفعل.

                                                                          ---

## لماذا تعتبر النصوص المكتوبة على YouTube بمثابة الحقيقة الأساسية؟

التسميات التوضيحية التلقائية على YouTube ليست مثالية، ولكنها:
    - **متاح دائمًا** لمقاطع الفيديو الخاصة بك
- **مجاني** - لا حاجة إلى وضع العلامات اليدوية
- **جيد بما فيه الكفاية** للقبض على الانتكاسات الخطيرة
- تم إنتاجه بواسطة محرك ASR مختلف (Google) ← مرجع مستقل

تكتشف مقارنة WER الانحدارات حيث يؤدي تغيير الكود إلى حدوث Vosk
أسوأ بكثير على الصوت الحقيقي، دون الحاجة إلى النسخ يدويًا
                                                                   أي شئ.