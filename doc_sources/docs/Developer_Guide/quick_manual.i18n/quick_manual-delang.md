## Erweiterte Regelattribute

Zusätzlich zu den Standardfeldern können Regeln um spezielle Optionen erweitert werden:

### `only_in_windows` (Fenstertitelfilter)
Trotz seines Namens ist dieses Attribut **Betriebssystemunabhängig**. Es filtert Regeln basierend auf dem Titel des aktuell aktiven Fensters.

* **Funktion:** Die Regel wird nur verarbeitet, wenn der Titel des aktiven Fensters mit einem der bereitgestellten Muster (Regex) übereinstimmt.
*   **Beispiel:**
    ```python
    (
        '|', 
        r'\b(pipe|symbol)\b', 
        75, 
        {'only_in_windows': ['Terminal', 'Console', 'iTerm']}
    ),
    ```
*In diesem Fall erfolgt die Ersetzung nur, wenn der Benutzer in einem Terminalfenster arbeitet.*

### `on_match_exec` (Skriptausführung)
Ermöglicht das Auslösen externer Python-Skripte, wenn eine Regel übereinstimmt.

* **Syntax:** `'on_match_exec': [CONFIG_DIR / 'script.py']`
* **Anwendungsfall:** Ideal für komplexe Aktionen wie API-Aufrufe, Dateisystemaufgaben oder die Generierung dynamischer Inhalte.