# ホームディレクトリとクロスプラットフォームパスの処理

Aura は、複数のオペレーティング システムで実行できるように設計されています。 Linux、macOS、または Windows を実行しているかどうかに関係なく、ファイル システム ナビゲーション コマンドが確実に機能するように、パス文字列はアクティブなファジー マップに登録される前に動的に解析されます。

---

## パス正規化ロジック (`FUZZY_MAP_pre.py`)

動的パス マッピング ロジックは、次の標準的な手法に依存しています。

### 1. チルダ削減 (POSIX)
POSIX 準拠のシステム (Linux および macOS) では、ユーザーのホーム ディレクトリに一致する絶対パス (例: `/home/username/`) は起動時に `~` 相対パスに変換されます。これにより、文字列の長さが短くなり、生成されたルールを同じオペレーティング システム上の異なるユーザー間で移植できるようになります。

```python
# Replaces '/home/username/projects' with '~/projects'
if sys.platform != 'win32' and project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_FOR_MAP = project_root_str_full.replace(home_dir_str, '~', 1)
```

### 2. 絶対パスの保持 (Windows)
Windows は、標準のコマンド プロンプト (`cmd.exe`) または PowerShell 環境では、`~` 文字を確実に評価しません。したがって、プラグインは Windows 環境 (`sys.platform == 'win32'`) を検出すると、コマンドの実行が失敗しないように完全修飾絶対パス (例: C:\Users\username\...`) を保存します。

### 3. スラッシュの正規化 (`as_posix()`)
Aura は、設定マップに POSIX スタイルのスラッシュ (`/`) を内部的に使用します。このスクリプトは、Python の `pathlib.Path.as_posix()` メソッドを利用して、OS に依存するすべてのパス区切り文字を正規化します。これにより、Windows 環境ではバックスラッシュ (`\`) が自動的にサニタイズされます。