# Übergabe-Bericht: CachyOS デバッグ – Aura STT 後処理

**データ:** 20. メルツ 2026  
**プロジェクト:** `~/projects/py/stt` (Aura STT – オフライン音声テキスト変換システム)  
**ステータス:** 問題が発生しています – Übergabe an nächsten Mitarbeiter  

---

## 1. 問題点

Aura での **CachyOS** 機能に関する詳細:

- **LanguageTool 経由の Rechtschreibkorrektur** wird nicht ausgefüult
- **すべて ~674 Regex-Regeln** は FUZZY_MAP_pre-Dateien grifen nicht を使用します
- Vosk-Transkriptionen werden **ungefiltert und unkorrigiert** ausgegeben (alles kleingeschrieben, keine Ersetzungen)
- **Manjaro と Windows** のソース コードの識別に関するすべての機能

例: Vosk liefert `"mal sehen ob es schwitzt bretzfeld"` → sollte nach Regelanwendung korrigier werden, wird aber unverändert ausgegeben.

---

## 2. システム管理

| |マンジャロ ✅ | CachyOS ⚠️ |
|---|---|---|
|パイソン | 3.14.2 | 3.14.3 |
|ジャワ | OpenJDK 17 | OpenJDK 17.0.18 |
|言語ツール | 6.6 | 6.6 |
| LTポート | 8082 | 8082 |
| WatchFiles-Reloads 開始 | 0 | früher viele (インツヴィッシェン ベホーベン) |

---

## 3. 最悪の事態が発生しました

### ✅ LanguageTool はこれを使用しました
- ポート 8082 での LT スタート
- Python-Aufruf 関数を直接実行するアイソリエーター テスト:
  ```
  POST /v2/check → 200
  "Das ist ein gross Fehler" → "Das ist ein groß Fehler"
  ```
- 問題: LT wird von Aura **gar nicht aufgerufen** (kein POST im LT-Log)

### ✅ 設定を修正してください
```python
USE_EXTERNAL_LANGUAGETOOL = False
LANGUAGETOOL_PORT = 8082
LANGUAGETOOL_CHECK_URL = "http://127.0.0.1:8082/v2/check"
```

### ✅ 正規表現キャッシュ関数の作成
```python
get_cached_regex(r'^test$', re.IGNORECASE)
# → re.compile('^test$', re.IGNORECASE)  ✓
```

### ✅ Python バージョンの同一性 (3.14.x システム側)

### ✅ inotify-Werte identisch (524288 / 16384)

### ✅ venv-問題のベホベン
`activate-venv_and_run-server.sh` の開始スクリプトは次のとおりです。
```bash
python3 -m venv .env   # ← falsch, wurde entfernt
python3 -m venv .venv  # ← korrekt, bleibt
```
Das doppelte venv-Erstellen wurde entfernt。 Dadurch ist Jetzt wieder ein Log vorhanden.

### ✅ ログ問題の原因
オーラ シュリープ ケイン ログ ヴァイル `&` デン プローゼス イン デン ヒンターグルント シュックト アンド stdout verschwand。 Log-Datei の Gelöst durch Umleitung (Empfehlung, noch nicht umgesetzt):
```bash
# In activate-venv_and_run-server.sh:
PYTHONDONTWRITEBYTECODE=1 python3 "$SCRIPT_TO_START" >> "$PROJECT_ROOT/log/aura_engine.log" 2>&1 &
```

---

## 4. Wie die Pipeline funktioniert (wichtig zum Verstehen)

```
Vosk (Speech-to-Text)
    ↓
process_text_in_background.py
    ↓
apply_all_rules_may_until_stable(text, GLOBAL_FUZZY_MAP_PRE, logger)
    ↓
apply_all_rules_until_stable(text, rules_map, logger)
    ↓  (gibt zurück: current_text, full_text_replaced_by_rule, skip_list, privacy_taint)
    ↓
if not regex_pre_is_replacing_all        # ← HIER wird LT blockiert
   and not is_only_number
   and 'LanguageTool' not in skip_list:
    correct_text_by_languagetool(...)    # ← wird nie erreicht
```

