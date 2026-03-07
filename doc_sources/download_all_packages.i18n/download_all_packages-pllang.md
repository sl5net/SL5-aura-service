## Narzędzia projektu: narzędzie do rozdzielania i pobierania plików

To repozytorium zawiera dwa potężne skrypty Pythona przeznaczone do zarządzania dystrybucją i pobieraniem dużych plików za pośrednictwem GitHub Releases.

1. **`split_and_hash.py`**: Narzędzie dla właścicieli repozytoriów umożliwiające dzielenie dużych plików na mniejsze części i generowanie kompletnego i weryfikowalnego manifestu sumy kontrolnej.
2. **`download_all_packages.py`**: Solidne narzędzie dla użytkowników końcowych umożliwiające automatyczne pobieranie, weryfikowanie i ponowne składanie tych wieloczęściowych plików, zapewniając integralność danych od początku do końca.

---

### 1. Skrypt podziału pliku i generowania sumy kontrolnej (`split_and_hash.py`)

Ten skrypt jest przeznaczony dla **opiekuna repozytorium**. Przygotowuje duże pliki do dystrybucji na platformach takich jak GitHub Releases, które mają indywidualne limity rozmiaru plików.

#### Zamiar

Podstawowym celem jest pobranie jednego dużego pliku (np. `vosk-model-de-0.21.zip`) i wykonanie dwóch kluczowych akcji:
1. Podziel plik na serię mniejszych, ponumerowanych części.
2. Wygeneruj pojedynczy, kompleksowy plik manifestu (`.sha256sums.txt`), który zawiera sumy kontrolne dla **zarówno oryginalnego, kompletnego pliku, jak i każdej pojedynczej części**.

Ten kompletny manifest jest kluczem do zapewnienia użytkownikowi końcowemu 100% integralności danych.

#### Kluczowe funkcje

* **Standardowe dzielenie:** Dzieli pliki na kawałki o wielkości 100MB (konfigurowalne w skrypcie).
* **Spójne nazewnictwo:** Tworzy części z przedrostkiem `Z_` (np. `Z_vosk-model-de-0.21.zip.part.aa`). Przedrostek `Z_` zapewnia prawidłowe sortowanie i obsługę w różnych systemach.
* **Pełny manifest integralności:** Wygenerowany plik `.sha256sums.txt` ma strukturę zapewniającą maksymalną niezawodność. Obejmuje:
* Hash SHA256 **oryginalnego, kompletnego pliku**.
* SHA256 **każdej części**, która została utworzona.

#### Użycie w przypadku wersji GitHub

1. Umieść duży plik (np. `vosk-model-de-0.21.zip`) w katalogu ze skryptem `split_and_hash.py`.
2. Uruchom skrypt na swoim terminalu:
__KOD_BLOKU_0__
3. Skrypt wygeneruje wszystkie pliki `Z_...part.xx` i odpowiadający im plik `...sha256sums.txt`.
4. Tworząc nową wersję GitHub, prześlij **wszystkie** wygenerowane pliki: pliki części i pojedynczy plik manifestu.
5. Powtórz ten proces dla każdego dużego pliku, który chcesz rozpowszechnić.

---

### 2. Automatyczne pobieranie i weryfikacja pakietów (`download_all_packages.py`)

Ten skrypt jest przeznaczony dla **użytkownika końcowego**. Zapewnia proste rozwiązanie wymagające jednego polecenia, umożliwiające niezawodne pobieranie i ponowne składanie wszystkich pakietów oferowanych w wersji GitHub.

#### Zamiar

Automatyzuje złożony i podatny na błędy proces pobierania dziesiątek części plików, weryfikowania każdej z nich i prawidłowego ich ponownego składania. Wykorzystuje manifesty sum kontrolnych dostarczone w wydaniu, aby zagwarantować, że ostateczny, złożony plik jest doskonałą, nieuszkodzoną kopią oryginału.

#### Kluczowe funkcje

* **Automatyczne wykrywanie:** Skrypt łączy się z interfejsem API GitHub, aby automatycznie znaleźć wszystkie dostępne „pakiety” w wydaniu, wyszukując pliki `.sha256sums.txt`. Nie jest wymagana ręczna konfiguracja nazw plików.
* **Proces oparty na integralności:** Dla każdego pakietu *najpierw* pobiera plik manifestu, aby uzyskać listę wymaganych części i ich poprawne sumy kontrolne.
* **Weryfikacja część po części:** pobiera jedną część na raz i natychmiast weryfikuje jej skrót SHA256.
* **Automatyczna ponowna próba w przypadku uszkodzenia:** Jeśli pobrana część jest uszkodzona (hash nie pasuje), skrypt automatycznie ją usuwa i pobiera ponownie, zapewniając czyste pobieranie.
* **Inteligentne ponowne składanie:** Po pobraniu i zweryfikowaniu wszystkich części pakietu następuje ich połączenie w odpowiedniej kolejności alfabetycznej (`.aa`, `.ab`, `.ac`...), aby zrekonstruować oryginalny duży plik.
* **Weryfikacja końcowa:** Po ponownym złożeniu oblicza skrót SHA256 ostatecznego, kompletnego pliku i weryfikuje go względem głównego skrótu znalezionego w manifeście. Zapewnia to kompleksowe potwierdzenie sukcesu.
* **Odporny i tolerancyjny:** skrypt jest odporny na drobne niespójności w nazewnictwie, takie jak `Z_` vs. `z_`, zapewniając płynną obsługę użytkownika.
* **Automatyczne czyszczenie:** Po pomyślnym zbudowaniu i zweryfikowaniu pakietu skrypt usuwa pobrane pliki części, aby zaoszczędzić miejsce na dysku.

#### Warunki wstępne

Użytkownik musi mieć zainstalowany Python oraz biblioteki `requests` i `tqdm`. Można je zainstalować za pomocą pip:
__KOD_BLOKU_1__

#### Użycie

1. Pobierz skrypt `download_all_packages.py`.
2. Uruchom go z terminala bez argumentów:
__KOD_BLOKU_2__
3. Skrypt zajmie się resztą, wyświetlając paski postępu i komunikaty o statusie. Po zakończeniu użytkownik będzie miał wszystkie ostateczne, zweryfikowane pliki ZIP gotowe do użycia w tym samym katalogu.