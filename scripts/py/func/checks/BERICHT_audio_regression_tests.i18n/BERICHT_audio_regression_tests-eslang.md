# SL5 Aura – Pruebas de regresión de audio: Statusbericht

**Dato:** 2026-03-14  
**Fecha:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. Was wurde gebaut

Un sistema de prueba das:
1. Un segmento de audio en un video de YouTube grabado (a través de `yt-dlp` + `ffmpeg`)
2. La transcripción de YouTube generada automáticamente para el siguiente segmento (a través de `youtube-transcript-api`)
3. Das Audio durch Vosk transkribiert
4. Opcional das Ergebnis durch die **volle Aura-Pipeline** schickt (`process_text_in_background`)
5. La tasa de error de palabras (WER) entre la salida de Aura y la transcripción de YouTube
6. Por `pytest` como prueba de regresión automática

Todas las descargas se realizan (`scripts/py/func/checks/fixtures/youtube_clips/`), así que las pruebas completas se ejecutan rápidamente.

---

## 2. Fecha

| Fechai | Zweck |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Fechas principales |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Clips de audio obtenidos |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Transcripciones de Gecachte |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Caché en Git adicional |
| `conftest.py` (Repo-Root) | Configure PYTHONPATH para pytest |

---

## 3. Prueba-Modi

### Modus A: solo Vosk (línea de base)
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
Testet nur Vosk-Qualität. Kein Aura. Schnell.

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
Schickt Vosk-Output a través de FuzzyMap Pre → LanguageTool → FuzzyMap Post.

### Modus C – Volle Aura-Pipeline, salida exacta
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
Für Segmente wo ein bekannter Befehl gesprochen wird. Prueba de Schärfster.

---

## 4. Was wird getestet – was nicht

| Fue | ¿Getestet? |
|---|---|
| Calidad Vosk STT | ✅ |
| FuzzyMap Pre-Regeln | ✅ (cuando Aura läuft) |
| LanguageTool-Correkturen | ✅ (cuando LT läuft) |
| FuzzyMap Post-Regeln | ✅ (cuando Aura läuft) |
| Salida de teclado (AutoHotkey/CopyQ) | ❌ bewusst — OS-Ebene, no hay lógica |
| Vosk-Modell-Cargando | ❌ — Aura liest Output-Datei, lädt kein Modell neu |

La salida se encuentra en `tts_output_*.txt` en la versión temporal: por lo tanto, Aura es interna, no en la terminal.

---

## 5. Iniciar sesión

### Testlauf normal (Aura muss bereits laufen):
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

### Mit vollem Registro:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

### Nuestras mejores pruebas:
```bash
# Nur Aura-Tests
.venv/bin/pytest ... -k "aura"

# Nur Vosk-Baseline
.venv/bin/pytest ... -k "not aura"

# Einen spezifischen Test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

### Aura + LT por primera vez iniciado:
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # prüfen ob LT läuft
```

---

## 6. Configuración adecuada

### Sprachcodes: ¡dos sistemas diferentes!

| Sistema | Código | Beispiel |
|---|---|---|
| Vosk-Modell-Ordner | `de` | `modelos/vosk-model-de-0.21` |
| Aura FuzzyMap-Ordenador | `de-DE` | `config/maps/.../de-DE/` |
| API de transcripción de YouTube | `de` | `api.fetch(..., idiomas=["de"])` |

**Lösung im Code:** `language="de-DE"` setzen. El código funciona automáticamente:
- Para Vosk: `"de-DE"` → `"de"` (dividido en `-`)
- Para YouTube: `"de-DE"` → `"de"` (dividido en `-`)
- Para Aura: `"de-DE"` directamente

