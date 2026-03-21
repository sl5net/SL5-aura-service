# SL5 Aura – Testy regresji audio: Statusbericht

**Data:** 2026-03-14XSPACEbreakX
**Data:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. Was wurde gebaut

W systemie testowym da się:
1. Ein Audio-Segment aus einem YouTube-Video herunterlädt (przez `yt-dlp` + `ffmpeg`)
2. Den automatisch generierten YouTube-Transcript für dasselbe Segment abruft (przez `youtube-transcript-api`)
3. Das Audio durch Vosk transkribiert
4. Opcjonalnie das Ergebnis durch die **volle Aura-Pipeline** schickt (`process_text_in_background`)
5. Die Word Error Rate (WER) zwischen Aura-Output i YouTube-Transcript berechnet
6. Per `pytest` als automatischer Regresionstest läuft

Wszystkie pliki do pobrania werden gecacht (`scripts/py/func/checks/fixtures/youtube_clips/`), sodass Folgetests schnell laufen.

---

## 2. Data

| Data | Zweck |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Najświeższa data testu |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Klipy audio Gecachte |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Transkrypcje Gecachte |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Pamięć podręczna z Git ausschließen |
| `conftest.py` (Repo-Root) | Setzt PYTHONPATH dla testu |

---

## 3. Test-Modi

### Modus A – tylko Vosk (linia bazowa)
__KOD_BLOKU_0__
Testet nur Vosk-Qualität. Kluczowa Aura. Schnell.

### Modus B – Volle Aura-Pipeline, WER-Vergleich
__KOD_BLOKU_1__
Schickt Vosk-Output podczas FuzzyMap Pre → LanguageTool → FuzzyMap Post.

### Modus C – Volle Aura-Pipeline, exakter Output
__KOD_BLOKU_2__
Für Segmente wo ein bekannter Befehl gesprochen wird. Test Schärfstera.

---

## 4. Was wird getestet — było nicht

| Był | Getestet? |
|---|---|
| Jakość Vosk STT | ✅ |
| FuzzyMap przed regeln | ✅ (wenn Aura läuft) |
| LanguageTool-Korektura | ✅ (wenn LT läuft) |
| FuzzyMap po Regeln | ✅ (wenn Aura läuft) |
| Wyjście z klawiatury (AutoHotkey/CopyQ) | ❌ bewusst — OS-Ebene, keine Logik |
| Ładowanie modelu Vosk | ❌ — Aura Liest Output-Datei, lädt kein Modell neu |

Der Output wird aus `tts_output_*.txt` w Temp-Verzeichnis gelesen — genau więc wie Aura es intern macht, nicht aus dem Terminal.

---

## 5. Uruchombefehle

### Normalny testlauf (Aura muss bereits laufen):
__KOD_BLOKU_3__

### Mit volem Log:
__KOD_BLOKU_4__

### Nur bestimmte Testy:
__KOD_BLOKU_5__

### Aura + LT należy rozpocząć:
__KOD_BLOKU_6__

---

## 6. Konfiguracja Wichtige

### Sprachcodes — zwei verschiedene Systeme!

| Systemu | Kod | Beispiel |
|---|---|---|
| Vosk-Modell-Ordner | `de` | `models/vosk-model-de-0.21` |
| Zamawianie Aura FuzzyMap | `de-DE` | `config/maps/.../de-DE/` |
| Interfejs API transkrypcji YouTube | `de` | `api.fetch(..., języki=["de"])` |

**Umieszczony kod:** `language="de-DE"` setzen. Kod macht automatyczny:
- Für Vosk: `"de-DE"` → `"de"` (split auf `-`)
- Für YouTube: `"de-DE"` → `"de"` (split auf `-`)
- Für Aura: `"de-DE"` direkt

### Auto-tłumacz deaktywowany przed testami:
__KOD_BLOKU_7__
Sonst übersetzt Aura deutschen Text ins Englische — das verfälscht den WER.

---

## 7. Rozwiązywanie problemów i losowanie

