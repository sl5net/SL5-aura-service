# Testy regresji audio – porównanie transkrypcji YouTube

Katalog ten zawiera lekki, rozwijający się w miarę upływu czasu pakiet regresji, który
weryfikuje jakość Vosk STT SL5 Aura w porównaniu z **prawdziwym dźwiękiem z Twojego własnego
Filmy z YouTube**.

---

## Układ katalogu

__KOD_BLOKU_0__

---

## Jak działa pojedynczy test

__KOD_BLOKU_1__

---

## Instalacja

__KOD_BLOKU_2__

Dodaj do `requirements-dev.txt`:
__KOD_BLOKU_3__

---

## Uruchamianie testów

__KOD_BLOKU_4__

---

## Dodawanie nowego przypadku testowego

Otwórz plik `test_youtube_audio_regression.py` i dołącz do `YOUTUBE_TEST_CASES`:

__KOD_BLOKU_5__

To wszystko. Żadnych innych plików do dotknięcia.

---

## Pamięć podręczna i Git

Katalog `fixtures/youtube_clips/` powinien być **ignorowany przez git** (dodaj do
`.gitignore` w razie potrzeby). Znajdują się w pamięci podręcznej pliki `.wav` i `.transcript.json`
czysto lokalne artefakty, które przyspieszają powtórki.

---

## Wskazówki dotyczące progu

| Scenariusz | Sugerowany `wer_threshold` |
|----------------------------------------|--------------------------------------|
| Czysta mowa studyjna, angielski | 0,10 – 0,15 |
| Swobodna mowa, angielski | 0,20 – 0,30 |
| Przemówienie niemieckie | 0,15 – 0,25 |
| Hałaśliwe tło | 0,30 – 0,45 |

Zacznij luźno (0,35) i dokręć, gdy zobaczysz, co faktycznie produkuje Vosk.

---

## Dlaczego transkrypcje YouTube są podstawą prawdy?

Automatyczne napisy w YouTube nie są idealne, ale są:
- **Zawsze dostępny** dla Twoich własnych filmów
- **Bezpłatne** – nie jest wymagane ręczne etykietowanie
- **Wystarczająco dobre**, aby wychwycić poważne regresje
- Wyprodukowane przez inny silnik ASR (Google) → niezależne odniesienie

Porównanie WER wychwytuje regresje, w których zmiana kodu powoduje powstanie Voska
znacznie gorzej w przypadku prawdziwego dźwięku, bez konieczności ręcznej transkrypcji
wszystko.