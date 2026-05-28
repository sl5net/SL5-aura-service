# Trino 統合 — 開発者ガイド

＃＃ 建築
オーラインターフェイス:
speech → INTERFACE=speech (.py のデフォルトのフォールバック)
端末 → INTERFACE=端末 (s() zshrc で明示)
web → INTERFACE=web (start_service で明示)
↓
aura_state.py ← 開発者向けの高レベル API
↓
trino_client.py ← 低レベルの DB 操作
↓
Trino メモリ カタログ
Memory.aura.features ← インターフェイスごとの変換のオン/オフ
Memory.aura.translation_state ← インターフェースごとのターゲット言語

## ローカルセットアップ

### 1. ドッカー

```bash
docker pull trinodb/trino
docker run -d --name trino -p 8083:8080 trinodb/trino
docker logs trino -f | grep -m1 "SERVER STARTED"
```

### 2. Python クライアント

```bash
source .venv/bin/activate
pip install trino
```

### 3. DB 初期化 (Aura 起動時に自動的に呼び出されます)

```bash
python3 scripts/py/func/db/init_trino_db.py
```

## 開発者 API — aura_state.py

```python
from scripts.py.func.db.aura_state import (
    enable_translation,
    disable_translation,
    set_language,
    get_current_language,
    is_translation_enabled,
    get_all_status,
)

# Enable translation for speech interface
enable_translation('speech', lang='en')

# Check status
is_translation_enabled('speech')  # True
get_current_language('speech')    # 'en'

# Disable
disable_translation('speech')

# All interfaces
get_all_status()
# [
#   {'interface': 'speech',   'translation': 'on',  'language': 'en'},
#   {'interface': 'terminal', 'translation': 'off', 'language': None},
#   {'interface': 'web',      'translation': 'off', 'language': None},
# ]
```

## 管理者 UI

http://ローカルホスト:8084

始める：
```bash
streamlit run scripts/py/chat/streamlit-admin.py --server.port 8084
```

## Trino UI (クエリ モニター)

http://localhost:8083/ui/

スクリプト/py/func/db/
§── init.py
§── trino_client.py ← 低レベル: feature_state、target_lang の取得/設定
§── init_trino_db.py ← 起動: Docker 起動 + スキーマ + テーブル
└── aura_state.py ← 開発者向けの高レベル API
スクリプト/py/チャット/
└── streamlit-admin.py ← ポート 8084 の管理 UI


## ロードマップ

- [x] Docker で実行されている Trino
- [x] Python クライアントが接続されました
- [x] Aura 起動時に DB が初期化されました
- [x] インターフェイス対応の変換状態
- [x] 音声/端末から分離された Web (Streamlit)
- [x] ポート 8084 の管理 UI
- [ ] 端子と音声は完全に独立しています
- [ ] ユーザー固有の上書き (マルチユーザー)
- [ ] 永続ストレージ (メモリ カタログを置き換えます)