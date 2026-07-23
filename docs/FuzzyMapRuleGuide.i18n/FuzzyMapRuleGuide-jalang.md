# FUZZY_MAP ルールガイド

## ルールの形式

```python
('replacement', r'regex_pattern', threshold, {'command_flags': re.IGNORECASE})
```

|ポジション |名前 |説明 |
|---|---|---|
| 1 |交換 |ルールが | に一致した後の出力テキスト
| 2 |パターン |照合する正規表現またはあいまい文字列 |
| 3 |しきい値 |正規表現ルールの場合: 無視されます。ファジー ルールの場合: 最小一致スコア (0 ～ 100) |
| 4 |オプション |オプションの辞書 (下記の「オプションのリファレンス」を参照)。デフォルトでは「0」を使用するか省略します。
### 未加工の置換
デフォルト (`False`) では、置換文字列は Python の `re.sub()` によって処理されます。これは、キャプチャされたグループを挿入するための `\1` や `\2` などの正規表現後方参照の使用をサポートします (例: `(r'\1', r'(\d)\s+(?=\d)', 95)`)。
置換が複数行の文字列であるか、エスケープされていないバックスラッシュが含まれている場合 (コード テンプレートやパスなど)、そのままの状態で保存する必要がある場合は、オプション ディクショナリで `'raw_replacement': True` を有効にします。
```python
(System_Instructions, r'^(system instructions)$', 10, {'command_flags': re.IGNORECASE, 'raw_replacement': True})
```

### 利用可能なユーザー構成可能なオプション:

* **`command_flags`** (整数): パターンのコンパイル中に使用される正規表現フラグ。
*例:* `{'command_flags': re.IGNORECASE}`
* **`raw_replacement`** (ブール値): `True` の場合、置換テキストは純粋な文字列リテラルとして扱われ、Python の `re.sub` バックスラッシュ解析によってバイパスされます。複数行のプロンプトまたはエスケープされていないバックスラッシュ (`\`) を含む文字列の場合に重要です。
*例:* `{'raw_replacement': True}`
* **`cache`** (ブール値): AURA 結果キャッシュを切り替えます。動的出力 (現在の時刻、ランダムなジョークなど) を生成するルールの場合は「False」に設定すると、一致するたびに新しく評価されるようになります。
*例:* `{'キャッシュ': False}`
* **`skip_list`** (文字列のリスト): このルールが一致した場合にスキップする後処理パイプライン モジュールを指定します。
*例:* `{'skip_list': ['LanguageTool']}` (文法チェックをスキップします)
* **`only_in_windows`** (文字列/正規表現): アクティブなウィンドウのタイトルがこのパターンに一致する場合にのみトリガーされるようにルールを制限します。
*例:* `{'only_in_windows': 'google ai スタジオ'}`
* **`exclude_windows`** (文字列/正規表現): アクティブなウィンドウのタイトルがこのパターンに一致する場合にルールがトリガーされないようにします。
*例:* `{'exclude_windows': 'ターミナル'}`
* **`on_match_exec`** (パス/文字列オブジェクトのリスト): このルールが一致した場合に実行されるスクリプト/プラグインへのパス (キャッチオール ルールとフォールバック ルールで頻繁に使用されます)。
*例:* `{'on_match_exec': [PROJECT_ROOT / 'scripts' / 'custom_action.py']}`

## パイプライン ロジック
- ルールは **トップダウン** で処理されます


## パイプライン ロジック

- ルールは **トップダウン** で処理されます
- **すべて**の一致ルールが適用されます (累積)
- **完全一致** (`^...$`) はパイプラインを即座に停止します
- 以前のルールが後のルールより優先されます

## 一般的なパターン

### 単一の単語 (単語境界) に一致します
```python
('Python', r'\bpython\b', 0, {'command_flags': re.IGNORECASE})
```

### 複数のバリアントを照合する
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'command_flags': re.IGNORECASE})
```

### Fullmatch – パイプラインを停止します
```python
('hello koan', r'^.*$', 0, {'command_flags': re.IGNORECASE})
```
⚠️ これは **すべて** に一致します。パイプラインはここで止まります。以前のルールが引き続き優先されます。

### 入力の先頭と一致する
```python
('Note: ', r'^notiz\b', 0, {'command_flags': re.IGNORECASE})
```

### フレーズと完全に一致
```python
('New York', r'\bnew york\b', 0, {'command_flags': re.IGNORECASE})
```

## ファイルの場所

|ファイル |フェーズ |説明 |
|---|---|---|
| `FUZZY_MAP_pre.py` |事前言語ツール |スペルチェックの前に適用される |
| `FUZZY_MAP.py` |ポスト言語ツール |スペルチェック後に適用される |
| `PUNCTUATION_MAP.py` |事前言語ツール |句読点の規則 |

## ヒント

- **一般**ルールの前に**特定**ルールを置く
- `^...$` 完全一致は、以降のすべての処理を停止したい場合にのみ使用してください。
- `FUZZY_MAP_pre.py` はスペルチェック前の修正に最適です
- Aura コンソールの「テスト入力」を使用してルールをテストします。
- バックアップは `.peter_backup` として自動的に作成されます

## 例

```python
FUZZY_MAP_pre = [
    # Correct a common STT mistake
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'command_flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'command_flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'command_flags': re.IGNORECASE}),
]
```

## 最初のルール — ステップバイステップ

1.「config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py」を開きます。
2. `FUZZY_MAP_pre = [...]` 内にルールを追加します。
3. 保存 — Aura は自動的にリロードされます。再起動は必要ありません。
4. トリガーフレーズを口述し、それが発火するのを観察します


## 推奨されるファイル構造

ルールを長いコメント ブロックの前**に置きます。
```python
# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re  # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('My Rule', r'my rule', 0, {'command_flags': re.IGNORECASE}),
]
# ============================================================
# Longer explanations, task descriptions, notes...
# can be as long as needed — they go AFTER the rules.
# ============================================================
```

**なぜですか?** Aura の自動修正は、ファイルの最初の ~1KB のみをスキャンします。
ルールが長いヘッダーの後に表示される場合、自動修正はルールを検索または修復できません。
1 行目のパス コメントも推奨されます。これは人間がファイルをすばやく識別するのに役立ちます。