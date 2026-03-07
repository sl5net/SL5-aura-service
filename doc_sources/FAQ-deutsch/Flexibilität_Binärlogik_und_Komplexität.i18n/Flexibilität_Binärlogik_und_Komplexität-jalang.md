## Die Flexibilität des Regelwerks: Von Binärlogik zur Komplexität

優先順位と詳細設定の組み合わせ (順序付け、フル マッチ ストップ、累積、ファジー フォールバック) の柔軟な対応:

### 1. Einfache (Binäre) Steuerung durch höchste Priorität

フル マッチ ストップ** で位置を決定する ** 優先順位を決定し、** カンファレンス アイン/オーシャルト メカニズム (「トグル」) を設定します。

* **例:** `FUZZY_MAP_pre` の Eine Regel ganz oben kann einen bestimmten Eingabestring (z. B. ein einfaches Kommandowort) erkennen、sofort verarbeiten und damit die gesamte nachfolgende Kaskade für dieses Token blockieren。さまざまなコマンドを使用して、さまざまな設定を行うことができます。

### 2. 複雑なアンパスンゲンとフレームワークの統合

Gleichzeitig erlaubt der Aufbau die Implementierung von komplexen, kaskadierenden Modifikationen, die für spezifische Framework-Anforderungen (wie CodeIgniter oder ähnliche) notwendig sind:

* **Kumulation:** Durch die Kumulation können mehrere Regeln sequenziell auf den Text angewendet werden, um beispielsweise die Benennungskonventionen oder Platzhalter eines Frameworks schrittweise in eine gewünschte Ausgabe zu überführen.
* **プラグイン:** `plugins/` の階層構造は、フレームワークの特別なプロジェクト (z.B. für CodeIgniter) としても、別個のモジュール ヒンツゲフグト ウェルデン コンネンから構成されています。プラグイン レーゲルは、定義されたものであり、優先順位は Kern-Sprachregeln であり、Kernlogik unangetastet bleibt であるため、優先順位は erweitert werden kann です。

**ファジット:** フレームワークの制御と優先順位 (モジュール > ツァイレ) とフル マッチの停止クリテリウムの制御により、フレームワークの詳細を確認できます。 Kontrolle uber den Verarbeitungsprozess。