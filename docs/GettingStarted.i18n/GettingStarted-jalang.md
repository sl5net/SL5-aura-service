# SL5 Aura の入門

> **前提条件:** セットアップ スクリプトが完了し、ホットキーが設定されている必要があります。
> そうでない場合は、[Installation section in README.md](../../README.i18n/README-jalang.md#installation) を参照してください。

---

## ステップ 1: 最初のディクテーション

1. Aura を起動します (まだ実行していない場合)。
   ```bash
   ./scripts/restart_venv_and_run-server.sh
   ```
起動音を待ちます。これは、Aura の準備ができたことを意味します。

2. 任意のテキスト フィールド (エディタ、ブラウザ、端末) をクリックします。
3. ホットキーを押して、**「Hello World」**と言い、もう一度ホットキーを押します。
4. テキストが表示されるのを確認します。

> **何も起こりませんでしたか?** `log/aura_engine.log` でエラーを確認してください。
> CachyOS/Arch の共通修正: `sudo pacman -S mimalloc`

---

## ステップ 2: 最初のルールを作成する

個人ルールを追加する最も速い方法:

1.「config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py」を開きます。
2. `FUZZY_MAP_pre = [...]` 内にルールを追加します。
   ```python
   ('Hello World', r'hello world', 0, {'flags': re.IGNORECASE})
   #  ^ output        ^ pattern        ^ threshold (ignored for regex)
   ```
3. **保存** — Aura は自動的にリロードされます。再起動は必要ありません。
4. 「hello world」と入力し、それが「Hello World」になるのを確認します。

> ルールの完全なリファレンスについては、「docs/FuzzyMapRuleGuide.md」を参照してください。

### Oma-Modus (初心者向けショートカット)

正規表現をまだ知りませんか?問題ない。

1. サンドボックス内の空の「FUZZY_MAP_pre.py」を開きます。
2. 単純な単語だけを 1 行に記述します (引用符やタプルは含めません)。
   ```
   raspberry
   ```
3. 保存 — 自動修正システムが裸の単語を検出し、自動的に保存します。
それを有効なルール エントリに変換します。
4. その後、置換テキストを手動で編集できます。

これは **Oma-Modus** と呼ばれるもので、何もせずに結果を求めるユーザーのために設計されています。
まず正規表現を学習します。

---

## ステップ 3: 公案で学ぶ

公案は、それぞれが 1 つの概念を教える小さな演習です。
これらは `configmaps/koans deutsch/` および `configmaps/koans english/` に存在します。

ここから始めてください:

|フォルダー |学ぶこと |
|---|---|
| `00_koan_oma-modus` |自動修正、正規表現のない最初のルール |
| `01_koan_erste_schritte` |最初のルール、パイプラインの基本 |
| `02_koan_listen` |リストの操作 |
| `03_koan_schwierige_namen` |認識しにくい名前のあいまい一致 |
| `04_koan_kleine_helfer` |便利なショートカット |

各 koan フォルダーには、コメント付きの例を含む `FUZZY_MAP_pre.py` が含まれています。
ルールのコメントを解除して保存し、トリガー フレーズを指示する - 完了です。

---

## ステップ 4: さらに進む

|何を |どこ |
|---|---|
|完全なルールのリファレンス | `docs/FuzzyMapRuleGuide.md` |
|独自のプラグインを作成する | `docs/CreatingNewPluginModules.md` |
|ルールから Python スクリプトを実行する | `docs/advanced-scripting.md` |
| DEV_MODE + ログフィルターの設定 | `docs/Developer_Guide/dev_mode_setup.md` |
|コンテキスト認識ルール (`only_in_windows`) | `docs/FuzzyMapRuleGuide.md` |