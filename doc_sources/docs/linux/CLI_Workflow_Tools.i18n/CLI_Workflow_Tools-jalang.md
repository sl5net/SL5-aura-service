# CLI ワークフロー ツール インストール ガイド

パス ナビゲーター プラグインの一部のアクションは、外部コマンド ライン ユーティリティに依存して、あいまい検索の実行、ファイルのリスト表示、およびクリップボードの操作を行います。これらのツールがない場合は、システム コンソールに警告が表示されます。

以下は、サポートされている各オペレーティング システムのインストール手順です。

## 必要なユーティリティ

* **`fzf`**: 汎用コマンドラインファジーファインダー。
* **`find`** (または `fd`): 標準のファイル検索ユーティリティ。
* **クリップボード ツール**: 出力をシステムのクリップボードに直接パイプするために使用されます。
* **Linux:** `xclip` (X11 環境が必要)。
* **macOS:** `pbcopy` (プリインストール)。
* **Windows:** `clip` (プリインストール)。
* **`file`**: 完全な端末プレビューのファイル タイプを決定します。

---

## インストール手順

### 1. Linux (Arch / Manjaro)
システムは Manjaro 上で実行されるため、「pacman」を使用して必要なパッケージをインストールできます。

```bash
sudo pacman -S fzf findutils xclip file
```

### 2. Linux (Debian / Ubuntu / Mint)
Debian ベースのシステムでは、「apt」を使用します。

```bash
sudo apt update
sudo apt install fzf findutils xclip file
```

### 3. macOS
[Homebrew](https://brew.sh/) パッケージ マネージャーを使用して、不足しているツールをインストールします。

```bash
brew install fzf findutils
# Note: 'pbcopy' and 'file' are native on macOS.
```

### 4. 窓
Windows を使用している場合は、[Scoop](https://scoop.sh/) または [Winget](https://github.com/microsoft/winget-cli) 経由で「fzf」をインストールすることをお勧めします。

```powershell
# Using Winget
winget install junegunn.fzf

# Using Scoop
scoop install fzf
```
__CODE_BLOCK_4__