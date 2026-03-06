## Zaawansowane atrybuty reguł

Oprócz standardowych pól reguły można wzbogacić o opcje specjalne:

### `only_in_windows` (Filtr tytułu okna)
Pomimo swojej nazwy, ten atrybut jest **niezależny od systemu operacyjnego**. Filtruje reguły na podstawie tytułu aktualnie aktywnego okna.

* **Funkcja:** Reguła jest przetwarzana tylko wtedy, gdy tytuł aktywnego okna pasuje do jednego z podanych wzorców (Regex).
*   **Przykład:**
__KOD_BLOKU_0__
*W tym przypadku wymiana następuje tylko wtedy, gdy użytkownik pracuje w oknie terminala.*

### `on_match_exec` (wykonanie skryptu)
Umożliwia uruchamianie zewnętrznych skryptów Pythona, gdy reguła pasuje.

* **Składnia:** `'on_match_exec': [CONFIG_DIR / 'script.py']`
* **Przypadek użycia:** Idealny do złożonych działań, takich jak wywołania API, zadania systemu plików lub generowanie zawartości dynamicznej.