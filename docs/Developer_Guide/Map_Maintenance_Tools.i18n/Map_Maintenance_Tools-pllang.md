# Narzędzia do konserwacji mapy Regex

Aby wesprzeć funkcję szybkiego wyszukiwania (polecenie `s` / `search_rules.sh`), używamy skryptu pomocniczego, który automatycznie opisuje wzorce wyrażeń regularnych za pomocą przykładów zrozumiałych dla człowieka.

## Dlaczego tego potrzebujemy?
Nasze pliki `FUZZY_MAP.py` zawierają złożone wyrażenia regularne. Aby umożliwić ich przeszukiwanie za pomocą wyszukiwarki rozmytej (fzf) bez konieczności rozumienia surowego wyrażenia regularnego, dodajemy komentarz `# PRZYKŁAD:` nad wzorcami.

**Zanim:**
__KOD_BLOKU_0__

**Po (wygenerowane automatycznie):**
__KOD_BLOKU_1__

## Skrypt Taggera (`map_tagger.py`)

Udostępniamy skrypt w języku Python, który skanuje wszystkie pliki `FUZZY_MAP.py` i `FUZZY_MAP_pre.py` i automatycznie generuje te przykłady.

### Instalacja
Skrypt wymaga biblioteki `exrex` do generowania losowych dopasowań dla złożonych wyrażeń regularnych.

__KOD_BLOKU_2__

### Użycie
Uruchom skrypt z katalogu głównego projektu:

__KOD_BLOKU_3__

### Przepływ pracy
1. **Utwórz lub edytuj** plik mapy (np. dodając nowe reguły).
2. **Uruchom** skrypt tagujący.
3. **Tryb interaktywny:**
- Skrypt wyświetli wygenerowaną sugestię.
- Naciśnij `ENTER`, aby zaakceptować.
- Wpisz `s`, aby pominąć.
- Wpisz `sa` (pomiń wszystko), jeśli chcesz pominąć wszystkie pozostałe wzorce, których wygenerowanie nie powiodło się.
4. **Zatwierdź** zmiany.

> **Uwaga:** Skrypt ignoruje istniejące znaczniki `# PRZYKŁAD:`, więc można go bezpiecznie uruchamiać wielokrotnie.