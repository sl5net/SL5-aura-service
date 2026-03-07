# Przewodnik programisty: generowanie wykresu zgłoszenia serwisowego

W tym dokumencie opisano solidną, bezpieczną dla wątków metodę generowania wizualnego wykresu wywołań długotrwałego pliku `aura_engine.py`. Używamy profilera `yappi` (do obsługi wielowątkowości) i `gprof2dot` do wizualizacji.

### Warunki wstępne

Upewnij się, że masz zainstalowane niezbędne narzędzia globalnie lub w środowisku wirtualnym:

__KOD_BLOKU_0__

### Krok 1: Modyfikacja usługi w celu profilowania

Skrypt `aura_engine.py` musi zostać zmodyfikowany, aby ręcznie uruchomić profiler `yappi` i bezpiecznie zapisać dane profilowania w przypadku przerwania (`Ctrl+C`).

**Kluczowe zmiany w `aura_engine.py`:**

1. **Import i obsługa sygnałów:** Zaimportuj `yappi` i zdefiniuj funkcję `generate_graph_on_interrupt` (jak zaimplementowano wcześniej), aby wywołać `yappi.stop()` i `stats.save(...)`.
2. **Start/Stop:** Dodaj `yappi.start()` i `signal.signal(signal.SIGINT, ...)` w bloku `if __name__ == "__main__":`, aby zawinąć wykonanie `main(...)`.

### Krok 2: Uruchomienie usługi i zebranie danych

Uruchom zmodyfikowany skrypt bezpośrednio i pozwól mu przetwarzać dane przez wystarczający czas (np. 10-20 sekund), aby upewnić się, że wszystkie podstawowe funkcje, w tym funkcje wątkowe (takie jak korekcja LanguageTool), zostaną wywołane.

__KOD_BLOKU_1__

Naciśnij raz **Ctrl+C**, aby uruchomić procedurę obsługi sygnału. Spowoduje to zatrzymanie profilera i zapisanie surowych danych w:

`\mathbf{yappi\_profile\_data.prof`

### Krok 3: Generowanie i filtrowanie wykresu wizualnego

Używamy `gprof2dot` do konwersji surowych danych `pstats` na format SVG. Ponieważ zaawansowane opcje filtrowania, takie jak `--include' i `--threshold' mogą nie być obsługiwane w naszym konkretnym środowisku, używamy podstawowego filtra **`--strip`** w celu oczyszczenia informacji o ścieżce i zmniejszenia bałaganu z wewnętrznych elementów systemu.

**Wykonaj polecenie wizualizacji:**

__KOD_BLOKU_2__

### Krok 4: Dokumentacja (kadrowanie ręczne)

Wynikowy plik `yappi_call_graph_stripped.svg` (lub `.png`) będzie duży, ale dokładnie będzie zawierał pełny przebieg wykonania, łącznie ze wszystkimi wątkami.

W celach dokumentacyjnych **ręcznie przytnij obraz**, aby skupić się na centralnej logice (10–20 głównych węzłów i ich połączeniach), aby utworzyć ukierunkowany i czytelny wykres wywołań dla dokumentacji repozytorium.

### Archiwizacja

Zmodyfikowany plik konfiguracyjny oraz ostateczną wizualizację Call Graph należy zarchiwizować w katalogu źródłowym dokumentacji:

| Artefakt | Lokalizacja |
| :--- | :--- |
| **Zmodyfikowany plik usługi** | `doc_sources/profiling/aura_engine_profiling_base.py` |
| **Ostatecznie przycięty obraz** | `doc_sources/profiling/core_logic_call_graph.svg` |
| **Surowe dane profilowe** | *(Opcjonalnie: Należy wyłączyć z ostatecznej dokumentacji repozytorium)* |


![yappi_call_graph](../yappi_call_graph_stripped.svg_20251024_010459.png "yappi_call_graph_stripped.svg_20251024_010459.png")