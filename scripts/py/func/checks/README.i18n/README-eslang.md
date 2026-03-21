# Pruebas de regresión de audio: comparación de transcripciones de YouTube

Este directorio contiene un conjunto de regresión liviano que crece sobre la marcha y que
verifica la calidad Vosk STT de SL5 Aura con **audio real propio
Vídeos de YouTube**.

---

## Diseño del directorio

```
scripts/py/func/checks/
├── test_youtube_audio_regression.py   ← the test file (add cases here)
└── fixtures/
    └── youtube_clips/                 ← auto-created, git-ignored cache
        ├── my_test_id.wav
        └── my_test_id.transcript.json
```

---

## Cómo funciona una prueba única

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

## Instalación

```bash
# Python dependencies
pip install yt-dlp youtube-transcript-api vosk jiwer pytest

# System dependency (must be on PATH)
sudo apt install ffmpeg        # Debian/Ubuntu
# or: brew install ffmpeg      # macOS
# or: choco install ffmpeg     # Windows
```

Agregar a `requisitos-dev.txt`:
```
yt-dlp
youtube-transcript-api
vosk
jiwer
pytest
```

---

## Ejecutando las pruebas

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

## Agregar un nuevo caso de prueba

Abra `test_youtube_audio_regression.py` y agréguelo a `YOUTUBE_TEST_CASES`:

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

Eso es todo. No hay otros archivos para tocar.

---

## Caché y Git

El directorio `fixtures/youtube_clips/` debe ser **git-ignored** (agregar a
`.gitignore` si es necesario). Los archivos `.wav` y `.transcript.json` almacenados en caché son
artefactos puramente locales que aceleran las repeticiones.

---

## Guía de umbral

| Escenario | `wer_threshold` sugerido |
|-------------------------------|--------------------------|
| Discurso de estudio limpio, inglés | 0,10 – 0,15 |
| Discurso informal, Inglés | 0,20 – 0,30 |
| discurso alemán | 0,15 – 0,25 |
| Fondo ruidoso | 0,30 – 0,45 |

Empiece flojo (0,35) y apriete una vez que vea lo que realmente produce Vosk.

---

## ¿Por qué las transcripciones de YouTube son verdad fundamental?

Los subtítulos automáticos de YouTube no son perfectos, pero lo son:
- **Siempre disponible** para tus propios videos
- **Gratis**: no es necesario etiquetar manualmente
- **Lo suficientemente bueno** para detectar regresiones graves
- Producido por un motor ASR diferente (Google) → referencia independiente

La comparación WER detecta regresiones en las que un cambio de código hace que Vosk
significativamente peor en audio real, sin necesidad de transcribir manualmente
cualquier cosa.