# Przewodnik instalacji narzędzi przepływu pracy CLI

Niektóre działania wtyczki nawigatora ścieżek opierają się na zewnętrznych narzędziach wiersza poleceń, które umożliwiają wyszukiwanie rozmyte, wyświetlanie listy plików i manipulowanie schowkiem. Jeśli brakuje tych narzędzi, w konsoli systemowej pojawi się ostrzeżenie.

Poniżej znajdują się instrukcje instalacji dla każdego obsługiwanego systemu operacyjnego.

## Wymagane narzędzia

* **`fzf`**: Uniwersalna wyszukiwarka rozmyta z wiersza poleceń.
* **`find`** (lub `fd`): standardowe narzędzie do wyszukiwania plików.
* **Narzędzie schowka**: Używane do przesyłania danych wyjściowych bezpośrednio do schowka systemowego.
* **Linux:** `xclip` (wymaga środowiska X11).
* **macOS:** `pbcopy` (preinstalowany).
* **Windows:** `clip` (preinstalowany).
* **`file`**: Określa typy plików dla pełnych podglądów terminala.

---

## Instrukcje instalacji

### 1. Linux (Arch/Manjaro)
Ponieważ twój system działa na Manjaro, możesz zainstalować wymagane pakiety za pomocą `pacman`:

__KOD_BLOKU_0__



## 1. Szybki wybór pliku (polecenie Aura)

Akcja `path_navigator` wykorzystuje następujące polecenie `fzf` obsługujące Git. Jego celem jest wyprowadzenie ścieżki pliku bezpośrednio do schowka systemowego.

**Logika poleceń:**
- Używa `git ls-files` w repozytorium Git (z wyłączeniem ignorowanych plików).
- Wraca do „znajdź”. -type f` poza repozytorium Git.
- Wyprowadza wybraną ścieżkę do schowka przy użyciu `xclip -selection schowek`.

## 2. Szybkie wykonanie pliku (funkcja „k”)

Aby zakończyć pętlę, używana jest niestandardowa funkcja powłoki „k”. Ta funkcja pobiera ścieżkę ze schowka i natychmiast otwiera plik w `kate`.

### Implementacja

Dodaj następującą funkcję do pliku konfiguracyjnego powłoki (np. `~/.bashrc`, `~/.zshrc`):

__KOD_BLOKU_1__

### Użycie

1. Użyj polecenia `path_navigator` (np. wpisz `search file` w narzędziu uruchamiającym).
2. Znajdź i wybierz żądany plik (np. `src/main/config.py`).
3. W terminalu wpisz `k` i naciśnij **ENTER**.
4. Plik otwiera się natychmiast w Kate.
__KOD_BLOKU_2__