### Auto-Translator deaktivieren vor Tests:
```bash
# Backup wiederherstellen (deaktiviert Auto-Translator):
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
Sonst übersetzt Aura deutschen Texto en inglés — das verfälscht den WER.

---

## 7. Bekannte Probleme & Lösungen

| Problema | Osa | Lösung |
|---|---|---|
| `SALTADO` sofort | Transcripción de YouTube nicht gefunden | `api.list('video_id')` muestra un mensaje verfügbare para ver |
| `SKIPPED` después del audio | Vosk-Modell no recibe fondos | `language.split("-")[0]` Reserva en el código |
| `Se encontraron 0 reglas FUZZY_MAP_pre` | Falscher Sprachcode y Aura | `"de-DE"` en lugar de `"de"` utilizado |
| `Conexión rechazada 8010` | LT no gestartet | Aura zuerst starten, años 60 |
| `zsh: terminado` | X11-Watchdog mata el proceso | `SDL_VIDEODRIVER=dummy` utilizado; Vigilancia-Schwellenwert erhöhen |
| YouTube `>>` Marcador | Zweitsprecher im Transcripción | `re.sub(r'>>', '', texto)` — ahora `>>` entfernen, Wörter behalten |
| `AttributeError: get_transcript` | youtube-transcripción-api v1.x | `api = YouTubeTranscriptApi(); api.fetch(...)` en lugar de método de clase |
| Caché enthält leeren Texto | Alter Lauf mit kaputtem Regex | `rm accesorios/youtube_clips/*.transcript.json` |

---

## 8. Ergebnisse bis jetzt

### Vídeo: `sOjRNICiZ7Q` (alemán), segmento 5–20

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

**Beobachtungen:**
- Aura hat eine Regel angewendet: `zehn dedo` → `10 dedo` ✅
- LT-Status während dieses Laufs unklar — Verbindung wurde verweigert
- Hoher WER liegt am Segment: YouTube-Transcripción comienza con Wörtern die Vosk nicht hört (Sprecher noch nicht am Mikro)
- **Empfehlung:** Segment verschieben auf einen Bereich wo klar gesprochen wird

---

## 9. Empfehlungen für nächste Schritte

1. **Besseres Segment wählen** — `ffplay` nutzen um die genaue Sekunde zu finden wo klar gesprochen wird
2. **LT-Status im Test prüfen** — `curl http://localhost:8010/v2/languages` para la prueba
3. **Modo C Tests hinzufügen** — Segmente wo bekannte Befehle gesprochen werden (`expected_output`)

---
---

# SL5 Aura – Pruebas de regresión de audio: Informe de estado

**Fecha:** 2026-03-14  
**Archivo:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. Qué se construyó

Un sistema de prueba que:
1. Descarga un segmento de audio de un video de YouTube (a través de `yt-dlp` + `ffmpeg`)
2. Obtiene la transcripción de YouTube generada automáticamente para el mismo segmento (a través de `youtube-transcript-api`).
3. Transcribe el audio a través de Vosk.
4. Opcionalmente, pasa el resultado a través del **canal completo de Aura** (`process_text_in_background`)
5. Calcula la tasa de error de palabras (WER) entre la salida de Aura y la transcripción de YouTube
6. Se ejecuta como una prueba de regresión automatizada mediante "pytest".

Todas las descargas se almacenan en caché (`scripts/py/func/checks/fixtures/youtube_clips/`), por lo que las ejecuciones posteriores son rápidas.

---

## 2. Archivos

| Archivo | Propósito |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Archivo de prueba principal |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Clips de audio en caché |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Transcripciones almacenadas en caché |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Excluir caché de Git |
| `conftest.py` (raíz del repositorio) | Establece PYTHONPATH para pytest |

---

## 3. Modos de prueba

### Modo A: solo Vosk (línea de base)
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
Prueba únicamente la calidad de Vosk. Sin aura. Rápido.

### Modo B – Tubería de Aura completa, comparación WER
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
Envía la salida de Vosk a través de FuzzyMap Pre → LanguageTool → FuzzyMap Post.

### Modo C: tubería de aura completa, coincidencia exacta de salida
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
Para segmentos que contienen un comando de voz conocido. Modo de prueba más estricto.

---

## 4. Lo que se prueba y lo que no

| Qué | ¿Probado? |
|---|---|
| Calidad Vosk STT | ✅ |
| Reglas previas de FuzzyMap | ✅ (cuando Aura corre) |
| Correcciones de LanguageTool | ✅ (cuando LT está funcionando) |
| Reglas de publicación de FuzzyMap | ✅ (cuando Aura corre) |
| Salida de teclado (AutoHotkey/CopyQ) | ❌ intencional: nivel de sistema operativo, sin lógica |
| Recarga del modelo Vosk | ❌ — Aura lee el archivo de salida, no recarga el modelo |

La salida se lee desde `tts_output_*.txt` en un directorio temporal, exactamente como lo hace Aura internamente, no desde la terminal.

---

## 5. Comandos de inicio

### Ejecución de prueba normal (Aura ya debe estar ejecutándose):
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

### Con registro completo:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

### Sólo pruebas específicas:
```bash
# Only Aura tests
.venv/bin/pytest ... -k "aura"

# Only Vosk baseline
.venv/bin/pytest ... -k "not aura"

# One specific test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

### Inicie Aura + LT primero:
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # verify LT is up
```

---

## 6. Configuración importante

### Códigos de idioma: ¡dos sistemas diferentes!

| Sistema | Código | Ejemplo |
|---|---|---|
| Carpeta modelo Vosk | `de` | `modelos/vosk-model-de-0.21` |
| Carpeta Aura FuzzyMap | `de-DE` | `config/maps/.../de-DE/` |
| API de transcripción de YouTube | `de` | `api.fetch(..., idiomas=["de"])` |

**Solución en código:** establezca `language="de-DE"`. El código maneja automáticamente:
- Para Vosk: `"de-DE"` → `"de"` (dividido en `-`)
- Para YouTube: `"de-DE"` → `"de"` (dividido en `-`)
- Para Aura: `"de-DE"` directamente

### Deshabilite el traductor automático antes de las pruebas:
```bash
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
De lo contrario, Aura traduce el texto del alemán al inglés, lo que corrompe la medición del WER.

---

## 7. Problemas conocidos y soluciones

| Problema | Causa | Arreglar |
|---|---|---|
| `SALTADO` inmediatamente | Transcripción de YouTube no encontrada | Llame a `api.list('video_id')` para ver los idiomas disponibles |
| `SALTADO` después del audio | Modelo Vosk no encontrado | `language.split("-")[0]` respaldo en el código |
| `Se encontraron 0 reglas FUZZY_MAP_pre` | Se pasó un código de idioma incorrecto a Aura | Utilice `"de-DE"` no `"de"` |
| `Conexión rechazada 8010` | LT no iniciado | Inicie Aura primero, espere 60 segundos |
| `zsh: terminado` | El perro guardián X11 finaliza el proceso | Utilice `SDL_VIDEODRIVER=ficticio`; elevar el umbral de vigilancia |
| Marcadores `>>` de YouTube | Segundo orador en la transcripción | `re.sub(r'>>', '', text)` — elimina `>>` únicamente, conserva las palabras |
| `AttributeError: get_transcript` | youtube-transcripción-api v1.x | Utilice `api = YouTubeTranscriptApi(); api.fetch(...)` |
| La caché contiene texto vacío | Ejecución antigua con expresiones regulares rotas | `rm accesorios/youtube_clips/*.transcript.json` |

---

## 8. Resultados hasta el momento

### Vídeo: `sOjRNICiZ7Q` (alemán), segmento 5–20

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

**Observaciones:**
- Aura aplicó una regla: `zehn dedo` → `10 dedo` ✅
- El estado de LT durante esta ejecución no está claro: se rechazó la conexión
- El WER alto se debe a la elección del segmento: la transcripción de YouTube comienza con palabras que Vosk no puede oír (el orador aún no está frente al micrófono)
- **Recomendación:** cambiar el segmento a una sección con un discurso claro

---

## 9. Próximos pasos recomendados

1. **Elija un segmento mejor**: use `ffplay` para encontrar el segundo exacto en el que el habla es clara
2. **Verifique el estado de LT antes de la prueba** — `curl http://localhost:8010/v2/languages` antes de ejecutar
3. **Agregar pruebas en Modo C**: segmentos que contienen comandos de voz conocidos (`expected_output`)