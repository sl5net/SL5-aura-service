# 1-Click インストーラー (ゼロセットアップ)

ワンクリックで **Aura** をマシン上で起動して実行できます。プログラミングの知識、ターミナル コマンド、または手動の Python セットアップは必要ありません。

---

## 前提条件なし

以下は**必要ありません**。
- Pythonがプリインストールされています
- Git またはコード リポジトリ
- コマンドラインまたはターミナルのエクスペリエンス

---

## クイックスタート

### 方法 1: Web ワンライナー (Linux / macOS で最も高速かつ推奨)
手動でのファイル処理を最大 30 秒節約し、端末ですぐに開始できます。

**Linux および macOS:**
#### Web ワンライナー CodeBerg
```bash
curl -sSL https://codeberg.org/seeh/SL5-aura-service/raw/branch/master/web_install.sh | bash
```
または
#### Web ワンライナー GitHub
```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

**Windows (PowerShell):**
#### Web ワンライナー CodeBerg
# テストされていません - Windows の場合は方法 2 (スタンドアロン バイナリ) を使用してください
```bash
irm https://codeberg.org/seeh/SL5-aura-service/raw/branch/master/web_install.sh | iex
```
または
#### Web ワンライナー github
```bash
irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

方法 2: スタンドアロン バイナリ (Windows およびデスクトップのクリック)

### 2.1 インストーラーをダウンロードする
[最新の GitHub リリース] から、オペレーティング システムに一致する単一のインストーラー ファイルをダウンロードします。

- **Windows:** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **Linux:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


＃＃＃２．２．インストーラーを実行する

aura-installer-windows.exe.zip の名前を aura-installer-windows.exe に変更します

ダウンロードしたファイルをダブルクリックします。セットアップ画面が表示され、自動的に環境が準備されます。

＃＃＃２．３．ディクテーションを開始する
完了すると、Aura はデスクトップにショートカットを作成し、すぐにリスニングを開始します。

---

## 自動的に何が起こるのでしょうか?

インストーラーを実行すると、Aura は自動的に次のことを行います。
- ローカルのプライベート音声認識エンジンを構成します。
- デフォルトの音声モデルをダウンロードします。
- 必要なすべてのシステム ショートカットとデスクトップ ランチャーをセットアップします。

---

## インストールの詳細と要件

- **インストール時間:** 約 2 ～ 3 分。
- **必要なディスク容量:** 最小 ~1.5 GB (選択した言語モデルに応じて最大 2.5 GB)。
- **インストール ディレクトリ:**
- **Linux および macOS:** `~/opt/sl5-aura-service`
- **Windows:** `%LOCALAPPDATA%\sl5-aura-service`

---

## 次のステップ

- **おばあちゃんモード:** ルール ファイルに 1 つの単語を入力すると、Aura がルールを自動作成するのを確認します。
- **Koans で学ぶ:** [Getting Started](../GettingStarted.i18n/GettingStarted-jalang.md) の概念をステップバイステップで学習します。