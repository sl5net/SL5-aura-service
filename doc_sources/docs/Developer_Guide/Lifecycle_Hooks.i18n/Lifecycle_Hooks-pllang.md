Haki Aura SL5: Dodano

HOOK_PLUGIN_LOAD = 'on_plugin_load'
HOOK_FILE_LOAD = 'przy ładowaniu_pliku'
HOOK_RELOAD = 'przy_przeładowaniu'
HOOK_UPSTREAM = 'na_zmianę_folderu'

on_folder_change() i
on_reload() do wyzwalania logiki po ponownym załadowaniu na gorąco. Użyj tego, aby wykonać łańcuchowo wykonywanie skryptów nadrzędnych, takich jak secure_packer.py w przypadku złożonych pakietów.

# Przewodnik programisty: Haki cyklu życia wtyczek

Aura SL5 umożliwia wtyczkom (Mapom) zdefiniowanie konkretnych „Hooków”, które są wykonywane automatycznie w przypadku zmiany stanu modułu. Jest to niezbędne w przypadku zaawansowanych przepływów pracy, takich jak system **Bezpieczna mapa prywatna**.

## Hak `on_folder_change` Hak

Zaimplementowano wykrywanie haków `on_folder_change`. Program reloader skanuje teraz katalog

## Hak `on_reload()`

Funkcja `on_reload()` jest funkcją opcjonalną, którą możesz zdefiniować w dowolnym module Map.

### Zachowanie
* **Wyzwalacz:** Wykonywany natychmiast po pomyślnym **przeładowaniu modułu na gorąco** (modyfikacja pliku + wyzwalanie głosowe).
* **Kontekst:** Działa w głównym wątku aplikacji.
* **Bezpieczeństwo:** Zapakowane w blok „try/except”. Błędy tutaj zostaną zarejestrowane, ale **nie spowodują awarii** aplikacji.

### Schemat użycia: „łańcuch szeregowy”
W przypadku złożonych pakietów (takich jak Private Maps) często masz wiele plików podrzędnych, ale tylko jeden centralny skrypt (`secure_packer.py`) powinien obsługiwać logikę.

Za pomocą haka możesz delegować zadanie w górę:

__KOD_BLOKU_0__