| Problem | Ursache | Losung |
|---|---|---|
| `POMIŃCZONE` sofort | Transkrypcja YouTube nicht gefunden | `api.list('video_id')` aufrufen um verfügbare Sprachen zu see |
| `POMIŃCZONE` nach Audio | Vosk-Modell nicht gefunden | `language.split("-")[0]` Zastępczy kod |
| `Znaleziono 0 reguł FUZZY_MAP_pre` | Falscher Sprachcode i aura | `"de-DE"` statt `"de"` verwenden |
| `Odmowa połączenia 8010` | LT nicht gestartet | Aura zuerst starten, lata 60. warton |
| `zsh: zakończone` | X11-Watchdog zabił Prozessa | `SDL_VIDEODRIVER= atrapa` użyj; Pies stróżujący-Schwellenwert erhöhen |
| Znacznik YouTube `>>` | Zweitsprecher im Transkrypcja | `re.sub(r'>>', '', tekst)` — nur `>>` entfernen, Wörter behalten |
| `Błąd atrybutu: get_transcript` | youtube-transkrypt-api v1.x | `api = YouTubeTranscriptApi(); api.fetch(...)` statt Klassenmethod |
| Zapisz tekst w pamięci podręcznej | Alter Lauf mit kaputtem Regex | `rm oprawy/youtube_clips/*.transcript.json` |

---

## 8. Ergebnisse bis jetzt

### Wideo: `sOjRNICiZ7Q` (niemiecki), segment 5–20 s

__KOD_BLOKU_8__

**Beobachtungen:**
- Aura hat eine Regel angewendet: `zehn palec` → `10 palec` ✅
- LT-Status während dieses Laufs unklar — Verbindung wurde verweigert
- Hoher WER Liegt am Segment: YouTube-Transkrypcja Beginnt mit Wörtern die Vosk nicht hört (Sprecher noch nicht am Mikro)
- **Empfehlung:** Segment verschieben auf einen Bereich wo klar gesprochen wird

---

## 9. Empfehlungen für nächste Schritte

1. **Besseres Segment wählen** — `ffplay` nutzen um die genaue Sekunde zu finden wo klar gesprochen wird
2. **Status LT w teście prüfen** — `curl http://localhost:8010/v2/languages` dla testu
3. **Modus C Tests hinzufügen** — Segmente wo bekannte Befehle gesprochen werden („oczekiwany_wynik”)

---
---

# SL5 Aura – Testy regresji dźwięku: Raport stanu

**Data:** 2026-03-14XSPACEbreakX
**Plik:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. Co zostało zbudowane

System testowy, który:
1. Pobiera fragment audio z filmu z YouTube (poprzez `yt-dlp` + `ffmpeg`)
2. Pobiera automatycznie wygenerowaną transkrypcję YouTube dla tego samego segmentu (za pośrednictwem `youtube-transcript-api`)
3. Transkrypcja dźwięku poprzez Vosk
4. Opcjonalnie przekazuje wynik przez **pełny potok Aura** (`process_text_in_background`)
5. Oblicza współczynnik błędów Word (WER) pomiędzy danymi wyjściowymi Aury a transkrypcją YouTube
6. Działa jako automatyczny test regresji poprzez `pytest`

Wszystkie pliki do pobrania są zapisywane w pamięci podręcznej (`scripts/py/func/checks/fixtures/youtube_clips/`), więc kolejne uruchomienia przebiegają szybko.

---

## 2. Pliki

