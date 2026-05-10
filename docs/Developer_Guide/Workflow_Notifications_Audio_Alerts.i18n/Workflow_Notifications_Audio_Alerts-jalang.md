# ワークフロー通知 (音声アラート)

生産性を向上させるために、コードをプッシュし、GitHub Actions ワークフローが完了するとすぐに自動的にアラートを (音声またはサウンド経由で) 通知するローカル Git エイリアスを構成できます。これにより、「GitHub 監視疲れ」を防ぎ、他のタスクに集中できるようになります。

### 前提条件

**GitHub CLI** と、テキスト読み上げエンジンまたはサウンド プレーヤーがシステムにインストールされている必要があります。

**Manjaro / Arch Linux の場合:**
```bash
sudo pacman -S github-cli espeak-ng
gh auth login
```

＃＃＃ 設定

ターミナルで次のコマンドを実行して、「pushsound」というグローバル Git エイリアスを作成します。

```bash
git config --global alias.pushsound '!git push && sleep 3 && gh run watch $(gh run list --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "all github workflow has finished"'
```

＃＃＃ 使用法

「git Push」の代わりに、単に次を実行します。
```bash
git pushsound
```
ターミナルはワークフローが完了するのを待ってから、*「すべての github ワークフローが終了しました」* とアナウンスします。

---

### カスタマイズと代替案

好みに応じて、別のエイリアス名または通知方法を使用することもできます。

#### 1. 推奨されるエイリアス名
「pushsound」が長すぎて入力できない場合は、次の代替手段を検討してください。
* `git pw` (プッシュ & ウォッチ) — **速度の点で推奨。**
* `git sync` (プッシュして「青信号」を待つことを意味します)
* `git Palert` (プッシュアラート)

#### 2. 通知スタイル
「espeak-ng」の部分を他のタイプのアラートに置き換えることができます。

* **デスクトップ通知:**
`... && 通知送信 "GitHub アクション" "ワークフローが完了しました!"`
* **システムサウンド (ベル):**
`... && paplay /usr/share/sounds/freedesktop/stereo/complete.oga`
* **組み合わせ (サウンド + 音声):**
`... && paplay /usr/share/sounds/freedesktop/stereo/message.oga && espeak-ng "完了"`

#### 3. アドバンスト: チームセーフ バージョン
複数の開発者が同じリポジトリに同時にプッシュしている場合、デフォルトのコマンドが間違った実行を追跡する可能性があります。自分の現在のブランチのみを監視するには、この「ブランチセーフ」バージョンを使用します。

```bash
git config --global alias.pw '!git push && sleep 3 && gh run watch $(gh run list --branch $(git branch --show-current) --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "Workflow finished"'

git config --global alias.pushsound '!git push && sleep 3 && (gh run watch $(gh run list --limit 1 --json databaseId --jq ".[0].databaseId") --exit-status && espeak-ng "workflow successful" || espeak-ng "workflow failed")'

```

### トラブルシューティング
* **「実行が見つかりませんでした」:** GitHub がプッシュを登録してワークフローを開始するのに時間がかかるため、「スリープ 3」を含めます。接続が非常に遅い場合は、これを「スリープ 5」に増やす必要があるかもしれません。
* **ターミナルのビープ音:** `espeak-ng` が機能しない場合は、音声がミュートになっていないこと、およびパッケージが正しくインストールされていることを確認してください。