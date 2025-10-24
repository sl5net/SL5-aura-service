Die Sortierung ergibt sich aus der Kombination der **alphabetischen Sortierung** auf jeder Ebene und der **Hierarchie** der Ordner.

Prinzip "First Match Wins", bestimmt durch die Lade-Reihenfolge die Priorität.

Sie starten den von einem gemeinsamen Wurzelverzeichnis aus, das `de-DE`, `en-US` und `plugins` enthält.

---

## Allgemeine Sortier- und Prioritätsreihenfolge

Die Ladereihenfolge (und damit die Priorität) ergibt sich in der Regel durch die alphabetische Sortierung der Ordner und Module auf jeder Ebene.

### 1. Globale Ordner-Ebene (Höchste Priorität)

Die Ordner auf der obersten Ebene werden zuerst alphabetisch durchlaufen:

| Ordner | Priorität | Bemerkung |
| :--- | :--- | :--- |
| `de-DE` | **1. Priorität** | Wird zuerst geladen. |
| `en-US` | **2. Priorität** | Wird nach `de-DE` geladen. |
| `plugins` | **3. Priorität** | Wird zuletzt geladen. |

### 2. Ladung der Kern-Regeln (de-DE und en-US)

Die Regeln aus diesen Kern-Sprachordnern werden zuerst in die Liste `fuzzy_map_pre` eingefügt.

### 3. Ladung der Plug-in-Regeln (Niedrigere Priorität)

Die Plug-ins kommen erst an dritter Stelle, da der Ordner `plugins` alphabetisch nach `de-DE` und `en-US` kommt.

Innerhalb des `plugins`-Ordners werden die Unterordner wieder alphabetisch durchlaufen:

| Plug-in | Alphabetische Reihenfolge |
| :--- | :--- |
| `CCC_tue` | 1. Plug-in |
| `digits_to_numbers` | 2. Plug-in |

### 4. Endgültige Prioritätskette für `FUZZY_MAP_pre`

Der Ladevorgang sammelt *alle* gefundenen Regeln in die finale Liste. Prioritätsreihenfolge:

| Platz in `fuzzy_map_pre` | Pfad zur Regel | Priorität |
| :--- | :--- | :--- |
| **1.** | `de-DE/FUZZY_MAP_pre.py` | **Höchste** (Basis-Sprachregeln) |
| **2.** | `en-US/FUZZY_MAP_pre.py` | Hoch (Basis-Sprachregeln) |
| **3.** | `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py` | Mittelhoch (Plugins werden alphabetisch sortiert, `CCC` kommt vor `digits`) |
| **4.** | `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py` | Niedrig (Plugins werden alphabetisch sortiert) |

---

## Wichtig: Fokus auf die Sprache (Kontextabhängigkeit)

Es wird nach der aktuell aktiven Sprache gefiltert.

Wenn Sie nur die Regeln für **Deutsch (`de-DE`)** laden, ergibt sich eine logischere Priorität, die Kernregeln höher bewertet als die Plugin-Regeln:

1.  **Kern-Regeln:** `de-DE/FUZZY_MAP_pre.py`
2.  **Plugin-Regeln (CCC):** `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py`
3.  **Plugin-Regeln (Digits):** `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py`

**Fazit zur Priorisierung:**

*   **Kern-Regeln** setzen sich gegen alle Plugins durch, da sie durch die alphabetische Sortierung der Ordner zuerst geladen werden.
*   **Plugins untereinander** werden strikt alphabetisch nach dem Namen des Plugin-Ordners sortiert (`C` vor `D`). Das bedeutet, `CCC_tue` hat eine höhere Priorität als `digits_to_numbers`.

