Die Sortierung ergibt sich aus der Kombination der **alphabetischen Sortierung** auf jeder Ebene und der **Hierarchie** der Ordner.

Prinzip "첫 번째 경기 승리", bestimmt durch die Lade-Reihenfolge die Priorität.

Wurzelverzeichnis aus, das `de-DE`, `en-US` 및 `plugins` 사용을 시작하세요.

---

## Allgemeine Sortier- 및 Prioritätsreihenfolge

Die Ladereihenfolge (und damit die Priorität) ergibt sich in der Regel durch die Alphabetische Sortierung der Ordner und Module auf jeder Ebene.

### 1. Globale Ordner-Ebene(Höchste Priorität)

Die Ordner auf der obersten Ebene werden zuerst 알파벳순 durchlaufen:

| 오드너 | 우선순위 | 베메르쿵 |
| :--- | :--- | :--- |
| `드-DE` | **1. 우선순위** | Wird zuerst 젤라덴. |
| `en-US` | **2. 우선순위** | Wird nach `de-DE` 젤라덴. |
| `플러그인` | **3. 우선순위** | Wird zuletzt 젤라덴. |

### 2. Ladung der Kern-Regeln(de-DE 및 en-US)

Die Regeln aus diesen Kern-Sprachordnern werden zuerst in die Liste `fuzzy_map_pre` eingefügt.

### 3. Ladung der Plug-in-Regeln(Niedrigere Priorität)

플러그인 설명은 Stelle, da der Ordner의 '플러그인' 알파벳순으로 'de-DE' 및 'en-US' kommt에 해당합니다.

Innerhalb des `plugins`-Ordners werden die Unterordner wieder Alphabetisch durchlaufen:

| 플러그인 | 알파벳순으로 작성 |
| :--- | :--- |
| `CCC_화` | 1. 플러그인 |
| `digits_to_numbers` | 2. 플러그인 |

### 4. `FUZZY_MAP_pre`에 대한 우선 순위 종료

Der Ladevorgang sammelt *alle* gefundenen Regeln in die finale Liste. 우선순위:

| 'fuzzy_map_pre'의 Platz | 파드 주르 레겔 | 우선순위 |
| :--- | :--- | :--- |
| **1.** | `de-DE/FUZZY_MAP_pre.py` | **Höchste** (Basis-Sprachregeln) |
| **2.** | `en-US/FUZZY_MAP_pre.py` | 호흐(Basis-Sprachregeln) |
| **3.** | `플러그인/CCC_tue/de-DE/FUZZY_MAP_pre.py` | Mittelhoch(플러그인 werden Alphabetisch sortiert, `CCC` kommt vor `digits`) |
| **4.** | `플러그인/digits_to_numbers/de-DE/FUZZY_MAP_pre.py` | Niedrig(플러그인 werden Alphabetisch sortiert) |

---

## Wichtig: Fokus auf die Sprache(Kontextabhängigkeit)

Sprache gefiltert의 활성 상태를 확인하는 것이 좋습니다.

Wenn Sie nur die Regeln für **Deutsch (`de-DE`)** laden, ergibt sich eine logischere Priorität, die Kernregeln höher bewertet als die Plugin-Regeln:

1. **컨-레겔른:** `de-DE/FUZZY_MAP_pre.py`
2. **플러그인 등록(CCC):** `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py`
3. **플러그인 등록(숫자):** `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py`

**Fazit zur Priorisierung:**

* **Kern-Regeln** setzen sich gegen alle Plugins durch, da sie durch die Alphabetische Sortierung der Ordner zuerst geladen werden.
* **플러그인은 확장되지 않습니다** werden strikt Alphabetisch nach dem Namen des Plugin-Ordners sortiert(`C` 또는 `D`). 물론, `CCC_tue`는 `digits_to_numbers`로 우선순위가 지정됩니다.