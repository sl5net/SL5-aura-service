## 目標: 「ディクテーション セッション」モデル

### Unser Ziel(ドイツ語): 「ディクティエ・シツング」死ね

アイン アインツィガー トリガー スタート アイン **「Diktier-Sitzung」**、フェイゼン ベスト:

1. **開始フェーズ (Warten auf Sprache):**
* Nach dem Trigger lauscht das システム。
* Wenn **keine** Spracheingabe erfolgt, endet die gesamte Sitzung nach `PRE_RECORDING_TIMEOUT` (z.B. 12s)。

2. **Aktivphase (Kontinuierliches Diktieren):**
* Sobald die erste Spracheingabe erkannt wird、wechselt die Sitzung in den aktiven Modus。
* Immer wenn VOSK eine Sprechpause erkennt und einen Textblock liefert (z.B. einen Satz)、wird Dieser Block **sofort** zur Verarbeitung (LanguageTool など) weitergegeben und als Text ausgegeben。
* Die Aufnahme läuft währenddessen **nahtlos weiter**。 Die Sitzung wartet auf den nächsten Satz。

3. **エンドフェーズ (Ende der Sitzung):**
* 最も重要な問題は次のとおりです:
* Der Nutzer bleibt für die Dauer des `SPEECH_PAUSE_TIMEOUT` (z.B. 1-2s) komplett はまだです。
* トリガーごとに、Der Nutzer stoppt die Sitzung manuell。

**Zusammengefasst:** Eine Sitzung、viele sofortige Textausgaben。活動を停止し、操作を一時停止してください。


### **目標:「ディクテーション セッション」モデル**

単一のトリガーで **「ディクテーション セッション」** が開始されます。これは 3 つのフェーズで構成されます。
1. **スタートアップフェーズ (スピーチ待機中):**
* トリガー後、システムはリスニングを開始します。
* **音声が検出されない**場合、「PRE_RECORDING_TIMEOUT」(例: 12 秒) 経過後にセッション全体が終了します。
2. **アクティブフェーズ (連続ディクテーション):**
* 最初の音声入力が検出されるとすぐに、セッションはアクティブ モードに切り替わります。
* VOSK が一時停止を検出し、テキスト チャンク (文など) を配信するたびに、このチャンクは **直ちに** 処理パイプライン (LanguageTool など) に渡され、テキストとして出力されます。
* 録音はバックグラウンドで**シームレス**に継続され、次の発話を待ちます。
3. **終了フェーズ (セッションの終了):**
* セッション全体は、次の 2 つの条件のいずれかが満たされた場合にのみ終了します。
* ユーザーは「SPEECH_PAUSE_TIMEOUT」の間 (例: 1 ～ 2 秒) 完全に沈黙したままになります。
* ユーザーはトリガーを介してセッションを手動で停止します。
**要約:** 1 つのセッションで複数の即時テキスト出力。セッションは、ユーザーが長い一時停止をするか、手動で終了するまでアクティブのままです。