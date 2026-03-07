**アルファベットの組み合わせ**を使用して、Ebene と **Hierarchie** der Ordner を組み合わせます。

プリンツィプ「初戦勝利」、ラーデ・ライヘンフォルゲの優先順位が最高です。

Sie starten den von einem gemeinsamen Wurzelverzeichnis aus、das `de-DE`、`en-US` および `plugins` enthält。

---

## Allgemeine Sortier- und Prioritätsreihenfolge

Die Ladereihenfolge (und damit die Priorität) は、Ebene の Ordner および Module をアルファベット順に選択します。

### 1. Globale Ordner-Ebene (Höchste Priorität)

Die Ordner auf der obersten Ebene werden zuerst alphabetisch durchlaufen:

|オードナー |優先順位 |ベーメルクング |
| :--- | :--- | :--- |
| `脱DE` | **1.優先順位** |ヴィルド・ツュルスト・ジェラーデン。 |
| `en-US` | **2.優先順位** |ヴィルドナッハ「ドDE」ゲラデン。 |
| `プラグイン` | **3.優先順位** |ヴィルド・ズレツト・ゲラーデン。 |

### 2. Ladung der Kern-Regeln (de-DE und en-US)

`fuzzy_map_pre` のリストを参照してください。

### 3. Ladung der Plug-in-Regeln (Niedrigere Priorität)

プラグインは、ドリッター Stelle、da der Ordner の「プラグイン」のアルファベットを「de-DE」と「en-US」に合わせて作成します。

Innerhalb des `plugins`-Ordners werden die Unterordner wieder alphabetisch durchlaufen:

|プラグイン |アルファベット順
| :--- | :--- |
| `CCC_tue` | 1. プラグイン |
| `数字から数字へ` | 2. プラグイン |

### 4. `FUZZY_MAP_pre` の優先順位を決定する

Der Ladevorgang sammelt *alle* gefundenen Regeln in die Finale Liste。優先事項:

| `fuzzy_map_pre` のプラッツ |プファド ツア レーゲル |優先順位 |
| :--- | :--- | :--- |
| **1.** | `de-DE/FUZZY_MAP_pre.py` | **Höchste** (ベーシス シュプラッハレーゲルン) |
| **2.** | `en-US/FUZZY_MAP_pre.py` | Hoch (Basis-Sprachregeln) |
| **3.** | `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py` | Mittelhoch (アルファベットを並べ替えるプラグイン、`CCC` kommt vor `digits`) |
| **4.** | `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py` | Niedrig (アルファベット順のプラグイン) |

---

## Wichtig: Fokus auf die Sprache (Kontextabhängigkeit)

操作を実行することはできません。

**Deutsch (`de-DE`)** を積んだ状態で、優先順位を決定し、Plugin-Regeln に従う必要があります:

1. **Kern-Regeln:** `de-DE/FUZZY_MAP_pre.py`
2. **プラグイン Regeln (CCC):** `plugins/CCC_tue/de-DE/FUZZY_MAP_pre.py`
3. **Plugin-Regeln (Digits):** `plugins/digits_to_numbers/de-DE/FUZZY_MAP_pre.py`

**優先順位:**

* **Kern-Regeln** はすべてのプラグインを設定し、アルファベット順に並べ替えます。
* **プラグインは見つかりません** アルファベット順に名前を付け、プラグインの順序を決定します (`C` または `D`)。 Das bedeutet、「CCC_tue」は「数字から数字」を優先します。