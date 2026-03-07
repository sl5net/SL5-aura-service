# 自動修正モジュール (クイックルール入力モード)

## 何をするのか

単純な単語 (引用符や Python 構文なし) をマップ ファイルに入力するとき
`FUZZY_MAP_pre.py` と同様に、システムが自動的に有効なルールに変換します。

これは新しいルールを作成する最も速い方法です。形式を覚える必要はありません。

＃＃ 例

これを「FUZZY_MAP_pre.py」に入力します。

```
oma
```

自動修正モジュールが「NameError」を検出しました（裸の言葉、有効な Python ではありません）
ファイルは自動的に次のように変換されます。

```python
# config/maps/.../de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('oma', 'oma'),
]
```

次に、実際に必要なものに合わせてルールを編集します。

```python
('Oma', 'oma'),              # capitalize
('Großmutter', 'oma'),       # synonym
('Thomas Müller', 'thomas'), # from a phone book
```

## 仕組み

モジュール「scripts/py/func/auto_fix_module.py」が自動的にトリガーされます
Aura がマップファイルのロード中に「NameError」を検出したとき。

すると、次のようになります。
1. 正しいファイルパスヘッダーを追加します。
2. 欠落している場合は「import re」を追加します
3. `FUZZY_MAP_pre = [` リスト定義を追加します
4. 裸の単語を `('word', 'word'),` タプルに変換します
5. `]`でリストを閉じます

## ルールと制限

- **1KB** より小さいファイルでのみ動作します (安全制限)
- のみに適用されます: `FUZZY_MAP.py`、`FUZZY_MAP_pre.py`、`PUNCTUATION_MAP.py`
- ファイルは有効な言語フォルダー内にある必要があります (例: `de-DE/`)
- 一度に複数の単語を入力できます (例: 電話帳リストから)

## `# too<-from` コメント

このコメントは、ルールの方向を思い出させるために自動的に追加されます。

```
too <- from
```

意味: **出力** (も) ← **入力** (から)。交換が先です。

`PUNCTUATION_MAP.py` の場合、方向は逆になります: `# from->too`

## リストからの一括入力

複数の単語を一度に貼り付けることができます。

```
thomas
maria
berlin
```

それぞれの裸の単語が独自のルールになります。

```python
('thomas', 'thomas'),
('maria', 'maria'),
('berlin', 'berlin'),
```

次に、必要に応じて各置換を編集します。

## ファイル: `scripts/py/func/auto_fix_module.py`