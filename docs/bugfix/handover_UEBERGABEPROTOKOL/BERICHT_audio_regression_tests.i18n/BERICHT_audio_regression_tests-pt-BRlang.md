# SL5 Aura – Testes de regressão de áudio: Statusbericht

**Dado:** 2026-03-14  
**Data:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. Foi wurde gebaut

Um sistema de teste das:
1. Um segmento de áudio de um vídeo do YouTube herunterlädt (via `yt-dlp` + `ffmpeg`)
2. A transcrição do YouTube gerada automaticamente para o segmento inicial (via `youtube-transcript-api`)
3. O áudio durante a tradução de Vosk
4. Opcional das Ergebnis durch die **volle Aura-Pipeline** schickt (`process_text_in_background`)
5. Taxa de erro de palavra (WER) entre saída da Aura e transcrição do YouTube
6. Por `pytest` como teste de regressão automático realizado

Todos os downloads foram registrados (`scripts/py/func/checks/fixtures/youtube_clips/`), então Folgetests schnell laufen.

---

## 2. Encontro

| Data | Zweck |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Data principal do teste |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Clipes de áudio Gecachte |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Transcrições Gecachte |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Cache do Git removido |
| `conftest.py` (Repo-Root) | Definir PYTHONPATH para pytest |

---

## 3. Mod de teste

### Modus A – apenas Vosk (linha de base)
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
Testado pela Vosk-Qualität. Kein Aura. Schnell.

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
Schickt Vosk-Output durch FuzzyMap Pré → LanguageTool → FuzzyMap Post.

### Modus C – Volle Aura-Pipeline, saída exata
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
Para segmentar qual será o melhor resultado. Teste de Schärfster.

---

## 4. Was wird getestet — was nicht

| Foi | Getestet? |
|---|---|
| Vosk STT-Qualidade | ✅ |
| Pré-registo do FuzzyMap | ✅ (quando Aura läuft) |
| Correção do LanguageTool | ✅ (quando LT läuft) |
| FuzzyMap Pós-Regência | ✅ (quando Aura läuft) |
| Saída do teclado (AutoHotkey/CopyQ) | ❌ bewusst — OS-Ebene, keine Logik |
| Carregamento de modelo Vosk | ❌ — Auraliest Output-Data, lädt kein Modell neu |

A saída é `tts_output_*.txt` na verificação de temperatura - geralmente como a Aura é internamente, não no Terminal.

---

## 5. Início da vida

### Normaler Testlauf (Aura muss bereits laufen):
__CODE_BLOCO_3__

### Mit vollem Log:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

### Testes recomendados:
__CODE_BLOCO_5__

### Aura + LT primeiro iniciado:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

---

## 6. Qual configuração

### Sprachcodes — dois sistemas diferentes!

| Sistema | Código | Beispiel |
|---|---|---|
| Vosk-Modell-Ordner | `de` | `modelos/vosk-model-de-0.21` |
| Ordenador de Mapa Aura Fuzzy | `de-DE` | `config/maps/.../de-DE/` |
| API de transcrição do YouTube | `de` | `api.fetch(..., idiomas=["de"])` |

**Lösung im Code:** `linguagem="de-DE"` setzen. O código faz isso automaticamente:
- Para Vosk: `"de-DE"` → `"de"` (dividido em `-`)
- Para YouTube: `"de-DE"` → `"de"` (dividido em `-`)
- Für Aura: `"de-DE"` diretamente

### Auto-Tradutor desativado para testes:
```bash
# Nur Aura-Tests
.venv/bin/pytest ... -k "aura"

# Nur Vosk-Baseline
.venv/bin/pytest ... -k "not aura"

# Einen spezifischen Test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```
Sonst übersetzt Aura deutschen Texto em inglês — das verfälscht den WER.

---

## 7. Bekannte Probleme & Lösungen

