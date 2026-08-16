# 注: type_watcher.sh でキーがスタックする問題 (dotool)

＃＃ 症状
Manjaro の再起動直後、「sl5net Aura」後の最初のディクテーション時
自動で開始され、単一の文字がスタックして無限に繰り返される
（例：「n」を何百回も繰り返す）トリガーキーが押されるまで
手動による回避策として再度実行します。

2026 年 7 月 21 日 ~09:44 (火) に 1 回観測され、テキスト: 「Die Ideen niemand wird」
mehr gefragt, aber es soll trotzdem genauso sein wie...nnnnn..."。

## タイムライン (ログで証明)
- 09:29:17 - `type_watcher.sh` が開始されました (log/type_watcher.log)
- 09:41:56 - ディクテーション「ideen niemand wird mehr gefragt...」を受信しました
(log/aura_engine.log、スレッド-13/14)
- 09:42:03 - テキストの処理が終了しました (「最高のファジー スコア:0%」)、
おそらく `tts_output_*.txt` ファイルに書き込まれます
- ~09:42:04-09:42:09 - `type_watcher.sh` がクラッシュしました (推測: ウォッチドッグ
ポーリング間隔は 5 秒です。以下を参照してください)
- 09:42:09 - ウォッチドッグ ログ (log/type_watcher_keep_alive.log):
「WATCHDOG: 'type_watcher.sh' が実行されていません。今すぐ開始します。」
- 09:42:13 - `type_watcher.sh` が再起動されました (log/type_watcher.log)
- 「ideen niemand...」ファイルの「typed content of ...」エントリはありませんでした。
log/type_watcher.log で見つかったもの — その特定のタイプ
テキストは完了/記録されませんでした。

## 根本原因のステータス
- 確認: `type_watcher.sh` がテキストの終了間でクラッシュしました
処理 (09:42:03) と、それが実行されていないことを検出するウォッチドッグ
(09:42:09)。ウォッチドッグ (`type_watcher_keep_alive.sh`) は kill のみを行います
そして、構成ファイルのタイムスタンプの変更 (`ts1`/`ts2`、
このインシデントでは変更されていないことが確認されました）、または次の場合に自動的に再起動します
`pgrep -f "type_watcher.sh"` はプロセスを見つけません。つまり、これは非常に困難でした。
おそらく外部からの破壊ではなく、自己衝突です。
- 仮説 (証明されていません): `set -euo Pipefail` (type_watcher.sh 行 5)
これにより、スクリプト内のゼロ以外の終了コードでスクリプトが終了しました。
おそらく `do_type()` の `dotool` パイプ (125 行目) が
中流。 「dotool」へのストリーミング中に bash プロセスが停止した場合、
別個の `dotoold` デーモン (独立して実行され続ける)
一致する「up」がないキーを「down」状態のままにすることができます。
受信すると、OS レベルのキーリピートが発生します。
- まだ証明されていません: ゼロ以外の原因となった正確なコマンド/ライン
「set -euo Pipefail」で終了します。クラッシュしたものからの標準エラー出力はありません
`type_watcher.sh` プロセスがキャプチャされました (ウォッチドッグがそれを呼び出します)
出力リダイレクトなし、`type_watcher_keep_alive.sh` 行 79)。
- 影響を受けるキーは、異なる文字間で常に同じ文字であるとは限りませんでした。
このバグの発生 (ユーザーレポート: 以前は "t" も同様でした)。

## すでに調査され、除外されています
- 構成変更による再起動ではありません (ユーザー: config によって確認されました)
変更されず、`ts1_old != ts1_new` チェックは「構成が変更されました」とログに記録されます)。
- `type_watcher.sh` の自動起動が重複していないこと
それ自体 (クラッシュの前に「Hello from Watcher」エントリが 1 つだけありました)。
- `do_type()` の `dotool type` 呼び出しは呼び出しごとにアトミックであり、
それ自体は文字ごとのキーを下/上に送信しません - `type_watcher.sh` を除外します
通常時のスタックキーの直接のソースとしてのアプリケーションロジック
(クラッシュしない) 操作。

## 修正はすでに適用されています (根本原因の修正ではなくフォールバック/軽減)
「type_watcher.sh」の「cleanup()」と「do_cleanup()」の両方
「keep-keys-up.sh」は以前は修飾キー (shift、ctrl、
alt など) `dotool`/`xdotool` 経由。これは行き詰まった常連には何の役にも立ちませんでした
キー (文字、数字、句読点)。

- `type_watcher.sh`: `cleanup()` が `dotool key <name>:up` を送信するようになりました。
すべての文字、数字、および一般的な句読点/空白キーではなく、
ただの修飾子。
- `type_watcher.sh`: `INPUT_METHOD` は検出後にエクスポートされるようになりました。
他のスクリプトは、どのバックエンド (`dotool` / `xdotool`) がアクティブであるかを確認できます。
- `keep-keys-up.sh`: `do_cleanup()` は `dotool` ブランチを取得しました (
`keyup` 動詞、キーごとの遅延なし、パフォーマンスのため）の場合にのみアクティブになります
`INPUT_METHOD=dotool`、既存の `xdotool keyup` 呼び出しをミラーリングします
修飾子用。

これは、`type_watcher.sh` の根本的なクラッシュを修正するものではありません。それだけ
クラッシュが再び発生した場合に、固着したキーが確実に解放されるようにします。
次のクリーンアップ パス (各 `do_type()` の後に呼び出される `--cleanup`、および
を繰り返す代わりに、`trap cleanup EXIT INT TERM` ハンドラーを介して)
手動でトリガーキーを押すまで無期限に続きます。

## これが再び発生した場合の次の手順
- クラッシュ時に「type_watcher.sh」の標準エラー出力をキャプチャします。現在
`type_watcher_keep_alive.sh` の 79 行目はリダイレクトなしで呼び出しています。
bash エラー メッセージは失われます (ウォッチドッグ自身に送られます)
stdout/stderr、自動起動メカニズムによって指示される場所）。
- デバッグ モードを検討してください。 `bash -x スクリプト/type_watcher/type_watcher.sh
2>> log/type_watcher_debug.log`、次のような環境変数を介して切り替えられます。
`TYPE_WATCHER_DEBUG=1`、次のエラー行を正確にキャプチャします。
クラッシュ。
- Manjaro 起動時に「type_watcher_keep_alive.sh」が何が始まるかを確認する

その stdout/stderr はどこでもキャプチャされます。
- 再現可能な場合は、クラッシュが次の要因と相関するかどうかをテストします。
`dotoold` はブート直後にまだ初期化中です (`sleep 0.1` を参照)
type_watcher.sh の 8 行目と `dotoold` 起動ループの行
102-110）。