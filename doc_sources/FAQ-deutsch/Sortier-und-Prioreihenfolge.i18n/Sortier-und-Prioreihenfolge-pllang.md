Die Sortierung ergibt sich aus der Kombination der **alphabetischen Sortierung** auf jeder Ebene und der **Hierarchie** der Ordner.

Prinzip „First Match Wins”, bestimmt durch die Lade-Reihenfolge die Priorität.

Sie starten den von einem gemeinsamen Wurzelverzeichnis aus, das `de-DE`, `en-US` i `plugins` enthält.

---

## Allgemeine Sortier- und Prioritätsreihenfolge

Die Ladereihenfolge (und damit die Priorität) ergibt sich in der Regel durch die alfabetische Sortierung der Ordner und Module auf jeder Ebene.

### 1. Globale Ordner-Ebene (Höchste Priorität)

Die Ordner auf der obersten Ebene werden zuerst alfabetisch durchlaufen:

| Zamów | Priorytet | Informacje |
| :--- | :--- | :--- |
| `de-DE` | **1. Priorytet** | Wird zuerst geladen. |
| `en-US` | **2. Priorytet** | Wird nach `de-DE` geladen. |
| `wtyczki` | **3. Priorytet** | Wird zuletzt geladen. |

### 2. Ladung der Kern-Regeln (de-DE i en-US)

Die Regeln aus diesen Kern-Sprachordnern werden zuerst in die Liste `fuzzy_map_pre` eingefügt.

### 3. Ladung der Plug-in-Regeln (Niedrigere Priorität)

Die Plugins kommen erst an dritter Stelle, da der Ordner `plugins` alfabetisch nach `de-DE` i `en-US` kommt.

Innerhalb des `plugins`-Ordners werden die Unterordner wieder alfabetisch durchlaufen:

| Wtyczka | Alphabetische Reihenfolge |
| :--- | :--- |
| `CCC_wtorek` | 1. Wtyczka |
| `cyfry_na_liczby` | 2. Wtyczka |

### 4. Endgültige Prioritätskette für `FUZZY_MAP_pre`

Der Ladevorgang sammelt *alle* gefundenen Regeln w finale Liste. Prioritätsreihenfolge:

| Miejsce w `fuzzy_map_pre` | Pfad zur Regel | Priorytet |
| :--- | :--- | :--- |
| **1.** | `de-DE/FUZZY_MAP_pre.py` | **Höchste** (Basis-Sprachregeln) |
| **2.** | `en-US/FUZZY_MAP_pre.py` | Hoch (Basis-Sprachregeln) |
| **3.** | `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py` | Mittelhoch (Wtyczki werden alfabetisch sortiert, `CCC` kommt vor `digits`) |
| **4.** | `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py` | Niedrig (Wtyczki są sortowane alfabetycznie) |

---

## Wichtig: Fokus auf die Sprache (Kontextabhängigkeit)

Es wird nach der aktuell aktiven Sprache gefiltert.

Wenn Sie nur die Regeln für **Deutsch (`de-DE`)** laden, ergibt sich eine logischere Priorität, die Kernregeln höher bewertet als die Plugin-Regeln:

1. **Kern-Regeln:** `de-DE/FUZZY_MAP_pre.py`
2. **Regeln wtyczki (CCC):** `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py`
3. **Regeln wtyczki (cyfry):** `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py`

**Fazit zur Priorisierung:**

* **Kern-Regeln** setzen sich gegen alle Plugins duch, da sie durch die alfabetische Sortierung der Ordner zuerst geladen werden.
* **Plugins untereinander** werden strikt alfabetisch nach dem Namen des Plugin-Ordners sortiert (`C` vor `D`). Das bedeutet, `CCC_tue` hat eine höhere Priorität als `digits_to_numbers`.