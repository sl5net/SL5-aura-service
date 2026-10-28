> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../matrix_threema_relay-README.md).*

# Element ↔ Threema ベータ GUI リレー

**Element Desktop**（Matrix）と間でメッセージをミラーリングする小さなデーモン
**Threema ベータ**（Threema デスクトップクライアント）を Linux/X11 で両方を動かすことによって
ユーザーのようにWindowsを操作する：キーボードショートカット、クリップボード、そしていくつかのマウスクリックを使って。

APIなし、トークンなし、追加のPythonライブラリなし。標準のX11コマンドラインツールのみ。

## それがすること

| 方向 | 何が起こるか |
|---|---|
| **Element → Threema** | Element で *あなた* が書いた最後のメッセージが読み込まれ、新しい場合は Threema Beta に貼り付けて送信されます。 |
| **Threema → Element** | 開いているThreemaチャットの最後の*受信*メッセージがコンテキストメニューを使ってコピーされ、新しい場合はElementに貼り付けて送信されます。 |

典型的な使用方法: Elementの部屋に口述または入力する（例えばAuraのように）
音声認識（speech-to-text）でテキストをThreemaチャットに届くようにし、そして見る
Threemaの返信は同じElementルームに表示されます。

両方のウィンドウは開かれており、ログイン済みで、転送したいチャット/ルームを表示している必要があります。

## ループ保護

ネイブイブツーウェイミラーは、すべてのメッセージのバックと永遠にバウンスします。 リレー
短命の歴史(`relay_history.py`)でこれを防ぐ:

1. リレーが転送するテキストは、180秒間送信される**前に記憶されます。
2. この歴史の向こう側にテキストが現れた場合、それは私たち自身です
   echo: 見ているようにマークされますが、**** 再び転送されません。
3. 新しくなった *and* の未知のテキストは、本物メッセージであり、転送されます。

テキストは空白の崩壊と比較されるので、ラインブレイクの違いは
コピー/ペーストはガードを倒さない。 エントリーが死ぬので、送信できます
ウィンドウが渡した後に同じテキスト(例えば "ok")が再び渡されます。

起動時に、各サイドの最後のメッセージは、**baseline** として読み込まれ、
*not*は転送しました。 開始後に到着したメッセージのみが中継されます。

## 要件

- Linux は **X11** で動作します（`echo $XDG_SESSION_TYPE` は `x11` を印刷する必要があります）。Wayland はサポートされていません。
- `xdotool`、`xclip`、`wmctrl`、および `xset`（オプション、スクリーンセーバーを無効にするために使用）
- Element デスクトップ (WM クラス `element.Element`)
- Threema ベータ版（WM クラス `threema beta.Threema Beta`、例えば Flatpak）
  `ch.threema.threema-desktop`)
- プロジェクトの仮想環境での Python 3
- 一度限りのキャリブレーションスクリプト用の`zsh`

## セットアップ:ワンタイムの口径測定

3maベータは、キーボードで操作できない独自のコンテキストメニューを描画します。
そのため、リレーは、相対的な位置でマウスで「メッセージのコピー」をクリックします
三間窓。 それらを一度測定して下さい:

```zsh
scripts/py/func/threema/threema-relay.zsh calibrate
```

スクリプトは3つのマウスの位置を要求し、それぞれにカウントダウン(触れない)
キーボードは、ウィンドウを移動またはサイズ変更しません。

1. **右クリック** 最後の*着信*メッセージ(左側の泡)をクリックし、残します
   メニューを開きます。
2. マウスを移動し、クリックせずに、**"Copy Message"**に移動します。
3. *message 入力欄にマウスを移動**。

結果は`~/.config/threema-relay.conf`で保存されます:

| キー | 意味 |
|---|---|
| `FX` | ウィンドウ幅のずれの水平クリック位置 |
| `BOTTOM` | ウィンドウの一番下端の上の位置、ピクセルをクリック |
| `DX`、`DY` | クリックポイントから「コピーメッセージ」へオフセット |
| `INPUT_FX`、`INPUT_BOTTOM` | メッセージ入力欄の位置 |
| `DELAY_MENU`、`DELAY_COPY` | 秒単位でオプション待ち(デフォルトは0.30/0.20) |

チャットの最後のメッセージとして、新しく受信したメッセージで校正を確認してください:

```zsh
scripts/py/func/threema/threema-relay.zsh test
```

コピーしたテキストを転送せずに印刷します。キャリブレーションはウィンドウに依存します
ジオメトリ：Threemaのウィンドウサイズを大幅に変更した場合は、再度校正してください。

## 使用方法

リポジトリのルートから:

```zsh
PYTHONPATH=. .venv/bin/python3 scripts/py/func/threema/matrix_threema_relay.py
```

オプション：

