# Zaawansowane akcje reguł: Wykonywanie skryptów Pythona

W tym dokumencie opisano, jak rozszerzyć funkcjonalność prostych reguł zamiany tekstu, wykonując niestandardowe skrypty w języku Python. Ta zaawansowana funkcja umożliwia tworzenie dynamicznych odpowiedzi, interakcję z plikami, wywoływanie zewnętrznych interfejsów API i wdrażanie złożonej logiki bezpośrednio w przepływie pracy rozpoznawania mowy.

## Podstawowa koncepcja: `on_match_exec`

Zamiast po prostu zastępować tekst, możesz teraz nakazać regule wykonanie jednego lub większej liczby skryptów Pythona, gdy pasuje do wzorca. Odbywa się to poprzez dodanie klucza `on_match_exec` do słownika opcji reguły.

Podstawowym zadaniem skryptu jest otrzymanie informacji o dopasowaniu, wykonanie akcji i zwrócenie końcowego ciągu znaków, który zostanie użyty jako nowy tekst.

### Struktura reguł

Reguła z akcją skryptową wygląda następująco:

__KOD_BLOKU_0__
**Kluczowe punkty:**
- Wartość `on_match_exec` musi być **listą**.
- Skrypty znajdują się w tym samym katalogu, co plik mapy, dlatego też `CONFIG_DIR / 'nazwa_skryptu.py'' jest zalecanym sposobem zdefiniowania ścieżki.

---

## Tworzenie skryptu wykonywalnego

Aby system mógł skorzystać z Twojego skryptu, musi przestrzegać dwóch prostych zasad:
1. Musi to być prawidłowy plik Pythona (np. `my_script.py`).
2. Musi zawierać funkcję o nazwie `execute(match_data)`.

### Funkcja `execute(match_data)`

Jest to standardowy punkt wejścia dla wszystkich wykonywalnych skryptów. System automatycznie wywoła tę funkcję, gdy reguła będzie pasować.

- **`match_data` (dict):** Słownik zawierający cały kontekst dotyczący meczu.
- **Wartość zwracana (str):** Funkcja **musi** zwracać ciąg znaków. Ten ciąg stanie się nowym przetworzonym tekstem.

### Słownik „match_data”.

Słownik ten stanowi pomost pomiędzy aplikacją główną a skryptem. Zawiera następujące klucze:

* `'oryginalny_tekst'` (str): Pełny ciąg tekstowy *przed* zastosowaniem jakiejkolwiek zamiany z bieżącej reguły.
* `'text_after_replacement'` (str): Tekst *po* zastosowaniu podstawowego ciągu zastępującego reguły, ale *przed* wywołaniem skryptu. (Jeśli zamianą jest „Brak”, będzie ona taka sama jak „oryginalny_tekst”).
* `'regex_match_obj'` (re.Match): Oficjalny obiekt dopasowania wyrażenia regularnego w języku Python. Jest to niezwykle przydatne przy uzyskiwaniu dostępu do **grup przechwytywania**. Możesz użyć `match_obj.group(1)`, `match_obj.group(2)` itp.
* `'rule_options'` (dykt): Kompletny słownik opcji dla reguły, która uruchomiła skrypt.

---

## Przykłady

### Przykład 1: pobieranie aktualnego czasu (reakcja dynamiczna)

Ten skrypt zwraca spersonalizowane powitanie na podstawie pory dnia.

**1. Zasada (w pliku mapy):**
__KOD_BLOKU_1__

**2. Skrypt (`get_current_time.py`):**
__KOD_BLOKU_2__
**Stosowanie:**
> **Wejście:** „która jest godzina”
> **Wyjście:** „Dzień dobry! Obecnie jest 14:30”.

### Przykład 2: Prosty kalkulator (przy użyciu grup przechwytywania)

Ten skrypt używa grup przechwytywania z wyrażenia regularnego do wykonania obliczeń.

**1. Zasada (w pliku mapy):**
__KOD_BLOKU_3__

**2. Skrypt (`calculator.py`):**
__KOD_BLOKU_4__
**Stosowanie:**
> **Wejście:** „oblicz 55 plus 10”
> **Wyjście:** „Wynik to 65.”

### Przykład 3: Stała lista zakupów (we/wy pliku)

Ten przykład pokazuje, jak jeden skrypt może obsłużyć wiele poleceń (dodawanie, wyświetlanie) poprzez sprawdzanie oryginalnego tekstu użytkownika i jak może utrwalać dane poprzez zapisywanie do pliku.

**1. Zasady (w pliku mapy):**
__KOD_BLOKU_5__

**2. Skrypt (`shopping_list.py`):**
__KOD_BLOKU_6__
**Stosowanie:**
> **Wejście 1:** „dodaj mleko do listy zakupów”
> **Wyjście 1:** „OK, dodałem „mleko” do listy zakupów.”
>
> **Wejście 2:** „pokaż listę zakupów”
> **Wyjście 2:** „Na liście masz: mleko”.

---

## Najlepsze praktyki

- **Jedno zadanie na skrypt:** Koncentruj skrypty na jednym zadaniu (np. `calculator.py` tylko oblicza).
- **Obsługa błędów:** Zawsze otaczaj logikę skryptu blokiem „try...except”, aby zapobiec awarii całej aplikacji. Zwróć przyjazny dla użytkownika komunikat o błędzie z bloku „z wyjątkiem”.
- **Biblioteki zewnętrzne:** Możesz używać bibliotek zewnętrznych (takich jak `requests` lub `wikipedia-api`), ale musisz upewnić się, że są one zainstalowane w Twoim środowisku Pythona (`pip install <nazwa-biblioteki>`).
- **Bezpieczeństwo:** Należy pamiętać, że ta funkcja może wykonać dowolny kod Pythona. Używaj wyłącznie skryptów z zaufanych źródeł.