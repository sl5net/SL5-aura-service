# Prioritätslogik (ファジーとフォールバックを含む)
Fuzzy-Berechnungen ではフォールバック機能が複雑になっています。


---

## 新しい優先順位ロジック (ファジーとフォールバックを含む)

これは、モジュール「default_mode_is_all = True」 (Kumulierung) との組み合わせで、**zweistufiger Prioritäts-Workflow** で実行されているものです:

### フェーズ 1: 高優先度 (決定論) デュルシュラウフ

Die Engine durchläuft die gesamte Liste `fuzzy_map_pre` (Modul-Reihenfolge > Zeilennummer)。

#### A. Stopp-Kriterium (Höchste Priorität)

Wenn eine Regel einen **フル マッチ** (`^...$`) erzielt、stoppt die Verarbeitung für dieses Token sofort。

* **優先順位:** レーゲルは、完全な一致を確認し、明確な決定を下し、プロゼスに従う必要があります。

#### B. Kumulations-Kriterium (Hohe Priorität)

Wenn eine Regel **keinen Full Match**、aber einen **partieln Match** oder eine Sonstige Ersetzung (ohne Stopp-Kriterium) erzielt:

* Die Ersetzung wird angewendet。
* **WICHTIG:** 変数 `current_rule_matched` が `True` であることを確認します。
* Die Verarbeitung geht zur nächsten Regel über (Kumulation)。

**優先順位:** Die Reihenfolge der Regeln ist hier entscheidend für die **Anwendungsreihenfolge**。テキストの内容を変更して、Regeln を修正します。

---

### フェーズ 2: 低優先度 (ファジー) フォールバック

Fuzzy-Check wird nur ausgelöst, wenn der gesamte deterministische Durchlauf (フェーズ 1) abgeschlossen ist und **keine einzige Regel** angewendet wurde (`current_rule_matched` ist immer noch `False`)。

Wenn der Fuzzy-Check ausgeführt wird、金色:

1. テキストが Wörtern に表示されるとき、**Zielwert** (`置換`) ähnlich sind (basierend auf der Schwelle) が表示されます。
2. ファジーマッチがうまく機能し、正確な結果が得られます。
3. **WICHTIG:** 死ぬ **ファジー関数が停止するのは、非常に難しい問題であり、ファジーマッチが難しいからです**。

#### ファジー レーゲルの優先順位は次のとおりでした:

```python
# Pseudo-Code:
for rule in fuzzy_map_pre:
    # 1. Deterministic/Regex checks here...

# Wenn Phase 1 beendet ist und KEIN Match gefunden wurde:
if not current_rule_matched:
    # 2. Fuzzy Fallback
    for rule in fuzzy_map_pre: # WIRD HIER DIE LISTE NOCHMAL DURCHLAUFEN?
        # Führe den Fuzzy-Check auf Basis der replacement/threshold der Regel durch.
```

**Fuzzy-Funktion は、すべてを解決するものではありません。

---

## フィナーレの優先順位 - ファジット

曖昧な詳細を実現するために、**決定段階 (フェーズ 1)** を決定し、リストのリストを作成します。

**Die höchste Priorität liegt bei den Regeln, die ganz oben in `fuzzy_map_pre` stehen, und sich an der Determinismus-Logik beteiligen (完全一致または累積)。**

1. **Stopp-Kriterium (^...$) の範囲:** 最も重要な点は、優先順位です。
2. **Regeln zur Kumulation (partieller Match):** Müssen in der logischen Reihenfolge der Transformationen stehen (vom Rohtext zur Finalen Form)。 `current_rule_matched` を `True` および **blockieren** として設定し、トークンのファジー フォールバックを制限します。
3. **ファジーフォールバック:** は **優先順位** です。活動的なものは、帽子の決定的な役割を果たします。

**ウィヒティグ:** Jede Regel (auch eine kumulierende, nicht-stoppende Regel)、フェーズ 1 で死亡します。トークンが死ぬまで **ファジー フォールバック** で死亡します。 Dies muss beim Design dergenerischen Regeln berücksichtigt werden.