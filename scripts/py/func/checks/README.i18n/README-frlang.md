# Tests de régression audio – Comparaison des transcriptions YouTube

Ce répertoire contient une suite de régression légère et évolutive qui
vérifie la qualité Vosk STT du SL5 Aura par rapport à **l'audio réel de votre propre
Vidéos YouTube**.

---

## Disposition du répertoire

```
scripts/py/func/checks/
├── test_youtube_audio_regression.py   ← the test file (add cases here)
└── fixtures/
    └── youtube_clips/                 ← auto-created, git-ignored cache
        ├── my_test_id.wav
        └── my_test_id.transcript.json
```

---

## Comment fonctionne un test unique

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

##Installation

```bash
# Python dependencies
pip install yt-dlp youtube-transcript-api vosk jiwer pytest

# System dependency (must be on PATH)
sudo apt install ffmpeg        # Debian/Ubuntu
# or: brew install ffmpeg      # macOS
# or: choco install ffmpeg     # Windows
```

Ajoutez à `requirements-dev.txt` :
```
yt-dlp
youtube-transcript-api
vosk
jiwer
pytest
```

---

## Exécution des tests

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

## Ajout d'un nouveau cas de test

Ouvrez `test_youtube_audio_regression.py` et ajoutez à `YOUTUBE_TEST_CASES` :

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

C'est ça. Aucun autre fichier à toucher.

---

## Cache et Git

Le répertoire `fixtures/youtube_clips/` doit être **git-ignoré** (ajouter à
`.gitignore` si nécessaire). Les fichiers `.wav` et `.transcript.json` mis en cache sont
des artefacts purement locaux qui accélèrent les rediffusions.

---

## Conseils sur le seuil

| Scénario | `wer_threshold` suggéré |
|-------------------------------|-------------------------------|
| Discours propre en studio, Anglais | 0,10 – 0,15 |
| Discours informel, anglais | 0,20 – 0,30 |
| Discours allemand | 0,15 – 0,25 |
| Fond bruyant | 0,30 – 0,45 |

Commencez lâchement (0,35) et resserrez une fois que vous voyez ce que Vosk produit réellement.

---

## Pourquoi les transcriptions YouTube comme vérité terrain ?

Les sous-titres automatiques de YouTube ne sont pas parfaits, mais ils le sont :
- **Toujours disponible** pour vos propres vidéos
- **Gratuit** – aucun étiquetage manuel nécessaire
- **Assez bon** pour détecter de sérieuses régressions
- Produit par un autre moteur ASR (Google) → référence indépendante

La comparaison WER détecte les régressions où un changement de code rend Vosk
nettement pire sur l'audio réel, sans avoir besoin de transcrire manuellement
rien.