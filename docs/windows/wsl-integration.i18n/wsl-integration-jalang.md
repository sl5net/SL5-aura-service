# WSL (Linux 用 Windows サブシステム) の統合

WSL を使用すると、完全な Linux 環境を Windows 上で直接実行できます。セットアップが完了すると、STT シェル統合は **Linux Bash または Zsh ガイドと同様に動作します**。シェル関数自体に Windows 固有の調整を行う必要はありません。

> **推奨対象者:** Linux ターミナルに慣れている、または開発作業のために WSL がすでにインストールされている Windows ユーザー。 WSL は、最も忠実なエクスペリエンスと互換性の侵害を最小限に抑えます。

## 前提条件

### WSL をインストールする (1 回限りのセットアップ)

PowerShell または CMD を **管理者** として開き、以下を実行します。

```powershell
wsl --install
```

これにより、デフォルトで WSL2 が Ubuntu とともにインストールされます。プロンプトが表示されたらマシンを再起動します。

特定のディストリビューションをインストールするには:

```powershell
wsl --install -d Ubuntu-24.04
# or
wsl --install -d Debian
```

利用可能なすべてのディストリビューションをリストします。

```powershell
wsl --list --online
```

### WSL バージョンを確認する

```powershell
wsl --list --verbose
```

「VERSION」列に「2」が表示されていることを確認してください。 「1」と表示されている場合は、次のようにアップグレードします。

```powershell
wsl --set-version <DistroName> 2
```

## WSL 内でのシェルの統合

WSL が実行されたら、Linux ターミナルを開き、希望するシェルの **Linux シェル ガイド**に従います。

|シェル |ガイド |
|------|------|
| Bash (WSL のデフォルト) | [bash-integration.md](../../linux/bash-integration.i18n/bash-integration-jalang.md) |
|ズシュ | [zsh-integration.md](../../linux/zsh-integration.i18n/zsh-integration-jalang.md) |
|魚 | [fish-integration.md](../../linux/fish-integration.i18n/fish-integration-jalang.md) |
|キシュ | [ksh-integration.md](../../linux/ksh-integration.i18n/ksh-integration-jalang.md) |
| POSIX sh / ダッシュ | [posix-sh-integration.md](../../linux/posix-sh-integration.i18n/posix-sh-integration-jalang.md) |

Bash を使用したデフォルトの Ubuntu/Debian WSL セットアップのクイック パスは次のとおりです。

```bash
nano ~/.bashrc
# Paste the function block from bash-integration.md
source ~/.bashrc
```

## WSL 固有の考慮事項

### WSL から Windows ファイルにアクセスする

Windows ドライブは `/mnt/` の下にマウントされます。

```bash
/mnt/c/   # → C:\
/mnt/d/   # → D:\
```

プロジェクトが Windows ファイルシステム (例: `C:\Projects\stt`) 上にある場合は、`PROJECT_ROOT` を次のように設定します。

```bash
export PROJECT_ROOT="/mnt/c/Projects/stt"
```

この行を `~/.bashrc` (またはシェルの同等のもの) の `s()` 関数の**上**に追加します。

> **パフォーマンスのヒント:** 最高の I/O パフォーマンスを得るには、プロジェクト ファイルを `/mnt/c/...` ではなく WSL ファイルシステム (例: `~/projects/stt`) 内に保持してください。 WSL と Windows 間のファイルシステム間のアクセスは大幅に遅くなります。

### WSL 内の Python 仮想環境

WSL 内で標準の Linux 仮想環境を作成して使用します。

```bash
cd "$PROJECT_ROOT"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

関数内の `PY_EXEC` パス (`$PROJECT_ROOT/.venv/bin/python3`) はそのままで正しく動作します。

### Windows ターミナルから `s` を実行する

Windows で WSL を使用するには、[Windows Terminal](https://aka.ms/terminal) が推奨される方法です。各 WSL ディストリビューションの複数のタブ、ペイン、プロファイルをサポートします。 Microsoft Store から、または次の方法でインストールします。

```powershell
winget install Microsoft.WindowsTerminal
```

最もシームレスなエクスペリエンスを実現するには、Windows ターミナル設定で WSL ディストリビューションをデフォルトのプロファイルとして設定します。

### WSL 内の Docker と Kiwix

Kiwix ヘルパー スクリプト (`kiwix-docker-start-if-not-running.sh`) には Docker が必要です。 Docker Desktop for Windows をインストールし、WSL 2 統合を有効にします。

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/)をダウンロードしてインストールします。
2. [Docker Desktop] → [設定] → [リソース] → [WSL 統合] で、WSL ディストリビューションを有効にします。
3. WSL 内で確認します。
   ```bash
   docker --version
   ```

### Windows から WSL `s` 関数を呼び出す (オプション)

WSL ターミナルを開かずに Windows CMD または PowerShell ウィンドウから「s」ショートカットを呼び出したい場合は、それをラップできます。

```powershell
# PowerShell wrapper
function s { wsl bash -i -c "s $args" }
```

```bat
:: CMD wrapper — save as s.bat on your PATH
@echo off
wsl bash -i -c "s %*"
```

> `-i` フラグは対話型シェルをロードし、`~/.bashrc` (および `s` 関数) が自動的にソースされるようにします。

＃＃ 特徴

- **完全な Linux 互換性**: すべての Unix ツール (`timeout`、`pgrep`、`mktemp`、`grep`) はネイティブに動作します。回避策は必要ありません。
- **動的パス**: シェル設定に設定された `PROJECT_ROOT` 変数を介してプロジェクト ルートを自動的に検索します。
- **自動再起動**: バックエンドがダウンしている場合、「start_service」とローカルの Wikipedia サービスの実行を試みます (Docker が実行されている必要があります)。
- **スマート タイムアウト**: 最初に 2 秒の素早い応答を試み、その後 70 秒の詳細な処理モードに戻ります。