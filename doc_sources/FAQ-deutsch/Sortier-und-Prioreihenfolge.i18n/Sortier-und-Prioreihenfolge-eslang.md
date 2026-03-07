Die Sortierung ergibt sich aus der Kombination der **alphabetischen Sortierung** auf jeder Ebene und der **Jerarchie** der Ordner.

Prinzip "Primer partido gana", bestimmt durch die Lade-Reihenfolge die Priorität.

Sie starten den von einem gemeinsamen Wurzelverzeichnis aus, das `de-DE`, `en-US` y `plugins` enthält.

---

## Allgemeine Sortier- und Prioritätsreihenfolge

Die Ladereihenfolge (und damit die Priorität) ergibt sich in der Regel durch die alphabetische Sortierung der Ordner und Module auf jeder Ebene.

### 1. Globale Ordner-Ebene (Höchste Priorität)

Die Ordner auf der obersten Ebene werden zuerst alphabetisch durchlaufen:

| Ordenador | Prioridad | Bemerkung |
| :--- | :--- | :--- |
| `de-DE` | **1. Prioridad** | Wird zuerst geladen. |
| `en-US` | **2. Prioridad** | Wird nach `de-DE` geladen. |
| `complementos` | **3. Prioridad** | Wird zuletzt geladen. |

### 2. Ladung der Kern-Regeln (de-DE y en-US)

Die Regeln aus diesen Kern-Sprachordnern werden zuerst in the Liste `fuzzy_map_pre` eingefügt.

### 3. Ladung der Plug-in-Regeln (Niedrigere Priorität)

Los complementos son primero una estrella, el orden alfabético de los "complementos" en "de-DE" y "en-US".

Innerhalb des `plugins`-Ordners werden die Unterordner wieder alfabético durchlaufen:

| Complemento | Alphabetische Reihenfolge |
| :--- | :--- |
| `CCC_mar` | 1. Complemento |
| `dígitos_a_números` | 2. Complemento |

### 4. Lista de prioridades finales para `FUZZY_MAP_pre`

Der Ladevorgang sammelt *alle* gefundenen Regeln in die finale Liste. Prioritätsreihenfolge:

| Plaza en `fuzzy_map_pre` | Pfad zur Regel | Prioridad |
| :--- | :--- | :--- |
| **1.** | `de-DE/FUZZY_MAP_pre.py` | **Höchste** (Basis-Sprachregeln) |
| **2.** | `es-ES/FUZZY_MAP_pre.py` | Hoch (Basis-Sprachregeln) |
| **3.** | `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py` | Mittelhoch (Los complementos se sortean alfabéticamente, `CCC` kommt vor `digits`) |
| **4.** | `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py` | Niedrig (Los complementos se sortean alfabéticamente) |

---

## Wichtig: Fokus auf die Sprache (Kontextabhängigkeit)

Es wird nach der aktuell aktiven Sprache gefiltert.

Cuando no hay reglas para **Deutsch (`de-DE`)** cargadas, ergibt sich una prioridad logística, el Kernregeln höher bewertet als die Plugin-Regeln:

1. **Regla del núcleo:** `de-DE/FUZZY_MAP_pre.py`
2. **Región del complemento (CCC):** `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py`
3. **Región del complemento (Dígitos):** `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py`

**Fazit zur Priorisierung:**

* **Kern-Regeln** configure sich gegen alle Plugins durch, da sie durch die alphabetische Sortierung der Ordner zuerst geladen werden.
* **Los complementos incluidos** se escriben alfabéticamente según los nombres de los pedidos de complementos ordenados (`C` o `D`). Esto significa que `CCC_tue` tiene una prioridad alta respecto a `digits_to_numbers`.