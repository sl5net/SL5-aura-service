# PRZEGLĄD FUNKCJI: Bezpieczne ładowanie prywatnych map i automatyczne pakowanie

W tym dokumencie opisano architekturę zarządzania wrażliwymi wtyczkami map (np. danymi klienta, zastrzeżonymi poleceniami) w sposób umożliwiający **edycję na żywo** przy jednoczesnym egzekwowaniu **najlepszych praktyk w zakresie bezpieczeństwa**, aby zapobiec przypadkowemu narażeniu Git.

---

## 1. Koncepcja: Bezpieczeństwo „Matryoszki”.

Aby zapewnić maksymalną prywatność podczas korzystania ze standardowych narzędzi, Aura stosuje strategię zagnieżdżania **Matryoshka (Russian Doll)** dla zaszyfrowanych archiwów.

1. **Warstwa zewnętrzna:** Standardowy plik ZIP zaszyfrowany **AES-256** (poprzez systemowe polecenie `zip`).
* *Wygląd:* Zawiera tylko **jeden** plik o nazwie `aura_secure.blob`.
* *Zaleta:* Ukrywa nazwy plików i strukturę katalogów przed wzrokiem ciekawskich.
2. **Warstwa wewnętrzna (Blob):** Nieszyfrowany kontener ZIP wewnątrz obiektu typu blob.
* *Treść:* Rzeczywista struktura katalogów i pliki Pythona.
3. **Stan pracy:** Po odblokowaniu pliki są rozpakowywane do folderu tymczasowego poprzedzonego podkreśleniem (np. „_prywatny”).
* *Bezpieczeństwo:* Ten folder jest ściśle ignorowany przez `.gitignore`.

---

## 2. Techniczny przepływ pracy

### A. Brama bezpieczeństwa (rozruch)
Przed rozpakowaniem czegokolwiek Aura sprawdza `scripts/py/func/map_reloader.py` pod kątem konkretnych reguł `.gitignore`.
* **Zasada 1:** `config/maps/**/.*` (Chroni kluczowe pliki)
* **Zasada 2:** `config/maps/**/_*` (Chroni katalogi robocze)
Jeśli ich brakuje, system **przerywa**.

### B. Rozpakowywanie (w oparciu o wyjątek)
1. Użytkownik tworzy plik klucza (np. `.auth_key.py`) zawierający hasło (w postaci zwykłego tekstu lub komentarzy).
2. Aura wykrywa ten plik i odpowiadający mu plik ZIP (np. `private.zip`).
3. Aura odszyfrowuje zewnętrzny ZIP za pomocą klucza.
4. Aura wykrywa plik `aura_secure.blob`, wyodrębnia warstwę wewnętrzną i przenosi pliki do katalogu roboczego `_private`.

### C. Edycja na żywo i automatyczne pakowanie (cykl)
W tym miejscu system staje się „samoleczący”:

1. **Edycja:** Modyfikujesz plik w `_private/` i zapisujesz go.
2. **Wyzwalacz:** Aura wykrywa zmianę i ponownie ładuje moduł.
3. **Lifecycle Hook:** Moduł uruchamia funkcję `on_reload()`.
4. **SecurePacker:** Skrypt (`secure_packer.py`) w katalogu głównym folderu prywatnego wykonuje:
* Tworzy wewnętrzny ZIP (strukturę).
* Zmienia nazwę na `.blob`.
* Wywołuje systemowe polecenie `zip` w celu zaszyfrowania go w zewnętrznym archiwum przy użyciu hasła z pliku `.key`.

**Wynik:** Twój plik `private.zip` jest zawsze aktualny i zawiera najnowsze zmiany, ale Git widzi tylko zmiany w binarnym pliku ZIP.

---

## 3. Przewodnik konfiguracji

### Krok 1: Struktura katalogów
Utwórz strukturę folderów taką jak ta:
__KOD_BLOKU_0__

### Krok 2: Plik klucza (`.auth_key.py`)
Należy zacząć od kropki.
__KOD_BLOKU_1__

### Krok 3: Skrypt pakujący (`secure_packer.py`)
Umieść ten skrypt w swoim prywatnym folderze mapy (przed początkowym spakowaniem). Obsługuje logikę szyfrowania. upewnij się, że Twoje mapy wywołują ten skrypt poprzez hak `on_reload`.

### Krok 4: Implementacja haka
W plikach map (`.py`) dodaj ten hak, aby uruchamiać tworzenie kopii zapasowej przy każdym zapisie:

__KOD_BLOKU_2__

---

## 4. Status i bezpieczeństwo Git

Po prawidłowym skonfigurowaniu, `git status` będzie **tylko** pokazywać:
__KOD_BLOKU_3__
Folder `_private_maps` i plik `.auth_key.py` nigdy nie są śledzone.
__KOD_BLOKU_4__
# Przewodnik programisty: Haki cyklu życia wtyczek

Aura SL5 umożliwia wtyczkom (Mapom) zdefiniowanie konkretnych „Hooków”, które są wykonywane automatycznie w przypadku zmiany stanu modułu. Jest to niezbędne w przypadku zaawansowanych przepływów pracy, takich jak system **Bezpieczna mapa prywatna**.

## Hak `on_reload()`

Funkcja `on_reload()` jest funkcją opcjonalną, którą możesz zdefiniować w dowolnym module Map.

### Zachowanie
* **Wyzwalacz:** Wykonywany natychmiast po pomyślnym **przeładowaniu modułu na gorąco** (modyfikacja pliku + wyzwalanie głosowe).
* **Kontekst:** Działa w głównym wątku aplikacji.
* **Bezpieczeństwo:** Zapakowane w blok „try/except”. Błędy tutaj zostaną zarejestrowane, ale **nie spowodują awarii** aplikacji.

### Schemat użycia: „łańcuch szeregowy”
W przypadku złożonych pakietów (takich jak Private Maps) często masz wiele plików podrzędnych, ale tylko jeden centralny skrypt (`secure_packer.py`) powinien obsługiwać logikę.

Za pomocą haka możesz delegować zadanie w górę:

__KOD_BLOKU_5__

### Najlepsze praktyki
1. **Trzymaj się szybko:** Nie uruchamiaj długich zadań blokujących (takich jak duże pobieranie plików) na głównym haku. Jeśli to konieczne, użyj nici.
2. **Idempotencja:** Upewnij się, że hak może działać wiele razy, nie psując niczego (np. nie dołączaj do pliku w nieskończoność, zamiast tego przepisz go).