## Omówienie funkcji: wdrażanie przełączalnego trybu tłumaczenia na żywo

Nasza wtykowa struktura asystentów głosowych została zaprojektowana z myślą o maksymalnej elastyczności. W tym przewodniku przedstawiono potężną funkcję: tryb tłumaczenia na żywo, który można włączać i wyłączać za pomocą prostego polecenia głosowego. Wyobraź sobie, że rozmawiasz ze swoim asystentem po niemiecku i słyszysz komunikat po portugalsku, a następnie natychmiast wracasz do normalnego zachowania.

Osiąga się to nie poprzez zmianę podstawowego silnika, ale poprzez sprytną manipulację samym plikiem konfiguracyjnym reguł.

### Jak z niego korzystać

Konfiguracja tego polega na dodaniu dwóch reguł do pliku `FUZZY_MAP_pre.py` i utworzeniu odpowiednich skryptów.

**1. Reguła przełączania:** Ta reguła nasłuchuje polecenia włączenia lub wyłączenia trybu tłumaczenia.

__KOD_BLOKU_0__
Kiedy powiesz „Übersetzung einschalten” (włącz tłumaczenie), zostanie wykonany skrypt `toggle_translation_mode.py`.

**2. Reguła tłumaczenia:** Jest to reguła typu „catch-all”, która, gdy jest aktywna, dopasowuje dowolny tekst i wysyła go do skryptu tłumaczącego.

__KOD_BLOKU_1__
Kluczem jest tutaj komentarz `# TRANSLATION_RULE`. Działa to jak „kotwica”, której skrypt przełączający używa do znajdowania i modyfikowania reguły znajdującej się poniżej.

### Jak to działa: magia za kurtyną

Zamiast używać stanu wewnętrznego, ta metoda bezpośrednio edytuje mapę reguł w systemie plików. Skrypt `toggle_translation_mode.py` pełni rolę menedżera konfiguracji.

1. **Znajdź regułę:** Po uruchomieniu skrypt odczytuje zawartość `FUZZY_MAP_pre.py`. Wyszukuje unikalny komentarz zakotwiczenia `# TRANSLATION_RULE`.

2. **Przełącz stan:**
* **Aby wyłączyć:** Jeśli linia reguły pod kotwicą jest aktywna, skrypt dodaje `#` na początku linii, skutecznie ją komentując i wyłączając.
* **Aby włączyć:** Jeśli linia reguły jest już zakomentowana, skrypt ostrożnie usuwa wiodący `#`, ponownie aktywując regułę.

3. **Zapisz i załaduj ponownie:** Skrypt zapisuje zmodyfikowaną zawartość z powrotem do `FUZZY_MAP_pre.py`. Następnie tworzy specjalny plik wyzwalacza (np. `RELOAD_RULES.trigger`). Główna usługa stale obserwuje ten plik wyzwalający. Kiedy się pojawi, usługa wie, że jej konfiguracja została zmieniona i ponownie ładuje całą mapę reguł z dysku, natychmiastowo stosując zmianę.

### Filozofia projektowania: zalety i uwagi

To podejście polegające na bezpośredniej modyfikacji pliku konfiguracyjnego zostało wybrane ze względu na jego przejrzystość i prostotę dla użytkownika końcowego.

#### Zalety:

* **Wysoka przejrzystość:** Aktualny stan systemu jest zawsze widoczny. Szybkie spojrzenie na plik `FUZZY_MAP_pre.py` natychmiast ujawnia, czy reguła tłumaczenia jest aktywna, czy też została skomentowana.
* **Brak zmian w silniku podstawowym:** Ta zaawansowana funkcja została zaimplementowana bez zmiany ani jednej linii podstawowego silnika przetwarzania reguł. Pokazuje elastyczność systemu wtyczek.
* **Intuicyjny dla programistów:** Koncepcja włączania lub wyłączania fragmentu konfiguracji poprzez skomentowanie go jest znanym, prostym i zaufanym wzorcem dla każdego, kto pracował z kodem lub plikami konfiguracyjnymi.

#### Rozważania:

* **Uprawnienia systemu plików:** Aby ta metoda działała, proces asystenta musi mieć uprawnienia do zapisu własnych plików konfiguracyjnych. W niektórych środowiskach o wysokim poziomie bezpieczeństwa może to być brane pod uwagę.