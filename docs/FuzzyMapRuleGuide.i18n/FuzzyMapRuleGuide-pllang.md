# Przewodnik po zasadach FUZZY_MAP

##Format reguły

__KOD_BLOKU_0__

| Pozycja | Imię | Opis |
|---|---|---|
| 1 | wymiana | Tekst wyjściowy po dopasowaniu reguły |
| 2 | wzór | Regex lub ciąg rozmyty do dopasowania do |
| 3 | próg | W przypadku reguł wyrażeń regularnych: ignorowane. W przypadku reguł rozmytych: minimalny wynik dopasowania (0–100) |
| 4 | opcje | Słownik opcjonalny (patrz „Informacje o opcjach” poniżej). Użyj `0` lub pomiń dla wartości domyślnych |
### Surowe zamienniki
Domyślnie (`False`) ciągi zastępcze są przetwarzane przez funkcję `re.sub()` w Pythonie, która obsługuje używanie odwołań zwrotnych do wyrażeń regularnych, takich jak `\1` lub `\2`, aby wstawić przechwycone grupy (na przykład: `(r'\1', r'(\d)\s+(?=\d)', 95)`.
Jeśli zamiana jest ciągiem wielowierszowym lub zawiera ukośniki odwrotne bez ucieczki (takie jak szablony kodu lub ścieżki) i powinna zostać zachowana dokładnie tak, jak jest, włącz opcję „raw_replacement”: True w słowniku opcji:
__KOD_BLOKU_1__

### Dostępne opcje konfigurowane przez użytkownika:

* **`flagi`** (liczba całkowita): Flagi wyrażeń regularnych używane podczas kompilacji wzorca.
*Przykład:* `{'flagi': re.IGNORECASE}`
* **`raw_replacement`** (boolean): Gdy `True`, tekst zastępczy jest traktowany jako czysty literał łańcuchowy i pomijany przez analizę składniową ukośnika odwrotnego `re.sub` w Pythonie. Ma kluczowe znaczenie w przypadku podpowiedzi wielowierszowych lub ciągów znaków z ukośnikami odwrotnymi bez ucieczki (`\`).
*Przykład:* `{'raw_replacement': True}`
* **`cache`** (boolean): Przełącza pamięć podręczną wyników AURA. Ustaw na „Fałsz” dla reguł generujących dynamiczne dane wyjściowe (np. bieżący czas, losowe dowcipy), aby mieć pewność, że są one oceniane na nowo w każdym meczu.
*Przykład:* `{'cache': Fałsz}`
* **`skip_list`** (lista ciągów znaków): Określa moduły potoku przetwarzania końcowego, które mają zostać pominięte, gdy pasuje ta reguła.
*Przykład:* `{'skip_list': ['LanguageTool']}` (pomija sprawdzanie gramatyki)
* **`only_in_windows`** (string/regex): Ogranicza regułę do uruchomienia tylko wtedy, gdy tytuł aktywnego okna pasuje do tego wzorca.
*Przykład:* `{'only_in_windows': 'google ai studio'}`
* **`exclude_windows`** (string/regex): Zapobiega uruchomieniu reguły, jeśli tytuł aktywnego okna pasuje do tego wzorca.
*Przykład:* `{'exclude_windows': 'Terminal'}`
* **`on_match_exec`** (lista obiektów Path/string): Ścieżki do skryptów/wtyczek, które powinny zostać wykonane, gdy ta reguła zostanie dopasowana (często używane przez reguły catch-all i fallback).
*Przykład:* `{'on_match_exec': [PROJECT_ROOT / 'scripts' / 'custom_action.py']}`

## Logika potoku
- Reguły są przetwarzane **z góry na dół**


## Logika potoku

- Reguły są przetwarzane **z góry na dół**
- **Wszystkie** reguły dopasowywania są stosowane (skumulowane)
- **fullmatch** (`^...$`) natychmiast zatrzymuje potok
- Wcześniejsze zasady mają pierwszeństwo przed późniejszymi zasadami

## Typowe wzorce

### Dopasuj pojedyncze słowo (granica słowa)
__KOD_BLOKU_2__

### Dopasuj wiele wariantów
__KOD_BLOKU_3__

### Fullmatch – zatrzymuje potok
__KOD_BLOKU_4__
⚠️ To pasuje do **wszystko**. Rurociąg zatrzymuje się w tym miejscu. Wcześniejsze zasady nadal mają pierwszeństwo.

### Dopasuj początek wejścia
__KOD_BLOKU_5__

### Dopasuj dokładną frazę
__KOD_BLOKU_6__

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

__KOD_BLOKU_7__

## Twoja pierwsza zasada — krok po kroku

1. Otwórz `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. Dodaj swoją regułę wewnątrz `FUZZY_MAP_pre = [...]`
3. Zapisz — Aura ładuje się automatycznie, nie ma potrzeby ponownego uruchamiania
4. Podyktuj frazę wyzwalającą i obserwuj, jak zadziała


## Zalecana struktura plików

Umieść swoje reguły **przed** długimi blokami komentarzy:
__KOD_BLOKU_8__

**Dlaczego?** Funkcja Auto-Fix firmy Aura skanuje tylko pierwszy ~1KB pliku.
Jeśli reguły pojawiają się po długim nagłówku, funkcja Auto-Fix nie może ich znaleźć ani naprawić.
Zalecany jest także komentarz do ścieżki w linii 1 — pomaga on szybko zidentyfikować plik.