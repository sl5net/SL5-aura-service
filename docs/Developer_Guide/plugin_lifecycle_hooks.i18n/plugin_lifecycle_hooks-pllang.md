# Haki cyklu życia wtyczek

Aura SL5 obsługuje haki cyklu życia, które pozwalają wtyczkom (Mapom) automatycznie wykonywać określoną logikę, gdy zmienia się ich stan.

## Hak `on_reload()`

Funkcja `on_reload()` jest specjalną opcjonalną funkcją, którą możesz zdefiniować w dowolnej mapie wtyczek (`.py`).

### Zachowanie
* **Wyzwalacz:** Ta funkcja jest wykonywana **natychmiast po** udanym ponownym załadowaniu modułu na gorąco (wykryta zmiana pliku + wyzwolenie głosowe).
* **Kontekst:** Działa w ramach głównego przepływu aplikacji.
*   **Scope:** It is **NOT** executed during the initial system startup (cold start). Dotyczy wyłącznie scenariuszy *ponownego* ładowania.

### Przypadki użycia
* **Bezpieczeństwo:** automatycznie ponownie szyfruj lub ponownie pakuj poufne pliki po edycji.
* **Zarządzanie stanem:** Resetowanie liczników globalnych lub czyszczenie określonych pamięci podręcznych.
* **Powiadomienie:** rejestrowanie określonych informacji debugowania w celu sprawdzenia, czy zmiana została zastosowana.

### Szczegóły techniczne i bezpieczeństwo
* **Obsługa błędów:** Wykonanie jest opakowane w blok `try/except`. Jeśli Twoja funkcja `on_reload` ulegnie awarii (np. `DivisionByZero`), zarejestruje błąd („❌ Błąd podczas wykonywania on_reload...`), ale **nie spowoduje awarii Aury**.
* **Wydajność:** Funkcja działa synchronicznie. Unikaj długotrwałych zadań (takich jak duże pobieranie) bezpośrednio w tej funkcji, ponieważ na krótko blokują one przetwarzanie poleceń głosowych. W przypadku ciężkich zadań utwórz wątek.

### Przykładowy kod

__KOD_BLOKU_0__