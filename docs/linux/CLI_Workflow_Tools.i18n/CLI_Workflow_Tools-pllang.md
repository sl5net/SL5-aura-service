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

### 2. Linux (Debian / Ubuntu / Mint)
W systemach opartych na Debianie użyj `apt`:

__KOD_BLOKU_1__

### 3. macOS
Użyj menedżera pakietów [Homebrew](https://brew.sh/), aby zainstalować brakujące narzędzia:

__KOD_BLOKU_2__

### 4. Okna
Jeśli używasz systemu Windows, zalecamy instalację `fzf` poprzez [Scoop](https://scoop.sh/) lub [Winget](https://github.com/microsoft/winget-cli):

__KOD_BLOKU_3__
__KOD_BLOKU_4__