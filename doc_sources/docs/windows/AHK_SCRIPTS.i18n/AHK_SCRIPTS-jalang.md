### マークダウン ドキュメント (`docs/AHK_SCRIPTS.md`)

# SL5-Aura-Service の AutoHotkey インフラストラクチャ

Windows ではファイル ロックとシステム ホットキーの処理方法が Linux とは異なるため、このプロジェクトでは AutoHotkey (v2) スクリプトのセットを使用して、Python STT エンジンと Windows ユーザー インターフェイスの間のギャップを埋めます。

## スクリプトの概要

### 1. `trigger-hotkeys.ahk`
* **目的:** サービスを制御するためのメイン ユーザー インターフェイス。
* **主な機能:**
* **F10** と **F11** をインターセプトしてディクテーションを開始/停止します。
* 「キーボード フック」を使用して、デフォルトの Windows システム動作 (例: F10 キーでメニュー バーをアクティブにする) をオーバーライドします。
* **展開:** Windows タスク スケジューラを介して「最高の特権」で登録されるように設計されているため、ユーザーが管理者レベルのアプリケーションで作業している場合でもホットキーをキャプチャできます。

### 2. `type_watcher.ahk`
* **目的:** STT パイプラインの「コンシューマー」として機能します。
* **主な機能:**
* Python エンジンによって生成された受信 `.txt` ファイルの一時ディレクトリを監視します。
* **ステート マシン (ゾンビ マップ):** 各ファイルが正確に 1 回入力されるようにするために、メモリベースのマップを実装します。これにより、冗長な Windows ファイル システム イベント (追加/変更) によって引き起こされる「二重入力」が防止されます。
* **安全な入力:** `SendText` を使用して、アクティブなエディターで特殊文字が正しく処理されるようにします。
* **信頼性の高いクリーンアップ:** Windows ファイル アクセス ロックを処理するための再試行ロジックを使用してファイルの削除を管理します。

### 3. `scripts/ahk/sync_editor.ahk`
* **目的:** ディスクとテキスト エディタ (Notepad++ など) の間のシームレスな同期を保証します。
* **主な機能:**
* **オンデマンド保存:** Python によってトリガーされ、エンジンがファイルを読み取る前にエディターで「Ctrl+S」を強制的に押すことができます。
* **ダイアログ オートメーター:** 「別のプログラムによって変更されたファイル」リロード ダイアログを自動的に検出して確認し、スムーズなリアルタイム更新エクスペリエンスを実現します。
* **視覚的なフィードバック:** 修正が適用されていることをユーザーに通知するための短期間の通知ボックスを提供します。

### 4. `scripts/notification_watcher.ahk`
* **目的:** バックグラウンド プロセスに UI フィードバックを提供します。
* **主な機能:**
* 特定のステータス ファイルまたはイベントを監視して、ユーザーに通知を表示します。
* メッセージの「計算」ロジック (Python) をメッセージの「表示」 (AHK) から切り離し、メインの STT エンジンが UI インタラクションによってブロックされないようにします。


---

### 管理者以外のフォールバック
アプリケーションが管理者権限なしで実行されている場合:
- **機能:** サービスは引き続き完全に機能します。
- **ホットキーの制限:** **F10** などのシステムで予約されているキーは、引き続き Windows メニューをトリガーする可能性があります。この場合、ホットキーを非システム キー (「F9」や「Insert」など) に変更することをお勧めします。
- **タスク スケジューラ:** 「AuraDictation_Hotkeys」タスクが管理者インストール中に作成された場合、スクリプトは標準ユーザーであっても高い権限で実行されます。そうでない場合、「start_dictation.bat」はローカルのユーザーレベルのインスタンスをサイレントに起動します。

---

### 3. Warum "nervige Meldungen" erscheinen und wie man sie im AHK-Code stoppt
Um sicherzustellen, dass das Skript selbst niemals den Nutzer mit Popups stört, füge diese "Silent-Flags" oben in deine `.ahk` Dateien ein:

```autohotkey
#Requires AutoHotkey v2.0
#SingleInstance Force   ; Ersetzt alte Instanzen ohne zu fragen
#NoTrayIcon            ; (Optional) Wenn du kein Icon im Tray willst
ListLines(False)       ; Erhöht Performance und verbirgt Debug-Logs
```

### 4. ホットキーの戦略 (F10 の代替)
Da F10 ohne Admin-Rechte unter Windows fast unmöglich sauber abzufangen ist, könntest du im `trigger-hotkeys.ahk` eine Weiche einbauen:

```autohotkey
if !A_IsAdmin {
    ; Wenn kein Admin, warne den Entwickler im Log
    ; Log("Running without Admin - F10 might be unreliable")
}

; Nutze Wildcards, um die Chance zu erhöhen, dass es auch ohne Admin klappt
*$f10::
{
    ; ... Logik
}
```

### Zusammenfassung der Verbesserungen:
1. **バッチ日付:** Nutzt `start "" /b`、um das schwarze Fenster zu vermeiden、und prüft vorher、ob der Admin-Task schon läuft。
2. **トランスペアレンツ:** Die Doku erklärt nun offen: 「Kein Admin? Kein 問題、nimm einfach eine andere Taste als F10」。
3. **AHK-スクリプト:** Nutzt `#SingleInstance Force`、うーん、「古いインスタンスが実行されています」 - ダイアログ zu unterdrücken。

ソフトウェアのプロフェッショナラー (「スムーズ」) を使用して、ヒンターグルンドを開始し、技術的な詳細を確認してください。
  
  
---

### このドキュメントが重要な理由:
**「ゾンビ マップ」** と **「タスク スケジューラ/管理者」** の要件を文書化することで、コードが単純な Linux スクリプトよりも複雑である理由を他の開発者 (そして将来の自分) に説明できます。これにより、「奇妙な回避策」が「Windows の制限に対する巧妙なソリューション」に変わります。

(s,29.1.'26 11:02 木)