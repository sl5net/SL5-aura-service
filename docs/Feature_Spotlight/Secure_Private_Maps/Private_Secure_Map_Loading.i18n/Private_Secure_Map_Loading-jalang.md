# 注目の機能: 安全なプライベート マップの読み込みと自動パッキング

このドキュメントでは、**セキュリティのベスト プラクティス**を強制して偶発的な Git 漏洩を防止しながら、**ライブ編集**を可能にする方法で機密マップ プラグイン (例: クライアント データ、独自のコマンド) を管理するためのアーキテクチャの概要を説明します。

---

## 1. コンセプト:「マトリョーシカ」セキュリティ

標準ツールを使用する際に最大限のプライバシーを確保するために、Aura は暗号化されたアーカイブに対して **マトリョーシカ (ロシア人形)** ネスト戦略を使用します。

1. **外層:** **AES-256** で暗号化された標準 ZIP ファイル (システムの `zip` コマンド経由)。
* *外観:* `aura_secure.blob` という名前のファイルが **1 つ** だけ含まれています。
* *利点:* ファイル名とディレクトリ構造を覗き見から隠します。
2. **内層 (BLOB):** BLOB 内の暗号化されていない ZIP コンテナー。
* *内容:* 実際のディレクトリ構造と Python ファイル。
3. **動作状態:** ロックが解除されると、ファイルは先頭にアンダースコアが付いた一時フォルダー (例: `_private`) に抽出されます。
* *セキュリティ:* このフォルダーは `.gitignore` によって厳密に無視されます。

---

## 2. 技術的なワークフロー

### A. セキュリティ ゲート (スタートアップ)
何かを解凍する前に、Aura は特定の `.gitignore` ルールについて `scripts/py/func/map_reloader.py` をチェックします。
* **ルール 1:** `config/maps/**/.*` (キー ファイルを保護)
* **ルール 2:** `config/maps/**/_*` (作業ディレクトリを保護)
これらが欠落している場合、システムは**異常終了**します。

### B. アンパック (例外駆動)
1. ユーザーは、パスワード (平文またはコメント) を含むキー ファイル (例: `.auth_key.py`) を作成します。
2. Aura は、このファイルと対応する ZIP (例: 「private.zip」) を検出します。
3. Aura は、キーを使用して外側の ZIP を復号化します。
4. Aura は `aura_secure.blob` を検出し、内部レイヤーを抽出し、ファイルを作業ディレクトリ `_private` に移動します。

### C. ライブ編集と自動パッキング (サイクル)
ここでシステムは「自己修復」状態になります。

1. **編集:** `_private/` 内のファイルを変更して保存します。
2. **トリガー:** Aura は変更を検出し、モジュールをリロードします。
3. **ライフサイクル フック:** モジュールは `on_reload()` 関数をトリガーします。
4. **SecurePacker:** プライベート フォルダーのルートにあるスクリプト (`secure_packer.py`) が実行されます。
※インナーZIP(構造)を作成します。
* `.blob` に名前を変更します。
* システムの `zip` コマンドを呼び出し、`.key` ファイルのパスワードを使用して外部アーカイブに暗号化します。

**結果:** `private.zip` は常に最新の変更内容を反映していますが、Git はバイナリ ZIP ファイルの変更のみを認識します。

---

## 3. セットアップガイド

### ステップ 1: ディレクトリ構造
次のようなフォルダー構造を作成します。
```text
config/maps/private/
├── .auth_key.py          # Contains your password (e.g. # MySecretPass)
└── private_maps.zip      # The encrypted archive
```

### ステップ 2: キー ファイル (`.auth_key.py`)
ドットで始める必要があります。
```python
# MySecretPassword123
# This file is ignored by Git.
```

### ステップ 3: Packer スクリプト (`secure_packer.py`)
このスクリプトをプライベート マップ フォルダー内に配置します (最初に圧縮する前に)。暗号化ロジックを処理します。マップが「on_reload」フックを介してこのスクリプトを呼び出すことを確認してください。

### ステップ 4: フックの実装
マップ ファイル (`.py`) に次のフックを追加して、保存するたびにバックアップをトリガーします。

```python
# In your private map file
def on_reload():
    # Logic to find and execute secure_packer.py
    # ... (See Developer Guide for snippet)
```

---

## 4. Git のステータスと安全性

適切に設定すると、「git status」には**のみ**が表示されます。
```text
modified:   config/maps/private/private_maps.zip
```
フォルダー「_private_maps」とファイル「.auth_key.py」は決して追跡されません。
```

---

### 2. Neu: `docs/Developer_Guide/Lifecycle_Hooks.md`

Wir sollten einen Ordner `Developer_Guide` (oder ähnlich) anlegen, um technische Details von allgemeinen Features zu trennen.

```markdown
# 開発者ガイド: プラグインのライフサイクル フック

Aura SL5 では、プラグイン (マップ) で、モジュールの状態が変化したときに自動的に実行される特定の「フック」を定義できます。これは、**Secure Private Map** システムのような高度なワークフローには不可欠です。

## `on_reload()` フック

`on_reload()` 関数は、任意の Map モジュールで定義できるオプションの関数です。

＃＃＃ 行動
* **トリガー:** モジュールが正常に **ホットリロード** (ファイル変更 + 音声トリガー) された直後に実行されます。
* **コンテキスト:** メイン アプリケーション スレッド内で実行されます。
* **安全性:** `try/excel` ブロックでラップされています。ここでのエラーはログに記録されますが、アプリケーションは**クラッシュしません**。

### 使用パターン: 「デイジーチェーン」
複雑なパッケージ (プライベート マップなど) の場合、多くのサブファイルがあることがよくありますが、ロジックを処理する必要があるのは 1 つの中央スクリプト (`secure_packer.py`) のみです。

フックを使用してタスクを上に委任できます。

```python
# Example: Delegating logic to a parent script
import importlib.util
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def on_reload():
    """
    Searches for 'secure_packer.py' in parent directories and executes it.
    """
    logger.info("🔄 Map modified. Triggering packer...")
    
    current_path = Path(__file__).resolve()
    search_dir = current_path.parent
    packer_script = None

    # Search upwards (max 4 levels)
    for _ in range(4):
        candidate = search_dir / "secure_packer.py"
        if candidate.exists():
            packer_script = candidate
            break
        if search_dir.name in ["maps", "config"]: break
        search_dir = search_dir.parent

    if packer_script:
        try:
            # Dynamic Import & Execution
            spec = importlib.util.spec_from_file_location("packer_dyn", packer_script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'on_reload'):
                module.on_reload()
        except Exception as e:
            logger.error(f"❌ Failed to run packer: {e}")
```

### ベストプラクティス
1. **高速に保つ:** メインフックで長時間のブロックタスク (巨大なダウンロードなど) を実行しないでください。必要に応じてスレッドを使用します。
2. **冪等性:** フックが機能を壊すことなく複数回実行できることを確認します (例: ファイルに無限に追加するのではなく、ファイルを書き換えます)。