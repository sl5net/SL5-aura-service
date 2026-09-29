> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../uebergabeprotokoll_z_fallback_llm_20260929_1430.md).*

# 引き渡しプロトコル: z_fallback_llm、CLI入力はジョークを返さない

状況: 2026-09-29

## 1- タスク(理解していない、まだ「はい」で確認されていない)

実際の状態:CLIの入力は正確に「コンピュータは正確に2ジョークを指示します」です。 冗談はありません。

ターゲットの状態: LLM 応答は、ログファイルではなく、コンソールに直接表示されます。

タスクの一部ではない:ログを再構築し、ログ行を短縮または拡張し、キャッシュの動作を変更します。 キャッシュバイパス(入力中の「ジョーク」)は、この方法で意図的に選択されます。

フォロワーは、まずこの理解とあなたとあなたの「はい」を待つ必要があります。

##2 環境

Manjaro Linux, ZSH, ブランチ機能/フォールバック-llm-lazy-install.

http://localhost:11434 (Binary /usr/bin/ollama) で Ollama が利用できます。 利用可能なモデル: llama3.2:latest、qwen3:8b。

モデル llama3.2、ストリーム:false、num 予測:100 とストップワード の curl による Ollama のテストは、有効な応答を提供します(コンピューターが医者に行くのはなぜですか?) ウイルスが起きたから! Ollama、モデル名、単語の停止、トークンの制限は原因ではありません。 テストプロンプトは ollama.py (システムロールなし、グラデーションと aura suffix) を尋ねるから実際のプロンプトよりも短くなりました。

構成:

```
config/settings_local.py
```

キー: PLUGINS ENABLED = {"z フォールバック llm": 1}. DynamicSettings().PLUGINS ENABLED.get("z フォールバック llm", False) 経由でアクセスします。

既存のパッケージのインストーラ:

```
scripts/py/func/ensure_package.py
```

#3 チェーンシーケンス(コードセクションから検証)

ルール:

```
config/maps/plugins/z_fallback_llm/de-DE/FUZZY_MAP_pre.py
```

ルール1には優先10があり、`{aura1}`とモードワード(通常、遅い、フロー、遅い、正確、徹底)が必要です。 ルール2は、100を優先し、オーラ、オーロラ、ララ、ドラ、時代、ハリラ、プロラ、またはコンピュータのいずれかのトリガーのいずれかが必要です。 どちらの呼び出しも ollama.py を尋ねます。 Firefox、Chrome、Brave、Elementなどのウィンドウを除外します。

デザイン:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

`execute()` は、最後に Regex のグループを入力して小さにします。 入力中の "joke" の場合、`bypass_cache = True` が設定されていると、キャッシュチェックはスキップされます。 これは、モデルの llama3.2 で Ollama リクエストに従っています。 タイムアウトは90秒です。 Ollama リクエストなしで早期返送は、空の入力(「聞き取りなし」)、`check_static_guardrails()` で「すべてを忘れる」、インスタント単語「即時」、「高速」で利用できます。

CLI のリターン:

```
scripts/py/service_api.py
```

関数は、最新の出力ファイルを読み、`status`、`result_text`、`input_text` で dict を返します。 ログライン「API-CLI-Call: Finished」は入力と結果を20文字に減らします。 純正ログの短縮とデータの短縮はできません。

#4 - CLI入力のログを保存

ログは`reload_performed`と「API-CLI-Call: Finished」のみです。 インプット="...コンピュータの正確" 結果="コンピュータ正確" `execute()`の全ての行が欠落しています(「入力なし」、「キャッシュバイパスなし」、「無修正AI回答」はありません)。

これは、`execute()`が実行されていないことを証明しません。

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

`mode='w'` で FileHandler を開きます。 要求 ollama.log ファイルは、各インポートの `utils` によって上書きされます。 `log_debug`は、メインプログラムのコンソールでstdout、すなわち書きます。

#5 質問を開く(未使用)

1- `execute()` は、CLI の入力時に全て実行されますか?
2- ルールマッチ、ルール1、ルール2、またはどれ?
3- CLI クライアントはコンソールで `result_text` を出力しますか?
4- 出力ファイルには、入力または応答だけが含まれていますか? 入力と結果の最初の20文字は同一で、表示されません。
5- テキストをドロップするために使用する正確なCLI呼び出しは何ですか? 未発表です。

## 6- 棄却された仮説

1- 入力は短縮されて届くわけではなく、それはログでの20文字の短縮だけでした。
2- Ollama、ストップワード、そして num_predict は原因ではありません。
3- キャッシュは「witz」でバイパスされているため、原因ではありません。

#7- タスクの外でエラーを見つけました(タスクなしで何かを変更しないでください)

1 ファイル:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

`if not raw_text:` 以降、`response = answer_for_all_fallback` が設定されます。 次の行は`clean_text_for_typing(raw_text)`で上書きします。 空のオラマの回答で、回答は空のままです。 同様に、`response.replace('sl5_config.py', ...)`と`response.replace(' sl5_record_trigger.py ', ...)`は結果が割り当てられていないため効果がありません。

2 ファイル:

```
config/maps/plugins/internals/de-DE/aura_constants.py
```

`Overlay` によると、`|` が見つからない場合、`OverlayOrange` が作成されます。 また、`_variants`には「コンピュータ」という単語は含まれていません。 ルール1は「コンピュータを正確に...」と一致できません。

3 ファイル:

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

`mode='w'`は、すべてのインポートでログを上書きします。

## 8- 次のステップ（あなたの「はい」の後でのみ）

ステップA: プロンプト記号なしで、CLI呼び出しをあなたから尋ねる。

ステップB：`result_text`の処理を見つける：

```
tools/search.sh "result_text" .
```

ステップC: 入力後にコンソール出力を確認する。そのために、メインプログラムのコンソールから完全なテキストをあなたに要求する。

ステップD：その後で初めて変更を提案すること、前後形式のみで。

##9- 後継者が遵守しなければならない作業規則

1-ドイツ語でのコミュニケーション コード、コメント、ログ、識別子のみ、コードのブロックでも。
2- あなたの出力から証拠なしでシステムの状態についての声明無し。 再構築はしない。
3- 新しいタスク:まず理解を記述し、 "yes" を待ちます。
4-「リポジトリにアクセスできない」設定はありません。
5- -i、-E、-w オプションでツール/search.sh 経由でのみリポジトリ検索。
6- エラーの場合、最初のフルトレースバックを取得します。
7- コマンドとファイルパスは、最後に句読なし、それぞれ自分の行にあります。
8- フォーマットの数値化 1-, 2-, 3-.
9- コードは、周囲の関数コードなしで前後のフォーマットで変更された行としてのみ変更します。
10- コードのブロックで主要なインデントを持つ Python コードはありません。代わりに、インデントのない小さな関数。
11- 絶対パス、ユーザー固有のパス、ファイルパスなしで行番号はありません。
12- 充填セットなし, 感情的な調子なし, 約 1400 応答あたりの文字 ターゲットとして.
13- すでに実行したアクションを処理します。
14- 出力をコピーすると、プロンプトサインをコピーしないと、それ以外の場合はコード127が作成されます。
./tools/find-nearest-commit.sh "2026-07-28 17:00"の日付と時刻を見つけるために15コミット
