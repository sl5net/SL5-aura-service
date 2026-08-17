# 🧠 SL5 Aura: Erweiterte オフライン LLM 統合

**ステータス:** 製品情報
**エンジン:** オラマ (ラマ 3.2 3B)
**遅延:** Sofort (キャッシュ ヒットにより <0.1 秒) / ~20 秒 (CPU の生成)

## 1. 「建築家とプラクティカント」の哲学を死ぬ
ハイブリッド モデルにおけるオーラの説明、**Präzision** と **Flexibilität** の検証:
* **Der Architekt (RegEx/Python):** Systembefehle の決定機能 (「Browser öffnen」、「Lauter」)。
* **Der Praktikant (Lokales LLM):** Übernimmt unscharfe Anfragen、Zusammenfassungen und Allgemeinwissen。活動は活発で、Regel の苦悩は消えません。

---

## 2. パフォーマンス建築家

正常な CPU (GPU) を使用している LLM は、**3-Stufen-Strategie**:

### Stufe 1: Der "Instant Modus" (Schlagworte)
* **トリガー:** Wörter は、「インスタント」、「シュネル」、「ゾフォート」を指します。
* **Logic:** LLM komplett の内容。 Vergleicht Schlagworte der Eingabe direkt mit der SQLite-Datenbank。
* **遅延:** **< 0.05s**

### Stufe 2: インテリジェント キャッシュ (SQLite)
* **Logik:** Jeder プロンプト wird gehasht (SHA256)。 `llm_cache.db` を削除してください。
* **機能「アクティブ バリエーション」:** システム マンシュマル (20% の確率) でキャッシュ トレファーの生成を開始します。 Ziel: ~5 Varianten pro Frage für mehr Lebendigkeit。
* **機能「セマンティック ハッシュ」:** フラゲン (>50 Zeichen) LLM の特別なキーワード (z.B. "installation anleitung") とハッシュ キーワード。 「Wie installiere ich es?」 「インストールに関する情報」も同様です。
* **遅延:** **~0.1s**

### Stufe 3: API の生成 (フォールバック)
* **ロジック:** キャッシュは存在しますが、Ollama API (`http://localhost:11434/api/generate`) を使用する必要があります。
* **最適化:**
* **ハードリミット:** `num_predict=60` のモデルの変更、およそ 1 秒40 ヴェルターン・ズ・ストッペン。
* **入力パイプ:** テキスト (README) は、STDIN の詳細、および Betriebssystems の議論の限界を示しています。
* **遅延:** **~15 ～ 25 秒** (CPU による影響)

---

## 3. システムの接地 (幻覚防止)

一般的な LLM は GUI (ボタン、メニュー) と呼ばれます。 **`AURA_TECH_PROFILE`** の制限事項:

1. **Keine GUI:** Aura はヘッドレス CLI に含まれています。
2. **Keine 設定ファイル:** ロジックは Python コード、`.json`/`.xml` を記述します。
3. **トリガー:** Externe Steuerung erfolgt über Dateisystem-Events (`touch /tmp/sl5_record.trigger`)、nicht über API。
4. **インストール:** Dauert の実際の 4GB モデルのダウンロード (verhindert falsche Versprechen) は 10 ～ 20 分です。

---

## 4. クリップボード ブリッジ (Linux セキュリティ)

Hintergrunddienste (systemd) können aus Sicherheitsgründen oft nicht auf die Zwischenablage (X11/Wayland) zugreifen。
* **Lösung:** ユーザー セッション (`clipboard_bridge.sh`) のスクリプトを参照し、RAM ディスク データ (`/tmp/aura_clipboard.txt`) に取り込みます。
* **オーラ:** Liest diese Datei und umgeht so alle Rechte-問題。

---

## 5. Selbst-Lernen (キャッシュウォーミング)

スクリプト「warm_up_cache.py」を書きます:
1. プロジェクトの「README.md」が最も重要です。
2. LLM の美しさ、ユーザーのアクセス制限など。
3. オーラを破壊する必要はありませんが、日付銀行を自動的に実行する必要があります。