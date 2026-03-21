# Testes de regressão de áudio – comparação de transcrições do YouTube

Este diretório contém um conjunto de regressão leve e crescente que
verifica a qualidade Vosk STT do SL5 Aura em relação ao ** áudio real do seu próprio
Vídeos do YouTube**.

---

## Layout do diretório

```
scripts/py/func/checks/
├── test_youtube_audio_regression.py   ← the test file (add cases here)
└── fixtures/
    └── youtube_clips/                 ← auto-created, git-ignored cache
        ├── my_test_id.wav
        └── my_test_id.transcript.json
```

---

## Como funciona um único teste

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

## Instalação

```bash
# Python dependencies
pip install yt-dlp youtube-transcript-api vosk jiwer pytest

# System dependency (must be on PATH)
sudo apt install ffmpeg        # Debian/Ubuntu
# or: brew install ffmpeg      # macOS
# or: choco install ffmpeg     # Windows
```

Adicione ao `requirements-dev.txt`:
__CODE_BLOCO_3__

---

## Executando os testes

```
yt-dlp
youtube-transcript-api
vosk
jiwer
pytest
```

---

## Adicionando um novo caso de teste

Abra `test_youtube_audio_regression.py` e anexe a `YOUTUBE_TEST_CASES`:

__CODE_BLOCO_5__

É isso. Nenhum outro arquivo para tocar.

---

## Cache e Git

O diretório `fixtures/youtube_clips/` deve ser **git-ignored** (adicione ao
`.gitignore` se necessário). Os arquivos `.wav` e `.transcript.json` armazenados em cache são
artefatos puramente locais que aceleram as repetições.

---

## Orientação de limite

| Cenário | `wer_threshold` sugerido |
|------------------------------------------|--------------------------|
| Discurso de estúdio limpo, inglês | 0,10 – 0,15 |
| Discurso casual, inglês | 0,20 – 0,30 |
| Discurso alemão | 0,15 – 0,25 |
| Fundo barulhento | 0,30 – 0,45 |

Comece solto (0,35) e aperte quando ver o que Vosk realmente produz.

---

## Por que as transcrições do YouTube são verdadeiras?

As legendas automáticas do YouTube não são perfeitas, mas são:
- **Sempre disponível** para seus próprios vídeos
- **Grátis** – não é necessária etiquetagem manual
- **Bom o suficiente** para capturar regressões sérias
- Produzido por um mecanismo ASR diferente (Google) → referência independente

A comparação WER captura regressões onde uma mudança de código faz Vosk
significativamente pior em áudio real, sem a necessidade de transcrever manualmente
qualquer coisa.