| オプション | 効果 |
|---|---|
| `--poll SECONDS` | 投票間隔(デフォルト`2.0`) |
| `--no-threema-to-element` | リレーのみエレメント | 三間 |
| `--no-element-enter` | エレメントの入力欄に三間メッセージを貼り付けるが、** 送信しない(安全テストモード) |

`Ctrl+C`で停止します。

最初に推奨される実行:`--no-element-enter`を使用して、Thremaでメッセージを送信
要素の入力フィールドに表示されることを確認し、チェックします。 オプションなしで実行します。

サンプルログ:

```
[INFO] Initial Element baseline: 'Test'
[INFO] Initial Threema baseline: 'kaa'
[INFO] New Element message -> Threema: 'Hallo Welt'
[INFO] New Threema message -> Element: 'müsli'
[INFO] Element shows our own relayed text - not sending back.
```

## 使い方

```
every poll interval
├─ Element:  focus window (wmctrl) → Up, Ctrl+A, Ctrl+C, Escape (xdotool) → read clipboard (xclip)
│            new + unknown  → paste into Threema + Return, remember text
│            new + known    → echo, ignore
└─ Threema:  focus window → right-click last incoming bubble → click "Copy Message"
                          → click input field (restores focus) → read clipboard
             new + unknown  → paste into Element (+ Return), remember text
             new + known    → echo, ignore
```

- *Up* は Element のコンポーザーで最後のメッセージを編集します。 *Ctrl+A / Ctrl+C* コピー
  *Escape* は編集モードを残します。 そのため、**your Own** 最後の要素のみ
  3maにメッセージが中継されます。
- 3ma の場合、**sentinel 文字列** は最初にクリップボードに入れられます。 それでも
  その後、何もコピーされていない(たとえば、自分のメッセージは、
  最後の1つと、クリックがバブルなしでヒットし、試みは無視されます。

## ファイル

| ファイル | 目的 |
|---|---|
| `matrix_threema_relay.py` | 主要ループ、CLI、決定ロジック(`classify_candidate`) |
| `read_last_element_message.py` | 要素の最後のメッセージ |
| `send_to_threema_window.py` | テキストを三間ベータへ貼り付け |
| `read_last_threema_message.py` | 3maの最後の着信メッセージ、負荷口径測定 |
| `send_to_element_window.py` | テキストを要素に貼り付ける |
| `relay_history.py` | ループ保護 |
| `threema-relay.zsh` | 校正・手動テストツール(`calibrate`、`test`) |
| `test_threema_relay.py` | ユニットテスト(X11不要) |

テストを実行します。

```zsh
PYTHONPATH=. .venv/bin/python3 -m unittest scripts.py.func.threema.test_threema_relay
```

## 制限事項

- **リレーはマウスおよびキーボードの焦点を使用します。 メニュー 各ポールの間に三間と
  要素のWindowsは集中され、マウスは簡単にジャンプします(それは元通りです)。 しない
  poll が実行される間、またはより長い `--poll` を使用します。
- すべての投票でクリップボードを上書きします。
- **スリーマで最後のメッセージ:** あなた自身のメッセージがスリーマで最後のとき
  チャット、見られない直前に到着した返信。
- **最後のメッセージのみ**は、投票ごとに読み込まれます。 複数のメッセージが1つ以内に届いた場合
  間隔は、最新のリレーのみです。
- **テキストのみ。** 画像、ファイル、反応、編集は中継されません。
- **ワンチャットペア。** 各ウィンドウでどのチャット・ルームが開きますか。
- **エレメントの入力欄にドラフト**は、次の貼り付けと組み合わせます。
  メッセージ
- **X11のみ。** Waylandブロックの合成入力とウィンドウフォーカスの変更。
- リレーは、X11 のスクリーンセーバーと DPMS を最初から無効にします (`xset s off -dpms`);
  再利用可能なか、再度ログインするまで、彼らはオフに滞在します。

## トラブルシューティング

| 症状 | 原因・修正 |
|---|---|
| `Threema window ... not found` | `xdotool search --class "Threema Beta"` と `xprop WM_CLASS` のチェックをします |
| `Nothing copied`/no 3ma → 要素 | `calibrate` を再実行し、`test` を実行し、最後のメッセージとして受信メッセージを. スピードマシンの設定で`DELAY_MENU`/`DELAY_COPY`を上げます。 |
| テキストは三間に到着しますが、送信されていません | 入力欄は焦点を合わせていません。校正から`INPUT_FX`/`INPUT_BOTTOM`を確認してください。 |
| 要素に三枚のテキストが表示されますが、送信されていません | `--no-element-enter` より中継が開始されました。 |
| 設定で`0,9353`などの数値決定 | ドイツのロケールの古いスクリプト版で書かれています。 Python コードはそれらを受け入れます。現在のスクリプトで再びキャリブレーションして、ドットを記述します。 お問い合わせ