### Warum LT nie aufgerufen wird (bekannt):

「apply_all_rules_may_until_stable」内:
```python
if full_text_replaced_by_rule:
    skip_list.append('LanguageTool')   # ← LT wird in skip_list gesetzt
    return new_processed_text, True, skip_list, ...
```

`process_text_in_background.py` の内容を変更します。
```python
regex_pre_is_replacing_all = regex_pre_is_replacing_all_maybe
# ...
if (not regex_pre_is_replacing_all ...):
    correct_text_by_languagetool(...)  # ← nur wenn False
```

私はログ・ステート・ベイ・ジェデム・ドゥルシュラウフです:
```
🚀Iterative-All-Rules: full_text_replaced_by_rule='True, skip_list='[]'
```

Das bedeutet: `full_text_replaced_by_rule = True` → LT wird übersprungen.

**不快な点:** CachyOS の `True` は `full_text_replaced_by_rule` ですが、Manjaro は異常ですか?

---

## 5. Regelformat (zum Verständnis)

```python
# FUZZY_MAP_pre Einträge:
FUZZY_MAP_pre = [
    ('git commit ', r'^geht cobit einen$', 85, {'flags': re.IGNORECASE}),
    ('Sebastian', r'^(mein vorname|sebastian)$', 85, {'flags': re.IGNORECASE}),
]
```

形式: `(置換、正規表現パターン、しきい値、オプション辞書)`

「apply_all_rules_until_stable」のバージョン:
- `コンパイルされた正規表現.完全一致(current_text)` → setzt `full_text_replaced_by_rule = True`
- `compiled_regex.search(current_text)` → 部分一致、setzt `full_text_replaced_by_rule` **nicht**

---

## 6. 自己テストのテスト (DEV_MODE)

DEV_MODE はオーラ バイムです。自動テストを開始します。 CachyOS の使用:
```
ERROR - ❌ FAIL: git
   Input:    'geht cobit'
   Expected: 'git commit'
   Got:      'geht cobit'
```

**ウィヒティグ:** テストパターン `r'^geht cobit einen$'` (braucht "einen") を参照し、テスト入力は `'geht cobit'` を参照してください。 → テストはフェーラーハフトと CachyOS の両方に適用されます。 **Aber:** CachyOS に関するすべてのテストが、Manjaro のすべての機能をテストします。

---

## 7. 説明: GLOBAL_debug_skip_list

Der vielversprechendste nächste Schritt ist `GLOBAL_debug_skip_list` zu aktivieren. Dieser Flag gibt `print()`-Ausgaben direkt auf stdout — ロギング システムを使用できます。 Das zeigt Schritt für Schritt は der Regelschleife passiert にありました。

```bash
# Wo ist GLOBAL_debug_skip_list definiert?
grep -n "GLOBAL_debug_skip_list" scripts/py/func/process_text_in_background.py | head -5
```

Dann auf `True` setzen und Aura starten. Die print-Ausgaben erscheinen direkt im Terminal。

### 代替: Direkter Isolationstest der Regelengine

```python
# /tmp/test_rules.py
import sys, re
sys.path.insert(0, '/home/seeh/projects/py/stt')

# Regeln direkt laden
from config.maps.plugins.git.de_DE import FUZZY_MAP_pre  # Pfad anpassen
from scripts.py.func.process_text_in_background import apply_all_rules_until_stable
import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

result = apply_all_rules_until_stable('geht cobit einen', FUZZY_MAP_pre, logger)
print('Ergebnis:', result)
```

---

## 8. Verdächtige Stellen im コード