| Problema | Ursache | Lösung |
|---|---|---|
| `SKIPPED` suave | Transcrição do YouTube não obtida | `api.list('video_id')` aumenta uma extensão para ver |
| `SKIPPED` nach Áudio | Modelos de voo não financiados | `linguagem.split("-")[0]` Fallback no código |
| `Encontradas 0 regras FUZZY_MAP_pre` | Falscher Sprachcode uma Aura | `"de-DE"` status `"de"` usado |
| `Conexão recusada 8010` | LT não foi iniciada | Aura zuerst starten, guerra dos anos 60 |
| `zsh: encerrado` | X11-Watchdog mata processo | `SDL_VIDEODRIVER=dummy` exibido; Watchdog-Schwellenwert erhöhen |
| Marcador `>>` do YouTube | Leia a transcrição | `re.sub(r'>>', '', text)` — apenas `>>` entfernen, Wörter behalten |
| `AttributeError: get_transcript` | youtube-transcript-api v1.x | `api = YouTubeTranscriptApi(); api.fetch(...)` status Klassenmethod |
| Cache enthält ler Texto | Alterar Lauf com Kaputtem Regex | `rm fixtures/youtube_clips/*.transcript.json` |

---

## 8. Ergebnisse bis jetzt

### Vídeo: `sOjRNICiZ7Q` (Alemão), segmento 5–20s

```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # prüfen ob LT läuft
```

**Beobachtungen:**
- Aura hat eine Regel angewendet: `zehn dedo` → `10 dedo` ✅
- LT-Status während dieses Laufs unklar — Verbindung wurde verweigert
- Hoher WER liegt am Segment: YouTube-Transcrição começa com Wörtern die Vosk nicht hört (Sprecher noch nicht am Mikro)
- **Empfehlung:** Segment verschieben auf einen Bereich wo klar gesprochen wird

---

## 9. Empfehlungen für nächste Schritte

1. **Besseres Segment wählen** — `ffplay` nutzen um die genaue Sekunde zu finden wo klar gesprochen wird
2. **LT-Status no teste prüfen** — `curl http://localhost:8010/v2/languages` antes do teste
3. **Modus C Tests Hinzufügen** — Segmente o que será feito antes do teste (`expected_output`)

---
---

# SL5 Aura – Testes de regressão de áudio: relatório de status

**Data:** 14/03/2026  
**Arquivo:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. O que foi construído

Um sistema de teste que:
1. Baixa um segmento de áudio de um vídeo do YouTube (via `yt-dlp` + `ffmpeg`)
2. Busca a transcrição gerada automaticamente pelo YouTube para o mesmo segmento (via `youtube-transcript-api`)
3. Transcreve o áudio através do Vosk
4. Opcionalmente, passa o resultado pelo **pipeline completo do Aura** (`process_text_in_background`)
5. Calcula a taxa de erros de palavras (WER) entre a saída do Aura e a transcrição do YouTube
6. Executa como um teste de regressão automatizado via `pytest`

Todos os downloads são armazenados em cache (`scripts/py/func/checks/fixtures/youtube_clips/`) para que as execuções subsequentes sejam rápidas.

---

## 2. Arquivos

| Arquivo | Finalidade |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Arquivo de teste principal |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Clipes de áudio armazenados em cache |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Transcrições em cache |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Excluir cache do Git |
| `conftest.py` (raiz do repositório) | Define PYTHONPATH para pytest |

---

## 3. Modos de teste

### Modo A – apenas Vosk (linha de base)
__CODE_BLOCO_9__
Testa apenas a qualidade Vosk. Sem Aura. Rápido.

