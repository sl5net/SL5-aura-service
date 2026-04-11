# Unmatched トレーニング プラグイン (`1_collect_unmatched_training`)

＃＃ 目的

このプラグインは、認識されない音声入力を自動的に収集し、追加します。
ファジーマップ正規表現の新しいバリアントとして。これにより、システムが「自己訓練」できるようになります。
比類のない認識結果から学習することで、時間をかけて学習します。

## 仕組み

1. 他のルールが一致しない場合、`COLLECT_UNMATCHED` キャッチオール ルールが起動します。
2. `collect_unmatched.py` は、一致したテキストを使用して `on_match_exec` 経由で呼び出されます。
3. 呼び出し元の `FUZZY_MAP_pre.py` 内の正規表現は自動的に拡張されます。

＃＃ 使用法

このキャッチオール ルールをトレーニングしたい `FUZZY_MAP_pre.py` の最後に追加します。
```python
from pathlib import Path
import os
PROJECT_ROOT = Path(os.environ["SL5NET_AURA_PROJECT_ROOT"])

FUZZY_MAP_pre = [
    # 1. Your rule to optimize (result first!)
    ('Blumen orchestrieren',
     r'^(Blumen giesen|Blumen gessen|Blumen essen)$', 100,
     {'flags': re.IGNORECASE}
    ),

    #################################################
    # 2. Activate this rule (place it after the rule you want to optimize)
    (f'{str(__file__)}', r'^(.*)$', 10,
     {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################
]
```

ラベル `f'{str(__file__)}' は、`collect_unmatched.py` に正確にそれを伝えます。
`FUZZY_MAP_pre.py` を更新してください。そのため、ルールはどのプラグインにも移植可能です。

## プラグインを無効にする

十分なトレーニング データを収集したら、次のいずれかの方法で無効にします。

- キャッチオール ルールをコメントアウトする
- フォルダの名前を無効な名前に変更する（スペースを追加するなど）
- `maps` ディレクトリからプラグイン フォルダーを削除する

## ファイル構造
```
1_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Example with catch-all rule
```

＃＃ 注記

プラグインは実行時に `FUZZY_MAP_pre.py` を変更します。更新されたものをコミットする
定期的にファイルを作成して、収集したトレーニング データを保存します。