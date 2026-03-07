## Ekstraktor artykułów Kiwix offline (Python/Docker/kiwix-serve)

Ten dokument zawiera przewodnik krok po kroku dotyczący konfigurowania i używania skryptu w języku Python, który wyodrębnia pełny, czysty tekst artykułu z Wikipedii z pliku ZIM offline przy użyciu serwera WWW `kiwix-serve` działającego w kontenerze Docker.

### Warunki wstępne

Musisz mieć zainstalowane następujące oprogramowanie w swoim systemie Manjaro:

1. **Docker:** Aby uruchomić oficjalny serwer `kiwix-tools` bez problemów z kompilacją.
2. **Python 3:** Ze środowiskiem wirtualnym (`venv`).
3. **Plik ZIM:** Baza danych Wikipedii offline (np. `wikipedia_de_all_mini_2025-09.zim`).

### 1. Konfiguracja systemu (Docker)

Upewnij się, że usługa Docker jest zainstalowana i uruchomiona.

__KOD_BLOKU_0__

### 2. Konfiguracja środowiska Python

Skonfiguruj wirtualne środowisko Python i zainstaluj niezbędne biblioteki.

__KOD_BLOKU_1__

### 3. Uruchamianie serwera Kiwix (zależność rdzenia)

Skrypt opiera się na `kiwix-serve` działającym na porcie `8080`. To polecenie używa oficjalnego, stabilnego obrazu Dockera i wiąże bieżący katalog (zawierający plik ZIM) z kontenerem.

**WAŻNE:** Przed uruchomieniem tego polecenia umieść plik ZIM (np. `wikipedia_de_all_mini_2025-09.zim`) w katalogu `kiwix_cli`.

__KOD_BLOKU_2__
Serwer działa teraz na `http://localhost:8080`.

### 4. Skrypt wyodrębniania artykułów

Utwórz plik o nazwie `article_extractor.py` i wklej do niego następujący końcowy, działający kod.

__KOD_BLOKU_3__

### 5. Aplikacja i czyszczenie

1. **Uruchom skrypt:**
__KOD_BLOKU_4__

2. **Zatrzymaj serwer Docker (po zakończeniu):**
Musisz zatrzymać kontener Docker, w przeciwnym razie będzie on nadal korzystał z portu 8080.
__KOD_BLOKU_5__
XSPACEbreakX
XSPACEbreakX