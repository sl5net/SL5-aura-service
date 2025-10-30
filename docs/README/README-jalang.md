# システム全体のオフライン音声からコマンドまたはテキストへのプラグイン可能なシステム

# SL5 Aura サービス - 機能と OS の互換性

SL5 オーラ サービスへようこそ!このドキュメントでは、主要な機能とそのオペレーティング システムの互換性の概要を説明します。

Aura は単なる文字起こしではありません。これは、あなたの音声を正確なアクションとテキストに変換する強力なオフライン処理エンジンです。

これは Vosk と LanguageTool に基づいて構築された完全なオフライン アシスタントであり、プラグイン可能なルール システムとダイナミック スクリプト エンジンを通じて究極のカスタマイズを実現するように設計されています。
  
  
翻訳: このドキュメントは [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/docs) にも存在します。

注: 多くのテキストは、元の英語ドキュメントの機械翻訳であり、一般的なガイダンスのみを目的としています。矛盾や曖昧な点がある場合には、常に英語版が優先されます。この翻訳を改善するためにコミュニティからの協力を歓迎します。


[![SL5 Aura (v0.7.0.2): A Deep Dive Under the Hood – Live Coding & Core Concepts](https://img.youtube.com/vi/tEijy8WRFCI/maxresdefault.jpg)](https://www.youtube.com/watch?v=tEijy8WRFCI)
( https://skipvids.com/?v=tEijy8WRFCI )

## 主な機能

* **オフライン&プライベート:** 100% ローカル。データがマシンから流出することはありません。
* **ダイナミック スクリプト エンジン:** テキストの置換を超えた機能。ルールはカスタム Python スクリプト (「on_match_exec」) を実行して、API の呼び出し (Wikipedia の検索など)、ファイルの操作 (ToDo リストの管理など)、動的コンテンツの生成 (コンテキストを認識した電子メールの挨拶など) などの高度なアクションを実行できます。
* **高度な制御の変換エンジン:** 構成主導の高度にカスタマイズ可能な処理パイプラインを実装します。ルールの優先順位、コマンド検出、およびテキスト変換は、純粋にファジー マップ内のルールの順序によって決定されるため、コーディングではなく**構成が必要です**。
* **控えめな RAM 使用量:** メモリをインテリジェントに管理し、十分な空き RAM がある場合にのみモデルをプリロードし、他のアプリケーション (PC ゲームなど) が常に優先されるようにします。
* **クロスプラットフォーム:** Linux、macOS、および Windows で動作します。
* **完全に自動化:** 独自の LanguageTool サーバーを管理します (ただし、外部を使用することもできます)。
* **超高速:** インテリジェントなキャッシュにより、即時の「リッスン中...」通知と高速処理が保証されます。

## ドキュメント

すべてのモジュールとスクリプトを含む完全な技術リファレンスについては、公式ドキュメント ページをご覧ください。自動的に生成され、常に最新の状態になります。

[**Go to Documentation >>**](https://sl5net.github.io/SL5-aura-service/)


### ビルドステータス
[![Linux Manjaro](https://img.shields.io/badge/Manjaro-Tested-27ae60?style=for-the-badge&logo=manjaro)](https://youtu.be/D9ylPBnP2aQ)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)
[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![Documentation](https://img.shields.io/badge/documentation-live-brightgreen)](https://sl5net.github.io/SL5-aura-service/)

**他の言語で読む:**

[🇬🇧 English](README.md) | [🇸🇦 العربية](docs/README/README-arlang.md) | [🇩🇪 Deutsch](docs/README/README-delang.md) | [🇪🇸 Español](docs/README/README-eslang.md) | [🇫🇷 Français](docs/README/README-frlang.md) | [🇮🇳 हिन्दी](docs/README/README-hilang.md) | [🇯🇵 日本語](docs/README/README-jalang.md) | [🇰🇷 한국어](docs/README/README-kolang.md) | [🇵🇱 Polski](docs/README/README-pllang.md) | [🇵🇹 Português](docs/README/README-ptlang.md) | [🇧🇷 Português Brasil](docs/README/README-pt-BRlang.md) | [🇨🇳 简体中文](docs/README/README-zh-CNlang.md)

---

## インストール

セットアップは 2 段階のプロセスです。
1. このリポジトリのクローンをコンピュータに作成します。
2. オペレーティング システムのワンタイム セットアップ スクリプトを実行します。

セットアップ スクリプトは、システムの依存関係、Python 環境、必要なモデルとツール (最大 4GB) を GitHub リリースから直接ダウンロードして最大速度を実現するなど、すべてを処理します。

#### Linux、macOS、Windows の場合
プロジェクトのルート ディレクトリでターミナルを開き、システムのスクリプトを実行します。
```bash
# For Ubuntu/Debian, Manjaro/Arch, macOs  or other derivatives

bash setup/{your-os}_setup.sh

# For Windows in Admin-Powershell

setup/windows11_setup.ps1
```

#### Windows の場合
管理者権限 **「PowerShell で実行」** でセットアップ スクリプトを実行します。

**読み取りと実行のためのツールをインストールします。 [CopyQ](https://github.com/hluk/CopyQ) または [AutoHotkey v2](https://www.autohotkey.com/)**。これはテキスト入力ウォッチャーに必要です。

---

＃＃ 使用法

### 1. サービスを開始する

#### Linux および macOS の場合
単一のスクリプトですべてを処理します。メインのディクテーション サービスとファイル ウォッチャーがバックグラウンドで自動的に開始されます。
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

#### Windows の場合
サービスの開始は、**2 段階の手動プロセス**です。

1. **メイン サービスを開始します。** `start_dictation_v2.0.bat` を実行します。または、`.venv` から `python3` を使用してサービスを開始します。

### 2. ホットキーを設定する

ディクテーションをトリガーするには、特定のファイルを作成するグローバル ホットキーが必要です。クロスプラットフォーム ツール [CopyQ](https://github.com/hluk/CopyQ) を強くお勧めします。

#### 私たちのおすすめ: CopyQ

CopyQ でグローバル ショートカットを使用して新しいコマンドを作成します。

**Linux/macOS のコマンド:**
```bash
touch /tmp/sl5_record.trigger
```

**[CopyQ](https://github.com/hluk/CopyQ) を使用する場合の Windows のコマンド:**
```js
copyq:
var filePath = 'c:/tmp/sl5_record.trigger';

var f = File(filePath);

if (f.openAppend()) {
    f.close();
} else {
    popup(
        'error',
        'cant read or open:\n' + filePath
        + '\n' + f.errorString()
    );
}
```


**[AutoHotkey](https://AutoHotkey.com) を使用する場合の Windows のコマンド:**
```sh
; trigger-hotkeys.ahk
; AutoHotkey v2 Skript
#SingleInstance Force ; Stellt sicher, dass nur eine Instanz des Skripts läuft

;===================================================================
; Hotkey zum Auslösen des Aura Triggers
; Drücke Strg + Alt + T, um die Trigger-Datei zu schreiben.
;===================================================================
f9::
f10::
f11::
{
    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("Aura Trigger ausgelöst!")
    SetTimer(() => ToolTip(), -1500)
}
```


### 3. ディクテーションを始めましょう!
任意のテキスト フィールドをクリックし、ホットキーを押すと、「Listening...」通知が表示されます。はっきりと話してから一時停止します。修正されたテキストが入力されます。

---


## 詳細設定 (オプション)

ローカル設定ファイルを作成することで、アプリケーションの動作をカスタマイズできます。

1. 「config/」ディレクトリに移動します。
2. `settings_local.py_Example.txt` のコピーを作成し、その名前を `settings_local.py` に変更します。
3. `settings_local.py` を編集して、メインの `config/settings.py` ファイルの設定をオーバーライドします。

この `settings_local.py` ファイルは Git によって (おそらく) 無視されるため、個人的な変更は (おそらく) 更新によって上書きされません。

### プラグインの構造とロジック

システムのモジュール性により、plugins/ ディレクトリを介した堅牢な拡張が可能になります。

処理エンジンは **階層的な優先順位チェーン** に厳密に従っています。

1. **モジュールのロード順序 (高優先度):** コア言語パック (de-DE、en-US) からロードされるルールは、plugins/ ディレクトリ (アルファベット順で最後にロードされる) からロードされるルールよりも優先されます。
  
2. **ファイル内順序 (マイクロ優先度):** 特定のマップ ファイル (FUZZY_MAP_pre.py) 内では、ルールは **行番号** (上から下) によって厳密に処理されます。
  

このアーキテクチャにより、コア システム ルールが保護されると同時に、プロジェクト固有のルールまたはコンテキスト認識ルール (CodeIgniter やゲーム コントロールのルールなど) をプラグインを介して優先度の低い拡張機能として簡単に追加できます。
## Windows ユーザー向けの主要なスクリプト

Windows システム上でアプリケーションをセットアップ、更新、実行するための最も重要なスクリプトのリストを次に示します。

### セットアップとアップデート
* `setup/setup.bat`: 環境の **最初の 1 回限りのセットアップ**のためのメイン スクリプト。
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `powershell を実行します -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

* `update.bat` : これらをプロジェクト フォルダーから実行し、**最新のコードと依存関係を取得します**。

### アプリケーションの実行
* `start_dictation_v2.0.bat`: **ディクテーション サービス**を開始するための主要なスクリプト。

### コアスクリプトとヘルパースクリプト
* `dictation_service.py`: コア Python サービス (通常は上記のスクリプトのいずれかによって開始されます)。
* `get_suggestions.py`: 特定の機能のためのヘルパー スクリプト。




## 🚀 主な機能と OS の互換性

OS 互換性の凡例:  
* 🐧 **Linux** (Arch、Ubuntu など)  
* 🍏 **macOS**  
* 🪟 **Windows**  
* 📱 **Android** (モバイル固有の機能用)  

---

### **コア Speech-to-Text (Aura) エンジン**
オフライン音声認識と音声処理のための主要なエンジン。

  
**オーラコア/** 🐧 🍏 🪟  
§─ `dictation_service.py` (Aura をオーケストレーションするメイン Python サービス) 🐧 🍏 🪟  
§┬ **ライブ ホットリロード** (構成とマップ) 🐧 🍏 🪟  
│§ **テキストの処理と修正/** 言語ごとにグループ化 (例: `de-DE`、`en-US`、...)   
│§ 1. `normalize_punctuation.py` (文字起こし後の句読点を標準化) 🐧 🍏 🪟  
│§ 2. **インテリジェントな事前修正** (`FuzzyMap Pre` - [The Primary Command Layer](docs/CreatingNewPluginModules-jalang.md)) 🐧 🍏 🪟  
││ * **動的スクリプト実行:** ルールはカスタム Python スクリプト (on_match_exec) をトリガーして、API 呼び出し、ファイル I/O などの高度なアクションを実行したり、動的応答を生成したりできます。  
││ * **カスケード実行:** ルールは順番に処理され、その効果は **累積的**です。以前のルールによって変更されたテキストには、後のルールが適用されます。  
││ * **最優先停止基準:** ルールが **完全一致** (^...$) に達すると、そのトークンの処理パイプライン全体が直ちに停止します。このメカニズムは、信頼性の高い音声コマンドを実装するために重要です。  
│§ 3. `correct_text_by_ languagetool.py` (文法/スタイル修正のために LanguageTool を統合) 🐧 🍏 🪟  
│└ 4. **インテリジェントな事後修正** (`FuzzyMap`)**– LT 後の改良** 🐧 🍏 🪟  
││ * LT 固有の出力を修正するために、LanguageTool の後に適用されます。前修正レイヤーと同じ厳密なカスケード優先順位ロジックに従います。  
││ * **動的スクリプト実行:** ルールはカスタム Python スクリプト ([on_match_exec](docs/advanced-scripting-jalang.md)) をトリガーして、API 呼び出し、ファイル I/O などの高度なアクションを実行したり、動的応答を生成したりできます。  
││ * **ファジー フォールバック:** **ファジー類似性チェック** (しきい値、たとえば 85% によって制御される) は、優先度が最も低いエラー修正層として機能します。これは、先行する決定的/カスケード ルールの実行全体で一致が見つからなかった場合 (current_rule_matched が False) にのみ実行され、可能な限り遅いファジー チェックを回避することでパフォーマンスを最適化します。  
§┬ **モデル管理/**   
│§─ `prioritize_model.py` (使用状況に基づいてモデルのロード/アンロードを最適化します) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (初回モデルのセットアップを構成します) 🐧 🍏 🪟  
§─ **アダプティブ VAD タイムアウト** 🐧 🍏 🪟  
§─ **アダプティブ ホットキー (開始/停止)** 🐧 🍏 🪟  
└─ **インスタント言語切り替え** (モデルのプリロードによる実験的) 🐧 🍏   

**システムユーティリティ/**   
§┬ **LanguageTool サーバー管理/**   
│§─ `start_ languagetool_server.py` (ローカル LanguageTool サーバーを初期化します) 🐧 🍏 🪟  
│└─ `stop_ languagetool_server.py` (LanguageTool サーバーをシャットダウンします) 🐧 🍏
§─ `monitor_mic.sh` (例: キーボードとモニターを使用せずにヘッドセットで使用する場合) 🐧 🍏 🪟  

### **モデルとパッケージの管理**  
大規模な言語モデルを堅牢に処理するためのツール。  

**モデル管理/** 🐧 🍏 🪟  
§─ **堅牢なモデル ダウンローダー** (GitHub リリース チャンク) 🐧 🍏 🪟  
§─ `split_and_hash.py` (リポジトリ所有者が大きなファイルを分割してチェックサムを生成するためのユーティリティ) 🐧 🍏 🪟  
━─ `download_all_packages.py` (エンドユーザーがマルチパート ファイルをダウンロード、検証、再構築するためのツール) 🐧 🍏 🪟  


### **開発および展開ヘルパー**  
環境のセットアップ、テスト、サービス実行のためのスクリプト。  

**DevHelpers/**  
§┬ **仮想環境管理/**  
│§ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
§┬ **システム全体のディクテーションの統合/**  
│§ Vosk-システム-リスナーの統合 🐧 🍏 🪟  
│§ `scripts/monitor_mic.sh` (Linux 固有のマイクモニタリング) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey は認識されたテキストをリッスンし、システム全体で入力します) 🪟  
━─ **CI/CD 自動化/**  
└─ 拡張された GitHub ワークフロー (インストール、テスト、ドキュメントのデプロイメント) 🐧 🍏 🪟 *(GitHub Actions で実行)*  

### **今後の/実験的な機能**  
現在開発中またはドラフト状態の機能。  

**実験的な機能/**  
§─ **ENTER_AFTER_DICTATION_REGEX** アクティベーション ルールの例 "(ExampleAplicationThatNotExist|Pi、個人用 AI)" 🐧  
§┬プラグイン  
│╰┬ **Live Lazy-Reload** (*) 🐧 🍏 🪟  
(*プラグインのアクティブ化/非アクティブ化とその構成への変更は、サービスを再起動せずに次回の処理実行時に適用されます。*)  
│ § **git コマンド** (git コマンド送信の音声制御) 🐧 🍏 🪟  
│ § **vannweil** (ドイツ-ヴァンヴァイルの地図) 🐧 🍏 🪟  
│ § **ポーカー プラグイン (ドラフト)** (ポーカー アプリケーションの音声制御) 🐧 🍏 🪟  
│ └ **0 A.D. プラグイン (ドラフト)** (0 A.D. ゲームの音声コントロール) 🐧   
§─ **セッション開始時または終了時のサウンド出力** (説明保留中) 🐧   
§─ **視覚障害者向けの音声出力** (説明保留中) 🐧 🍏 🪟  
━─ **SL5 Aura Android プロトタイプ** (まだ完全にはオフラインではありません) 📱  

---

*(注: Arch (ARL) や Ubuntu (UBT) などの特定の Linux ディストリビューションは、一般的な Linux 🐧 シンボルでカバーされています。詳細な区別については、インストール ガイドで説明されている場合があります。)*









<詳細>
<summary>クリックすると、このスクリプト リストの生成に使用されたコマンドが表示されます</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "dictation_service.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</詳細>


### 少しグラフィックで見て、背後にあるものを確認してください。

![yappi_call_graph](doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

  
![pydeps -v -o dependencies.svg scripts/py/func/main.py](doc_sources/dependencies.svg)


# 使用モデル:

推奨事項: Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 のモデルを使用します (おそらく高速です)

この Zip 形式のモデルは `models/` フォルダーに保存する必要があります

`mv vosk-model-*.zip モデル/`


|モデル |サイズ |ワードエラー率/速度 |メモ |ライセンス |
| -------------------------------------------------------------------------------------- | ---- | -------------------------------------------------------------------------------------------- | -------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1.8G | 5.69 (librispeech test-clean)<br/>6.05 (tedlium)<br/>29.78 (コールセンター) |正確な一般的な米国英語モデル |アパッチ2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) | 1.9G | 9.83 (Tuda-de テスト)<br/>24.00 (ポッドキャスト)<br/>12.82 (CV テスト)<br/>12.42 (mls)<br/>33.26 (mtedx) |電話およびサーバー用のドイツの大型モデル |アパッチ2.0 |

この表には、サイズ、ワードエラー率または速度、注意事項、ライセンス情報など、さまざまな Vosk モデルの概要が示されています。


- **Vosk モデル:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **言語ツール:**  
(6.6)[https://languagetool.org/download/](https://languagetool.org/download/)

**LanguageTool のライセンス:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---

## プロジェクトをサポートする
このツールが役立つと思われた場合は、コーヒーの購入をご検討ください。あなたのサポートは、将来の改善を促進するのに役立ちます。

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)