# Abschlussbericht: SL5 Aura – Uruchomienie kompleksowego testu

**Data:** 2026-03-15XSPACEbreakX
**Data:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. Plan Der

Ein echter End-to-End Test der das bekannte Problem untersucht:
**Bei manchen Aufnahmen fehlt das letzte Wort im Output.**

Solta testu:
1. Eine WAV-Datei als constainles Mikrofon einspeisen
2. Aura per `touch /tmp/sl5_record.trigger` starten — genau wie im echten Betrieb
3. Mit zweitem Zatrzymanie wyzwalacza
4. Plik wyjściowy z transkrypcją YouTube-vergleichen
5. Feststellen ob ein Wort am Ende fehlt

---

## 2. Was erreicht wurde ✅

- Aura reagiert auf den Trigger korrekt
- LT läuft und ist erreichbar (`http://127.0.0.1:8082`)
- `_wait_for_output()` znajdź kość `tts_output_*.txt` Datei
- `_fetch_yt_transcript_segment()` holt den Referenz-Text korrekt
- Der grundlegende Testaufbau ist solide und funktioniert konzeptionell

---

## 3. Das ungelöste Problem 🔴

### Problem z Kernem: `manage_audio_routing` überschreibt alles

Beim Session-Start ruft Aura stażysta auf:
__KOD_BLOKU_0__

Diese Funktion macht als erstes:
__KOD_BLOKU_1__

**Sie löscht jeden Sink den wir vorher erstellt haben.**

Danach erstellt sie keinen neuen Sink weil `mode == 'SYSTEM_DEFAULT'` (nicht `MIC_AND_DESKTOP`).

### Versuchte Lösungen

| Versuch | Problem |
|---|---|
| Utwórz wirtualne źródło PulseAudio | PipeWire ignoruje `moduł-wirtualne-źródło' |
| `settings_local.py` na `MIC_AND_DESKTOP` setzen | Datei wurde mit mehrfachen Einträgen korrumpiert |
| Zaznacz blok override-block i koniec schreiben | Aura lädt Ustawienia nicht schnell genug neu bevor Trigger kommt |
| `_create_mic_and_desktop_sink()` bezpośrednio w teście | Wird von `manage_audio_routing` przy rozpoczęciu sesji Gelöscht |
| `pw-pętla zwrotna` | Erscheint als Source aber Aura hört nicht darauf |

### Warum `settings_local.py` Zastąp funkcję nicht

`dynamic_settings.py` überwacht die Datei und lädt sie nach — aber mit einem Intervall. Der Trigger kommt zu schnell nach dem Schreiben. Aura starte die Session noch mit dem alten Wert `SYSTEM_DEFAULT`.

Außerdem: selbst wenn Aura `MIC_AND_DESKTOP` lädt, erstellt es den Sink erst beim **nächsten** Session-Start — nicht sofort.

---

## 4. Mögliche Lösungswege

### Opcja A — Längeres Warten nach Settings-Ęnderung
__KOD_BLOKU_2__
Risiko: Nicht zuverlässig, Timing-abhängig.

### Opcja B — Aura neu starten nach Settings-Ęnderung
__KOD_BLOKU_3__
Nachteil: Test dauert über 1 minuta. Aber zuverlässig.

### Opcja C — `manage_audio_routing` bezpośrednio w teście aufrufen
__KOD_BLOKU_4__
Dann istnieje der Sink bevor der Trigger kommt — i `manage_audio_routing` przy rozpoczęciu sesji po wykonaniu `is_mic_and_desktop_sink_active() == True` i überspringt das Setup.

Das ist wahrscheinlich die **sauberste Lösung**.

### Opcja D — `process_text_in_background` direkt aufrufen (kein Trigger)
Zobacz w `test_youtube_audio_regression.py` — Vosk-Output direkt in die Pipeline übergeben, ohne den echten Trigger-Mechanismus. Dann testet man die Pipeline aber nicht das Abschneiden des letzten Wortes.

### Opcja E — Aura mit `run_mode_override=TEST` starten
Falls Aura einen Test-Modus hat der das Audio-Routing überspringt.

---

## 5. Uwolnij

**Opcja C** zuerst probieren — einen Import-Test machen:

__KOD_BLOKU_5__

Wenn das funktioniert:
__KOD_BLOKU_6__

Dann erkennt Aura beim Session-Start `is_mic_and_desktop_sink_active() == True` i ostatni zlew w Ruhe.

---

## 6. Was dieser Test langfristig Bringt

Sobald er läuft, kann man:
- `SPEECH_PAUSE_TIMEOUT` Werte testen (1.0, 2.0, 4.0s) and seehen ob das letzte Wort abgeschnitten wird
- `transcribe_audio_with_feedback.py` Optymalizacja parametrów
- Regressionen erkennen wenn sich das Audio-Handling ändert
- Beweisen dass ein Fix wirklich hilft

---

---

# Raport końcowy: SL5 Aura – uruchomienie kompleksowego testu

**Data:** 2026-03-15XSPACEbreakX
**Plik:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. Plan

Prawdziwy, kompleksowy test mający na celu zbadanie znanego problemu:
**W niektórych nagraniach ostatnie słowo na wyjściu jest obcinane.**

Test powinien:
1. Podaj plik WAV jako wirtualny mikrofon
2. Uruchom Aurę poprzez `touch /tmp/sl5_record.trigger` — dokładnie tak, jak w rzeczywistym użyciu
3. Zatrzymaj się za pomocą drugiego spustu
4. Porównaj wyniki z transkrypcją YouTube
5. Sprawdź, czy na końcu brakuje słowa

---

## 2. Co udało się osiągnąć ✅

- Aura prawidłowo reaguje na spust
- LT działa i jest osiągalny (`http://127.0.0.1:8082`)
- `_wait_for_output()` znajduje plik `tts_output_*.txt`
- `_fetch_yt_transcript_segment()` poprawnie pobiera tekst referencyjny
- Podstawowa struktura testu jest solidna i działa koncepcyjnie

