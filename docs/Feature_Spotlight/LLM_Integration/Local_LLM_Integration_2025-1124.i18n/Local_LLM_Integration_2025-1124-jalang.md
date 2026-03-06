# 🧠 SL5 Aura ハイブリッド モード: ローカル LLM 統合

**ステータス:** 実験的 / 安定版
**テクノロジー:** Ollama (Llama 3.2) + Python サブプロセス
**プライバシー:** 100% オフライン

## コンセプトは「アーキテクト＆インターン」

伝統的に、Aura は高速、正確、予測可能な決定論的ルール (RegEx) に依存しています。こちらは**「建築家」**です。ただし、ユーザーは *「ジョークを教えてください」* や *「このテキストを要約してください」* など、「あいまいな」質問や創造的な質問をしたい場合があります。

ここで **ローカル LLM プラグイン** (**「インターン」**) が登場します。
1. **Aura (正規表現)** は、最初にすべての厳密なコマンド (「ライトをオンにする」、「アプリを開く」) をチェックします。
2. **AND**/ **OR** に一致するものがない場合、特定のトリガー ワード (例: 「Aura ...」) が検出された場合、フォールバック ルールがアクティブになります。
3. テキストはローカル AI モデル (Ollama) に送信されます。
4. 応答はサニタイズされ、TTS またはテキスト入力によって出力されます。

---

## 🛠 前提条件

プラグインには、マシン上でローカルに動作する [Ollama](https://ollama.com/) の実行インスタンスが必要です。

```bash
# Installation (Arch/Manjaro)
sudo pacman -S ollama
sudo systemctl enable --now ollama

# Download model (Llama 3.2 3B - only ~2GB, very fast)
ollama run llama3.2
```

---

## 📂 構造とロード順序

プラグインは意図的に「z_fallback_llm」フォルダーに配置されます。
Aura はプラグインを **アルファベット順**でロードするため、この名前付けにより、LLM ルールが **最後にロードされることが保証されます**。これは、認識されないコマンドに対する「セーフティ ネット」として機能します。

**パス:** `config/maps/plugins/z_fallback_llm/de-DE/`

### 1. マップ (`FUZZY_MAP_pre.py`)

**高スコア (100)** とトリガー ワードを使用して、Aura に強制的に制御をスクリプトに引き渡します。

```python
import re
from pathlib import Path
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # Trigger: "Aura" + any text
    ('ask_ollama', r'^\s*(Aura|Aurora|Laura)\s+(.*)$', 100, {
        'flags': re.IGNORECASE,
        # 'skip_list': ['LanguageTool'], # Optional: Performance boost
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py']
    }),
]
```

### 2. ハンドラー (`ask_ollama.py`)

このスクリプトは Ollama CLI と通信します。
**重要:** これには「clean_text_for_typing」関数が含まれています。生の LLM 出力には、絵文字 (😂、🚀) や特殊文字が含まれることが多く、「xdotool」などのツールやレガシー TTS システムをクラッシュさせる可能性があります。

```python
# Snippet from ask_ollama.py
def execute(match_data):
    # ... (Regex group extraction) ...
    
    # System prompt for short answers
    system_instruction = "Answer in German. Max 2 sentences. No emojis."
    
    # Subprocess call (blocks briefly, note the timeout!)
    cmd = ["ollama", "run", "llama3.2", full_prompt]
    result = subprocess.run(cmd, capture_output=True, ...)

    # IMPORTANT: Sanitize output for system stability
    return clean_text_for_typing(result.stdout)
```

---

## ⚙️ カスタマイズオプション

### トリガーの変更
「Aura」をウェイクワードとして使用したくない場合は、「FUZZY_MAP_pre.py」の正規表現を変更してください。
* 真のキャッチオールの例 (Aura が知らないすべて): `r'^(.*)$'` (注意: スコアを調整してください!)

### モデルの交換
`ask_ollama.py` 内のモデルを簡単に交換できます (たとえば、より複雑なロジックの場合は `mistral` に切り替えることができますが、より多くの RAM が必要になります)。
```python
cmd = ["ollama", "run", "mistral", full_prompt]
```

### システムプロンプト (ペルソナ)
`system_instruction` を調整することで、Aura に個性を与えることができます。
> 「あなたは SF 映画の皮肉たっぷりなアシスタントです。」

---

## ⚠️ 既知の制限事項

1. **レイテンシ:** ブート後の最初のリクエストでは、モデルが RAM に読み込まれるまでに 1 ～ 3 秒かかる場合があります。後続のリクエストは高速になります。
2. **競合:** 正規表現が広すぎる (`.*`) 場合、適切なフォルダー構造がなければ、標準コマンドを飲み込んでしまう可能性があります。アルファベット順 (`z_...`) は必須です。
3. **ハードウェア:** 約 1 個のハードウェアが必要です。 Llama 3.2 用の 2GB の空き RAM。