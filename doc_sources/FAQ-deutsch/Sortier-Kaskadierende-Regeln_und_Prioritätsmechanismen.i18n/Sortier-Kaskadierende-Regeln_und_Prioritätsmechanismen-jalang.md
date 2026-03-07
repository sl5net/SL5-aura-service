# Kaskadierende Regelausführung und Priorität Mechanismen

詳細、優先順位、モードおよびフォールバックに関する複雑な情報はすべてありません。

---

# Kaskadierende Regelausführung und Priorität Mechanismen

レーゲルシステムの基本的な優先順位、優先順位、バイダーダイの位置はリスト `fuzzy_map_pre` の優先順位です (Modul-Lade-Reihenfolge > Zeilennummer)。

**Kaskadierenden Regelausführung** (`default_mode_is_all = True`) を含む Prinzip は、すべての Regeln nacheinander angewendet werden、bis ein spezifisches Stopp-Kriterium erfüllt ist を守ります。

## 1. 優先順位: Der Deterministische Durchlauf

Die Verarbeitung beginnt mit dem Durchlauf der Regeln in der geladenen Reihenfolge。 Anwendungen による優先順位:

### A. Absolutes Stopp-Kriterium (Höchste Priorität)
Die Regel mit der höchsten Priorität, die einen **volständigen Match** (von `^` bis `$`) auf das Token erzielt, wird angewendet und bedet die gesamte Verarbeitung für dieses Token sofort (**最初のマッチの勝利**)。特定の条件を満たし、決定性を持った Regel Vorrang の帽子を選びましょう。

### B. クムレーション (Transformationsreihenfolge)
Wenn eine Regel zutrifft、aber keinen vollständigen Match (`^...$`) erzielt、wird die Ersetzung angewendet。 Die Verarbeitung geht jedoch zur nächsten Regel über。 **変更内容** のテキストを読み取って、**Kaskadierung** の変換を聞いてください。

## 2. 優先順位: ファジーフォールバック

Fuzzy-Logic (Ähnlichkeitsscore 0–100) は、フォールバックを参照し、ローテキストのヒントを参照してください。

Aus Performance- und Stabilitätsgründen wird die Fuzzy-Logik **nur dann** aktiviert, wenn der gesamte deterministische Durchlauf (Punkt 1) **keine einzige Regel** angewendet hat。フラグと **ブロック** を決定するための決定的な規則は、トークンのファジー フォールバックではありません。

## 3. Die Externe Validierung (LanguageTool)

Nach Abschluss aller Regel-basierten Ersetzungen wird eine zusätzliche Prüfung durch LanguageTool (LT) durchgeführt, um stilistische oder grammatikalische Fehler zu beheben.

Dieses Tool wird jedoch übersprungen, wenn die Anzahl der durchgeführten Regel-Ersetzungen im Verhältnis zur ursprünglichen Textlänge einen Schwellenwert übersteigt (`LT_SKIP_RATIO_THRESHOLD`)。 Dies stellt sicher、dass LT nicht auf Texte angewendet wird、die durch unsere Kaskade bereits so stark Transformiert wurden、dass die Korrektur durch LT fehleranfällig wäre。