---

## 3. Nierozwiązany problem 🔴

### Podstawowy problem: „manage_audio_routing” zastępuje wszystko

Na początku sesji Aura wewnętrznie wywołuje:
__KOD_BLOKU_7__

Ta funkcja najpierw wykonuje:
__KOD_BLOKU_8__

**Usuwa wszystkie ujścia, które wcześniej utworzyliśmy.**

Następnie nie tworzy nowego ujścia, ponieważ `mode == 'SYSTEM_DEFAULT'` (a nie `MIC_AND_DESKTOP`).

### Próby rozwiązań

| Próba | Problem |
|---|---|
| Utwórz wirtualne źródło PulseAudio | PipeWire ignoruje `wirtualne-źródło modułu` |
| Ustaw `settings_local.py` na `MIC_AND_DESKTOP` | Plik został uszkodzony z wieloma wpisami |
| Zapisz zaznaczony blok nadpisania na końcu pliku | Aura nie ładuje ustawień wystarczająco szybko przed uruchomieniem spustu |
| `_create_mic_and_desktop_sink()` bezpośrednio w teście | Usunięte przez `manage_audio_routing` na początku sesji |
| `pw-pętla zwrotna` | Pojawia się jako źródło, ale Aura go nie słucha |

---

## 4. Zalecany następny krok

Wywołaj `manage_audio_routing` bezpośrednio z testu przed wyzwalaczem:

__KOD_BLOKU_9__

Kiedy Aura rozpoczyna sesję, sprawdza `is_mic_and_desktop_sink_active()` — jeśli `True`, pomija konfigurację i pozostawia zlew w spokoju. To najczystsze rozwiązanie.

---

## 5. Co ten test umożliwi w dłuższej perspektywie

Po uruchomieniu:
- Przetestuj wartości `SPEECH_PAUSE_TIMEOUT` (1,0, 2,0, 4,0 s) i wykryj obcięcie słowa
- Zoptymalizuj parametry `transcribe_audio_with_feedback.py`
- Wychwytuj regresje, gdy zmienia się obsługa dźwięku
- Udowodnij, że poprawka rzeczywiście działa