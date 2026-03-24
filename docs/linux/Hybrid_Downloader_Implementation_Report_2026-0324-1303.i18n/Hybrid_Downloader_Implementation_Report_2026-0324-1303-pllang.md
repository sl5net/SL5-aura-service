# Raport z wdrożenia Hybrid Downloadera 24.3.'26 13:04 Wt

## 1. Podsumowanie stanu projektu
Nowy skrypt `download_release_hybrid.py` został pomyślnie zaimplementowany i zintegrowany. Replikuje podstawową logikę oryginalnego pliku `download_all_packages.py`, dodając jednocześnie warstwę hybrydową BitTorrent.

### Zweryfikowano podstawowe funkcje:
* **Przetwarzanie argumentów CLI:** Pomyślnie obsługuje `--exclude`, `--tag` i `--list`.
* **Wykrywanie środowiska CI:** poprawnie identyfikuje akcje GitHub i automatycznie wyklucza duże modele.
* **Wykrywanie zasobów:** Pomyślnie grupuje udostępnione zasoby w logiczne pakiety (części, sumy kontrolne, torrenty).
* **Niezawodny tryb awaryjny:** Skrypt wykrywa brak `libtorrent` i płynnie przechodzi w tryb awaryjny HTTP.

---

## 2. Wykonanie i wyniki testu
**Polecenie wykonane:**
`python Tools/download_release_hybrid.py --list`

### Zaobserwowane dane wyjściowe:
* **Sprawdzanie zależności:** `--> Informacje: nie znaleziono „libtorrent”. Torrent hybrydowy wyłączony. Korzystanie z zastępczego protokołu HTTP.` (Oczekiwane w bieżącym systemie).
* **Łączność API:** Pomyślnie pobrano informacje o wersji dla `sl5net/SL5-aura-service @ v0.2.0`.
* **Wynik odkrycia:** Zidentyfikowano 5 pakietów:
1. `LanguageTool-6.6.zip` (3 części)
2. `lid.176.zip` (2 części)
3. `vosk-model-de-0.21.zip` (20 części)
4. `vosk-model-en-us-0.22.zip` (19 części)
5. `vosk-model-small-en-us-0.15.zip` (1 część)

---

## 3. Raport o błędach: problemy z zależnościami
### Problem: Błąd instalacji `libtorrent`
W obecnym środowisku **Manjaro/Arch Linux** silnik BitTorrent („libtorrent”) nie mógł zostać zainstalowany za pomocą standardowych menedżerów pakietów.

* **Próby poleceń:**
* `sudo pacman -S python-libtorrent` -> `nie znaleziono celu`
* `pamac build python-libtorrent-rasterbar` -> `nie znaleziono celu`
* `pamac build python-libtorrent` -> `nie znaleziono celu`
* **Główna przyczyna:** Powiązania Pythona dla `libtorrent` w systemach opartych na Arch są często słabo utrzymywane w oficjalnych repozytoriach lub wymagają określonych pomocników/narzędzi do budowania AUR (`base-devel`), których obecnie brakuje lub są źle skonfigurowane.
* **Skutek:** Funkcje BitTorrent (P2P i Web-Seeds) są obecnie nieaktywne. Skrypt pozostaje w pełni funkcjonalny dzięki **zastępczemu protokołowi HTTP**.

---

## 4. Lista rzeczy do zrobienia (kolejne kroki)

### Faza 1: Migracja środowiska
- [ ] **Przełącznik systemu operacyjnego:** Przenieś testowanie do innego systemu operacyjnego (np. Ubuntu, Debian lub Windows), gdzie `python3-libtorrent` lub `pip install libtorrent` jest łatwiej dostępny.
- [ ] **Ponowna weryfikacja zależności:** Upewnij się, że „Motor” (`libtorrent`) ładuje się poprawnie w nowym systemie operacyjnym.

### Faza 2: Walidacja funkcjonalna
- [ ] **Pełny test pobierania:** Uruchom skrypt bez flagi `--list`, aby zweryfikować częściowe pobieranie, łączenie i weryfikację SHA256.
- [ ] **Test wykluczeń:** Uruchom z `--exclude de`, aby potwierdzić, że konfiguracja wyłącznie w języku angielskim działa zgodnie z oczekiwaniami.
- [ ] **Test torrenta:** Utwórz plik `.torrent` za pomocą narzędzia GitHub Web-Seed i sprawdź, czy hybrydowy moduł pobierania nadaje priorytet P2P/Web-Seed w stosunku do standardowych części HTTP.

### Faza 3: Oczyszczanie
- [ ] **Ostateczna kontrola czyszczenia:** Upewnij się, że po pełnym uruchomieniu w końcowej strukturze katalogów lokalnych nie ma plików `.i18n` ani plików tłumaczeń.