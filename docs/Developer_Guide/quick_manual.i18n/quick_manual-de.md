
Hier ist das **SL5 Aura Dev-Cheatsheet** (Compact):

1.  **Pfad:** `config/maps/plugins/<name>/de-DE/` (Sprachordner ist **Pflicht**).
2.  **Timing:**
    *   `FUZZY_MAP_pre.py` = **Vor** LanguageTool (Raw Input, Commands, Speed).
    *   `FUZZY_MAP.py` = **Nach** LanguageTool (Korrigierter Text).
3.  **Action:** Tuple muss `'on_match_exec': [CONFIG_DIR / 'script.py']` nutzen.
    *   Ziel-Script benötigt: `def execute(match_data):`.
4.  **Override:** `'skip_list': ['LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']` erzwingt Ausführung bei unsicherem Input.
5.  **Hook:** `def on_reload():` in der Map für Wartungsaufgaben nach Hot-Reload.

---

### 📜 SL5 Aura Developer Standard (10.12.'25 18:34 Wed)

**1. Directory Structure (Mandatory)**
*   Plugins **müssen** in einem Sprach-Unterordner liegen.
*   ✅ Richtig: `config/maps/plugins/my_plugin/de-DE/FUZZY_MAP_pre.py`
*   ❌ Falsch: `config/maps/plugins/my_plugin/FUZZY_MAP_pre.py`

**2. File Naming (Pipeline Control)**
*   `FUZZY_MAP_pre.py`: **Pre-Processing**. Läuft **vor** LanguageTool. (Pflicht für Systemkommandos, Raw-Inputs, schnelle Reaktionen).
*   `FUZZY_MAP.py`: **Post-Processing**. Läuft **nach** LanguageTool (für korrigierten Text).

**3. Execution Pattern (Standard)**
*   Nutzung von `on_match_exec` für die Ausführung von Skripten.
*   Beispiel: `'on_match_exec': [CONFIG_DIR / 'my_script.py']`
*   Das Skript muss eine `def execute(match_data):` Funktion haben.

**4. Safety Override**
*   Um Sicherheitschecks bei unsicheren Inputs zu umgehen:
*   `'skip_list': ['LanguageTool', 'LT_SKIP_RATIO_THRESHOLD']` im Rule-Tuple hinzufügen.

**5. Lifecycle Hooks**
*   `def on_reload():` im Map-File definieren, um nach einem Hot-Reload Wartungsaufgaben (wie `secure_packer.py` via Daisy-Chain) zu starten.




## Erweiterte Regel-Attribute

Zusätzlich zu `search` und `replace` können Regeln durch weitere Attribute gesteuert werden:

### 1. `only_in_windows` (Fenster-Filter)
Trotz des Namens ist dieses Attribut **betriebssystemunabhängig**. Es dient dazu, die Ausführung einer Regel auf bestimmte aktive Fenster zu beschränken.

*   **Typ:** Liste von Strings oder Regex-Mustern.
*   **Funktion:** Die Regel wird nur angewendet, wenn der Titel des aktuell aktiven Fensters eines der Muster in der Liste enthält.
*   **Beispiel:**
    ```python
    (
        '|', 
        r'\b(pipe|treib symbol)\b', 
        75, 
        {
            'command_flags': re.IGNORECASE,
            'only_in_windows': ['Konsole', 'konsole', 'Terminal', 'Console']
        }
    ),
    ```
    *In diesem Beispiel wird das Wort "pipe" nur dann durch das Symbol "|" ersetzt, wenn der Benutzer sich in einem Terminal-Fenster befindet.*

### 2. `on_match_exec` (Dynamische Skripte)
Wie bereits erwähnt, erlaubt dieses Attribut die Ausführung externer Python-Logik.

*   **Syntax:** `'on_match_exec': [CONFIG_DIR / 'script.py']`
*   **Nutzen:** Ideal für API-Abfragen, Datei-Operationen oder komplexe Textersetzungen, die über einfaches Regex hinausgehen.