| Plik | Cel |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` | Główny plik testowy |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Zapisane w pamięci podręcznej klipy audio |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Zapisy w pamięci podręcznej |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Wyklucz pamięć podręczną z Git |
| `conftest.py` (korzeń repozytorium) | Ustawia PYTHONPATH dla pytest |

---

## 3. Tryby testowe

### Tryb A – tylko Vosk (linia bazowa)
__KOD_BLOKU_9__
Testuje tylko jakość Vosk. Brak aury. Szybko.

### Tryb B – potok pełnej aury, porównanie WER
__KOD_BLOKU_10__
Wysyła dane wyjściowe Voska poprzez FuzzyMap Pre → LanguageTool → FuzzyMap Post.

### Tryb C – potok pełnej aury, dokładne dopasowanie wyjściowe
__KOD_BLOKU_11__
Dla segmentów zawierających znane polecenie głosowe. Najbardziej rygorystyczny tryb testowy.

---

## 4. Co jest testowane — a co nie

| Co | Przetestowany? |
|---|---|
| Jakość Vosk STT | ✅ |
| Zasady wstępne FuzzyMap | ✅ (kiedy Aura działa) |
| Poprawki języka | ✅ (kiedy działa LT) |
| FuzzyMap Zasady postu | ✅ (kiedy Aura działa) |
| Wyjście klawiatury (AutoHotkey/CopyQ) | ❌ zamierzone — poziom systemu operacyjnego, brak logiki |
| Ponowne ładowanie modelu Voska | ❌ — Aura czyta plik wyjściowy, nie ładuje ponownie modelu |

Dane wyjściowe są odczytywane z `tts_output_*.txt` w katalogu tymczasowym — dokładnie tak, jak Aura robi to wewnętrznie, a nie z terminala.

---

## 5. Uruchom polecenia

### Normalne uruchomienie testowe (Aura musi już działać):
__KOD_BLOKU_12__

### Z pełnym logiem:
__KOD_BLOKU_13__

### Tylko określone testy:
__KOD_BLOKU_14__

### Najpierw uruchom Aurę + LT:
__KOD_BLOKU_15__

---

## 6. Ważna konfiguracja

### Kody językowe — dwa różne systemy!

| Systemu | Kod | Przykład |
|---|---|---|
| Folder modelu Vosk | `de` | `models/vosk-model-de-0.21` |
| Folder Aura FuzzyMap | `de-DE` | `config/maps/.../de-DE/` |
| Interfejs API transkrypcji YouTube | `de` | `api.fetch(..., języki=["de"])` |

**Rozwiązanie w kodzie:** set `language="de-DE"`. Kod automatycznie obsługuje:
- Dla Voska: `"de-DE"` → `"de"` (podzielone na `-`)
- Dla YouTube: `"de-DE"` → `"de"` (podzielone na `-`)
- Dla Aury: bezpośrednio „de-DE”.

### Wyłącz autotłumacz przed testami:
__KOD_BLOKU_16__
W przeciwnym razie Aura tłumaczy tekst niemiecki na angielski, co zaburza pomiar WER.

---

## 7. Znane problemy i rozwiązania

| Problem | Przyczyna | Napraw |
|---|---|---|
| `POMIŃCZONE` natychmiast | Nie znaleziono transkrypcji YouTube | Wywołaj `api.list('video_id')`, aby zobaczyć dostępne języki |
| `POMIŃCZONO` po dźwięku | Nie znaleziono modelu Voska | `language.split("-")[0]` zastępczy kod |
| `Znaleziono 0 reguł FUZZY_MAP_pre` | Do Aury przesłano błędny kod językowy | Użyj `"de-DE"`, a nie `"de"` |
| `Odmowa połączenia 8010` | LT nie rozpoczęło się | Najpierw uruchom Aurę, poczekaj 60 s |
| `zsh: zakończone` | Watchdog X11 zabija proces | Użyj `SDL_VIDEODRIVER= atrapa`; podnieś próg watchdoga |
| Znaczniki YouTube `>>` | Drugi mówca w transkrypcji | `re.sub(r'>>', '', tekst)` — usuń tylko `>>`, zachowaj słowa |
| `Błąd atrybutu: get_transcript` | youtube-transkrypt-api v1.x | Użyj `api = YouTubeTranscriptApi(); api.fetch(...)` |
| Pamięć podręczna zawiera pusty tekst | Stary bieg z uszkodzonym wyrażeniem regularnym | `rm oprawy/youtube_clips/*.transcript.json` |

---

## 8. Dotychczasowe wyniki

### Wideo: `sOjRNICiZ7Q` (niemiecki), segment 5–20

__KOD_BLOKU_17__

**Obserwacje:**
- Aura zastosowała zasadę: `zehn palec` → `10 palec` ✅
- Stan LT podczas tego przebiegu jest niejasny — połączenie zostało odrzucone
– Wysoki WER wynika z wyboru segmentu: transkrypcja YouTube zaczyna się od słów, których Vosk nie słyszy (mówca nie jest jeszcze przy mikrofonie)
- **Zalecenie:** przesuń segment do sekcji, w której mowa jest wyraźna

---

## 9. Zalecane kolejne kroki

1. **Wybierz lepszy segment** — użyj „ffplay”, aby znaleźć dokładną sekundę, w której mowa jest wyraźna
2. **Sprawdź status LT przed testem** — `curl http://localhost:8010/v2/languages` przed uruchomieniem
3. **Dodaj testy Mode C** — segmenty zawierające znane polecenia głosowe („oczekiwane_wyjście”)