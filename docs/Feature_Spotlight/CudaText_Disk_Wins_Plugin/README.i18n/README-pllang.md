# Wtyczka CudaText: „Dysk wygrywa” (Wymuś automatyczne przeładowanie przy zmianie zewnętrznej)

CudaText nie ma wbudowanej opcji, która dyskretnie przeładowuje plik w momencie jego pojawienia się
zmiany na dysku — każdy wbudowany tryb „zmienione na dysku” nadal je wyświetla
rodzaj monitu (modalny lub bezmodalny) przed ponownym załadowaniem
(patrz `ui_notif_confirm` w `default.json`, wartości `0`-`4`, z których wszystkie
zapytać). Ta wtyczka wypełnia tę lukę: **dysk zawsze wygrywa**, nigdy bez monitu.

Zarchiwizowane tutaj, aby nikt nie musiał w tym celu ponownie tworzyć interfejsu API wtyczki CudaText
Ponownie. Źródło prawdy o samej wtyczce żyje
[`cuda_disk_wins/`](.././cuda_disk_wins/) w tym folderze.

## Co to robi

- Odpytuje każdy otwarty plik o określonej nazwie raz na sekundę (konfigurowalne za pomocą
`TIMER_INTERVAL` w `__init__.py`).
- Jeśli zmienił się czas mtime pliku na dysku, wtyczka ponownie go odczytuje i wywołuje
`Editor.set_text_all()` — **nadpisywanie wszelkich niezapisanych zmian w pliku
zakładkę edytora bez pytania**.
- Następnie usuwa flagę „zmodyfikowaną” („PROP_MODIFIED = False”), więc plik
zakładka wygląda czysto, jakby nic się nigdy nie rozdzieliło.
- Best-effort przywraca pozycję karetki i górną widoczną linię po
przeładować.
- Dodaje dwa polecenia w `Wtyczki → Zwycięstwa dysku`:
- `Włącz/wyłącz automatyczne przeładowanie`
- `Sprawdź teraz` (ręczne sprawdzenie jednorazowe)

## Dlaczego wtyczka zamiast ustawienia

Własny obserwator plików CudaText (`ui_notif`) oferuje zawsze tylko zachowania „zapytaj”:

| `ui_notif_confirm` | Zachowanie |
|----------------------------------|------------------------------------------------------------------|
| 0 | monit bezmodalny, zawsze |
| 1 | monit bezmodalny, jeśli edytor został zmodyfikowany lub Cofnij nie jest pusty |
| 2 | monit bezmodalny, jeśli edytor został zmodyfikowany |
| 3 | monit modalny, zawsze |
| 4 | monit modalny, jeśli edytor został zmodyfikowany |

Nie ma wartości oznaczającej „przeładuj automatycznie, bez monitu, kontynuuj”.
Stąd ta mała wtyczka, która uruchamia własną pętlę odpytywania i ładuje ponownie
bezpośrednio poprzez API Pythona.

## Instalacja

__KOD_BLOKU_0__

Uruchom ponownie CudaText.

**Ważne:** wyłącz także własne okno dialogowe powiadamiania o zmianach CudaText, więc
nie walczy z wtyczką. W
`~/.config/cudatext/settings/user.json`:

__KOD_BLOKU_1__

(Odpowiada `Opcjom → Ustawienia – konfiguracja użytkownika` w interfejsie użytkownika.) Uruchom ponownie
CudaText ponownie po tej zmianie.

## Zastrzeżenia

- Jest to celowo destrukcyjne: niezapisane zmiany edytora są odrzucane
dyskretnie w momencie, gdy plik zmieni się zewnętrznie. To wszystko
punktu wtyczki — nie instaluj jej, jeśli czasami chcesz ją zachować
zmiany lokalne zamiast zmian zewnętrznych.
- Reaguje tylko na zmiany w mtime pliku; wpisując w samym edytorze
nie powoduje przeładowania (brak pętli sprzężenia zwrotnego).
- Jeśli plik zostanie usunięty zewnętrznie, wtyczka nie zrobi nic, dopóki to nie nastąpi

- Kodowanie jest odczytywane poprzez `PROP_ENC` i mapowane do najbliższego kodeka Pythona;
rozszerz `ENC_MAP` w `__init__.py`, jeśli używasz jeszcze kodowania
katalogowany.

## Pochodzenie

Zbudowany z myślą o „zawsze preferuj zmiany systemu plików zamiast niezapisanego edytora
bufory, brak potwierdzenia” wymaganie omówione podczas konfigurowania CudaText
przez `yay -S cudatext-qt6-bin python` na Arch.