### Modo B – Pipeline Full Aura, comparação WER
```bash
# Backup wiederherstellen (deaktiviert Auto-Translator):
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
Envia a saída Vosk através do FuzzyMap Pre → LanguageTool → FuzzyMap Post.

### Modo C – Pipeline Full Aura, correspondência exata de saída
```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```
Para segmentos contendo um comando de voz conhecido. Modo de teste mais rigoroso.

---

## 4. O que é testado - o que não é

| O que | Testado? |
|---|---|
| Qualidade Vosk STT | ✅ |
| Pré-regras do FuzzyMap | ✅ (quando a Aura está em execução) |
| Correções do LanguageTool | ✅ (quando LT estiver em execução) |
| Regras de postagem do FuzzyMap | ✅ (quando a Aura está em execução) |
| Saída do teclado (AutoHotkey/CopyQ) | ❌ intencional — nível do sistema operacional, sem lógica |
| Recarregamento do modelo Vosk | ❌ — Aura lê arquivo de saída, não recarrega modelo |

A saída é lida de `tts_output_*.txt` em um diretório temporário — exatamente como o Aura faz internamente, não no terminal.

---

## 5. Comandos de inicialização

### Execução de teste normal (o Aura já deve estar em execução):
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

### Com registro completo:
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

### Apenas testes específicos:
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

### Inicie o Aura + LT primeiro:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

---

## 6. Configuração importante

### Códigos de idioma — dois sistemas diferentes!

| Sistema | Código | Exemplo |
|---|---|---|
| Pasta do modelo Vosk | `de` | `modelos/vosk-model-de-0.21` |
| Pasta Aura FuzzyMap | `de-DE` | `config/maps/.../de-DE/` |
| API de transcrição do YouTube | `de` | `api.fetch(..., idiomas=["de"])` |

**Solução em código:** defina `linguagem="de-DE"`. O código trata automaticamente:
- Para Vosk: `"de-DE"` → `"de"` (dividido em `-`)
- Para YouTube: `"de-DE"` → `"de"` (dividido em `-`)
- Para Aura: `"de-DE"` diretamente

### Desative o tradutor automático antes dos testes:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```
Caso contrário, a Aura traduz o texto alemão para inglês – o que corrompe a medição WER.

---

## 7. Problemas e soluções conhecidos

| Problema | Causa | Correção |
|---|---|---|
| `SKIPPED` imediatamente | Transcrição do YouTube não encontrada | Chame `api.list('video_id')` para ver os idiomas disponíveis |
| `SKIPPED` após o áudio | Modelo Vosk não encontrado | `linguagem.split("-")[0]` fallback no código |
| `Encontradas 0 regras FUZZY_MAP_pre` | Código de idioma errado passado para Aura | Use `"de-DE"` e não `"de"` |
| `Conexão recusada 8010` | LT não iniciado | Inicie o Aura primeiro, espere 60 anos |
| `zsh: encerrado` | Watchdog X11 mata processo | Use `SDL_VIDEODRIVER=dummy`; aumentar limite de vigilância |
| Marcadores `>>` do YouTube | Segundo orador na transcrição | `re.sub(r'>>', '', text)` — remova apenas `>>`, mantenha as palavras |
| `AttributeError: get_transcript` | youtube-transcript-api v1.x | Use `api = YouTubeTranscriptApi(); api.fetch(...)` |
| Cache contém texto vazio | Corrida antiga com regex quebrada | `rm fixtures/youtube_clips/*.transcript.json` |

---

## 8. Resultados até agora

### Vídeo: `sOjRNICiZ7Q` (alemão), segmento 5–20s

```bash
# Only Aura tests
.venv/bin/pytest ... -k "aura"

# Only Vosk baseline
.venv/bin/pytest ... -k "not aura"

# One specific test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

**Observações:**
- Aura aplicou uma regra: `zehn dedo` → `10 dedo` ✅
- O status do LT durante esta execução não está claro — a conexão foi recusada
- O WER alto se deve à escolha do segmento: a transcrição do YouTube começa com palavras que Vosk não consegue ouvir (o locutor ainda não está no microfone)
- **Recomendação:** mude o segmento para uma seção com fala clara

---

## 9. Próximas etapas recomendadas

1. **Escolha um segmento melhor** — use `ffplay` para encontrar o segundo exato em que a fala é clara
2. **Verifique o status do LT antes do teste** — `curl http://localhost:8010/v2/languages` antes de executar
3. **Adicionar testes do Modo C** — segmentos contendo comandos de voz conhecidos (`expected_output`)