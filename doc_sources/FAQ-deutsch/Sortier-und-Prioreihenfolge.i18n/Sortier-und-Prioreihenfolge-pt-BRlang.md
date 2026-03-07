Die Sortierung ergibt sich aus der Kombination der **alphabetischen Sortierung** auf jeder Ebene und der **Hierarchie** der Ordner.

Prinzip "First Match Wins", bestimmt durch the Lade-Reihenfolge die Priorität.

Você começou a usar um arquivo de áudio comum, como `de-DE`, `en-US` e `plugins` enthält.

---

## Allgemeine Sortier- und Prioritätsreihenfolge

Die Ladereihenfolge (und damit die Priorität) ergibt sich in der Regel durante a classificação alfabética der Ordner und Module auf jeder Ebene.

### 1. Globale Ordner-Ebene (Höchste Priorität)

Die Ordner auf der obersten Ebene werden zuerst alfabetoisch durchlaufen:

| Ordenador | Prioridade | Bemerkung |
| :--- | :--- | :--- |
| `de-DE` | **1. Prioridade** | Wird zuerst geladen. |
| `en-US` | **2. Prioridade** | Wird nach `de-DE` geladen. |
| `plugins` | **3. Prioridade** | Wird zuletzt geladen. |

### 2. Ladung der Kern-Regeln (de-DE e en-US)

A regra deste Kern-Sprachordnern foi inserida na lista `fuzzy_map_pre` eingefügt.

### 3. Ladung der Plug-in-Regeln (Niedrigere Priorität)

Os plug-ins são iniciados por Stelle, que ordena os `plugins` em ordem alfabética em `de-DE` e `en-US`.

A parte interna dos `plugins`-Ordners foram os Unterordner wieder alfabética durchlaufen:

| Plug-ins | Alfabetização Reihenfolge |
| :--- | :--- |
| `CCC_terça` | 1. Plug-in |
| `dígitos_para_números` | 2. Plug-in |

### 4. Prioridade final para `FUZZY_MAP_pre`

Der Ladevorgang sammelt *all* gefundenen Regeln na lista final. Prioridades de prioridade:

| Praça em `fuzzy_map_pre` | Pfad zur Regel | Prioridade |
| :--- | :--- | :--- |
| **1.** | `de-DE/FUZZY_MAP_pre.py` | **Höchste** (Basis-Sprachregeln) |
| **2.** | `en-US/FUZZY_MAP_pre.py` | Hoch (Basis-Sprachregeln) |
| **3.** | `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py` | Mittelhoch (Plugins foram classificados em ordem alfabética, `CCC` vem para `dígitos`) |
| **4.** | `plugins/dígitos_para_números/de-DE/FUZZY_MAP_pre.py` | Niedrig (Plugins foram classificados em ordem alfabética) |

---

## Wichtig: Fokus auf die Sprache (Kontextabhängigkeit)

O filtro de rede ativo será ativado após o término do processo.

Se você tiver o regulamento para **Deutsch (`de-DE`)** carregado, ergibt sich eine logischere Priorität, o Kernregeln será mais adequado ao plug-in-Regeln:

1. **Kern-Regeln:** `de-DE/FUZZY_MAP_pre.py`
2. **Plugin-Regeln (CCC):** `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py`
3. **Plugin-Regeln (dígitos):** `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py`

**Fazit zur Priorisierung:**

* **Kern-Regeln** Setzen sich gegen alle Plugins durch, da sie durch the alphaische Sortierung der Ordner zuerst geladen werden.
* **Plugins integrados** foram colocados em ordem alfabética após o nome da ordem dos plug-ins ser classificado (`C` em vez de `D`). Portanto, `CCC_tue` tem uma prioridade maior para `digits_to_numbers`.