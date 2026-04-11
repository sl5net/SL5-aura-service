# Przewodnik po zasadach FUZZY_MAP

## Format reguły

__KOD_BLOKU_0__

| Pozycja | Imię | Opis |
|---|---|---|
| 1 | wymiana | Tekst wyjściowy po dopasowaniu reguły |
| 2 | wzór | Regex lub ciąg rozmyty do dopasowania do |
| 3 | próg | Ignorowane ze względu na reguły wyrażeń regularnych. Używane do dopasowywania rozmytego (0–100) |
| 4 | flagi | `{'flagi': re.IGNORECASE}` dla nieuwzględniania wielkości liter, `0` dla rozróżniania wielkości liter |

## Logika potoku

- Reguły są przetwarzane **z góry na dół**
- **Wszystkie** reguły dopasowywania są stosowane (skumulowane)
- **fullmatch** (`^...$`) natychmiast zatrzymuje potok
- Wcześniejsze zasady mają pierwszeństwo przed późniejszymi zasadami

## Typowe wzorce

### Dopasuj pojedyncze słowo (granica słowa)
__KOD_BLOKU_1__

### Dopasuj wiele wariantów
__KOD_BLOKU_2__

### Fullmatch – zatrzymuje potok
__KOD_BLOKU_3__
⚠️ To pasuje do **wszystko**. Rurociąg zatrzymuje się w tym miejscu. Wcześniejsze zasady nadal mają pierwszeństwo.

### Dopasuj początek wejścia
__KOD_BLOKU_4__

### Dopasuj dokładną frazę
__KOD_BLOKU_5__

## Lokalizacje plików

| Plik | Faza | Opis |
|---|---|---|
| `FUZZY_MAP_pre.py` | Narzędzie do nauki języka | Stosowane przed sprawdzaniem pisowni |
| `FUZZY_MAP.py` | Narzędzie post-językowe | Stosowane po sprawdzeniu pisowni |
| `PUNCTUATION_MAP.py` | Narzędzie do nauki języka | Zasady interpunkcji |

## Porady

- Umieść **szczegółowe** zasady przed **ogólnymi** zasadami
- Używaj `^...$` pełnego dopasowania tylko wtedy, gdy chcesz zatrzymać całe dalsze przetwarzanie
- `FUZZY_MAP_pre.py` jest idealny do poprawek przed sprawdzeniem pisowni
- Reguły testowe za pomocą: „Twojego wejścia testowego” w konsoli Aura
- Kopie zapasowe są tworzone automatycznie jako `.peter_backup`

## Przykłady

__KOD_BLOKU_6__

## Twoja pierwsza zasada — krok po kroku

1. Otwórz `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. Dodaj swoją regułę wewnątrz `FUZZY_MAP_pre = [...]`
3. Zapisz — Aura ładuje się automatycznie, nie ma potrzeby ponownego uruchamiania
4. Podyktuj frazę wyzwalającą i obserwuj, jak zadziała


## Zalecana struktura plików

Umieść swoje reguły **przed** długimi blokami komentarzy:
__KOD_BLOKU_7__

**Dlaczego?** Funkcja Auto-Fix firmy Aura skanuje tylko pierwszy ~1KB pliku.
Jeśli reguły pojawiają się po długim nagłówku, funkcja Auto-Fix nie może ich znaleźć ani naprawić.
Zalecany jest także komentarz do ścieżki w linii 1 — pomaga on szybko zidentyfikować plik.