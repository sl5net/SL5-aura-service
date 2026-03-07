Die Sortierung ergibt sich aus der **alphabetischen Sortierung** auf jeder Ebene 和 der **Hierarchie** der Ordner。

原则是“首场比赛获胜”，最好是在 Lade-Reihenfolge die Priorität 上。

开始使用同一个软件，包括“de-DE”、“en-US”和“plugins”。

---

## 全部排序和优先级

Die Ladereihenfolge（和 damit die Priorität）可以在 der Regel durch die 字母排序排序和模块 auf jeder Ebene 中使用。

### 1. Globale Ordner-Ebene (Höchste Priorität)

Die Ordner auf der obersten Ebene werden zuerst按字母顺序排列：

|奥德纳 |优先 |关闭 |
| :--- | :--- | :--- |
| `de-DE` | **1.优先** |最好的冰淇淋。 |
| `en-US` | **2.优先** | Wird nach `de-DE` geladen。 |
| `插件` | **3.优先** | Wird zuletzt geladen。 |

### 2. Ladung der Kern-Regeln (de-DE 和 en-US)

在“fuzzy_map_pre”列表中，您将看到 Kern-Sprachordnern 的状态。

### 3. Ladung der Plug-in-Regeln (Niedrigere Priorität)

插件最初是一个 Dritter Stelle，是按字母顺序排列的“插件”，包括“de-DE”和“en-US”。

Innerhalb des `plugins`-Ordners werden die Unterordner wieder Alphabetisch durchlaufen：

|插件|字母表 Reihenfolge |
| :--- | :--- |
| `CCC_tue` | 1. 插件 |
| `数字到数字` | 2. 插件|

### 4. 结束“FUZZY_MAP_pre”的优先级

Der Ladevorgang sammelt *alle* gefundenen Regeln in die Finale Liste。优先级：

| `fuzzy_map_pre` 中的 Platz |普法德·祖尔·雷格尔 |优先 |
| :--- | :--- | :--- |
| **1.** | `de-DE/FUZZY_MAP_pre.py` | **Höchste**（Basis-Sprachregeln）|
| **2.** | `en-US/FUZZY_MAP_pre.py` | Hoch（基础语言）|
| **3.** | `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py` | Mittelhoch（插件按字母排序，‘CCC’ kommt vor ‘digits’） |
| **4.** | `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py` | Niedrig（按字母顺序排序的插件）|

---

## Wichtig：Fokus auf die Sprache (Kontextabhängigkeit)

Es wird nach der aktuell aktiven Sprache gefiltert。

Wenn Sie nur die Regeln für **Deutsch (`de-DE`)** laden, ergibt sich eine logischere Priorität, die Kernregeln höher bewertet als die Plugin-Regeln:

1. **Kern-Regeln:** `de-DE/FUZZY_MAP_pre.py`
2. **插件-Regeln (CCC):** `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py`
3. **插件-Regeln（数字）：** `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py`

**优先考虑的因素：**

* **Kern-Regeln** 设置所有插件，然后按字母顺序排序。
* **插件下的插件**按字母顺序排列，名称为插件顺序排序（`C` 或 `D`）。因此，“CCC_tue”优先级为“digits_to_numbers”。