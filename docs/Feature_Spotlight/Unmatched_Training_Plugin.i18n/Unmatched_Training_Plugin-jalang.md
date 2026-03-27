# Unmatched トレーニング プラグイン (`a_collect_unmatched_training`)

＃＃ 目的

このプラグインは、認識されない音声入力を自動的に収集し、追加します。
ファジーマップ正規表現の新しいバリアントとして。これにより、システムが「自己訓練」できるようになります。
比類のない認識結果から学習することで、時間をかけて学習します。

## 仕組み

1. `FUZZY_MAP_pre.py` の `COLLECT_UNMATCHED` キャッチオール ルールは、次の場合に起動します。
音声入力に一致するルールは他にありませんでした。
2. `collect_unmatched.py` は、一致したテキストを使用して `on_match_exec` 経由で呼び出されます。
3. テキストが `unmatched_list.txt` (パイプ区切り) に追加されます。
4. `FUZZY_MAP_pre.py` の正規表現は、新しいバリアントで自動的に拡張されます。

## プラグインを無効にする

十分なトレーニング データを収集したら、次のいずれかの方法でこのプラグインを無効にします。

- Aura 設定で無効化する
- `maps` ディレクトリからプラグイン フォルダーを削除する
- 無効な名前でフォルダーの名前を変更します (例: スペースを追加します: `a_collect unmatched_training`)

## ファイル構造
```
a_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Catch-all rule + growing regex variants
```

＃＃ 注記

プラグインは実行時に `FUZZY_MAP_pre.py` を変更します。必ずコミットしてください
収集されたトレーニング データを保存するためにファイルを定期的に更新します。