＃＃＃８ａ。 Privacy_taint_occurred 問題が発生しました
「apply_all_rules_until_stable」内:
```python
privacy_taint_occurred = True  # ← wird bei JEDEM Match gesetzt, auch nicht-privaten!
```
Das könnte dazu führen dass Logs unterdrückt werden und Verhalten anders ist.

＃＃＃８ｂ． Zwei verschiedene 正規表現関数
```python
get_cached_regex(pattern, flags)    # in apply_all_rules_until_stable
get_compiled_regex(pattern, logger) # in apply_all_rules_may_until_stable
```
Unterschiedliche Signaturen – これは、Verwirrung führen です。

＃＃＃８ｃ。 aura_engine.py の NameError-Risiko
```python
if settings.USE_EXTERNAL_LANGUAGETOOL:
    active_lt_url = settings.EXTERNAL_LANGUAGETOOL_URL
    # languagetool_process ← NIE gesetzt in diesem Zweig!

if not languagetool_process:  # ← NameError wenn USE_EXTERNAL_LANGUAGETOOL=True
    sys.exit(1)
```

---

## 9. Bekannte Altlasten im Code (ニヒト・クリティシュ、アベル・ズ・ビーチテン)

「正しいテキスト_バイ_言語ツール.py」内:
- `get_lt_session_202601311817()` が存在する `_lt_session` を参照する → `NameError` が正常に動作する
- `正しいテキスト_バイ_言語ツール_202601311818()` は正しいコピーです
- `adapter` mit `pool_connections=25` am Modulende nie verwendet

---

## 10. README は実際に使用されています

```markdown
*   **Linux (Wayland):** ⚠️ Likely supported, but not fully tested.
*   **Linux (CachyOS / Arch-based rolling release):** ⚠️ Partially supported.
    Post-processing rules and LanguageTool correction currently unreliable.
    Investigation ongoing. Manjaro (also Arch-based) works correctly.
```

コミット: `"CachyOS は現時点では制限されています"`

---

## 11. レレヴァンテ・ダティエン

|ダテイ |レレヴァンツ |
|---|---|
| `aura_engine.py` | Haupteinstiegspunkt、LT-Start、active_lt_url |
| `scripts/py/func/process_text_in_background.py` |レーゲル パイプライン、LT-アウフルフ |
| `scripts/py/func/start_ languagetool_server.py` | LT-Start-Logik、センチネル |
| `scripts/py/func/正しいテキスト_バイ_言語ツール.py` | LT HTTP-アウフルフ |
| `scripts/py/func/config/dynamic_settings.py` | DEV_MODE を搭載した |
| `config/settings.py` | LANGUAGETOOL_PORT=8082、CHECK_URL |
| `config/settings_local.py` | DEV_MODE=True/False (ローカル ユーバーシュライベン) |
| `config/filters/settings_local_log_filter.py` | LOG_ONLY、LOG_EXCLUDE |
| `scripts/activate-venv_and_run-server.sh` | Startskript (venv-Bug behoben) |
| `log/aura_engine.log` | Hauptlog (戦争の状況とバグ) |
| `log/ languagetool_server.log` | LT-サーバー-ログ |

---

## 12. ヒルフライヒェ・ベフェレ

```bash
# Aura starten:
~/projects/py/stt/scripts/restart_venv_and_run-server.sh

# venv aktivieren (Fish):
source ~/projects/py/stt/.venv/bin/activate.fish

# LT manuell starten:
java -Xms512m -Xmx4g \
  -jar ~/projects/py/stt/LanguageTool-6.6/languagetool-server.jar \
  --port 8082 --address 127.0.0.1 --allow-origin "*" &

# LT direkt testen:
curl -s -d "language=de-DE&text=Das ist ein gross Fehler" \
  http://127.0.0.1:8082/v2/check | python3 -m json.tool

# Laufende Prozesse:
pgrep -a -f "aura\|languagetool"

# Log live verfolgen:
tail -f log/aura_engine.log
```

---

*Bericht erstellt am 20.03.2026 — クロード ソネット 4.6 のデバッグ セッション*