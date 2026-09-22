> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

# ⬟ SL5 オーラ – あなたの声。あなたのルール。

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 100％オフライン、プライバシー重視の音声アシスタントフレームワーク。  
> 自分の声が正確に何をするのか定義してください — 1つの単語から
> 完全な Python スクリプトへ。クラウドはなし。データはあなたのマシンを離れません。
> Linux、macOS、Windowsで、ターミナル、ブラウザ、またはバックグラウンドサービスとして動作します。

| 👵 初心者 | 🎓 学習者 | 🧑‍💻 開発者 |
|---|---|---|
| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-jalang.md#the-oma-modus-beginner-shortcut) : 単語を書くだけで、Auraが残りを行います | コアンで学ぶ — 一度に一つの概念 | 完全なPythonスクリプティング、プラグイン、API呼び出し |
| 🗄️ 状態管理 | Trino + Airflow オーケストレーション, fzf, CopyQ, 音声/ターミナルコマンド, ブラウザUI |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **テストごとに約2.87 J** (39 tests without LanguageTool across >800 maps @ 0.07s warm / 0.36s cold 🌿 measured with XMDLINK1X) · クラウドコンピューティングなし

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **フルテストスイート：** LanguageToolで94のテストを800以上のマップで実行、ウォームで0.07秒 / コールドで0.46秒 · クラウドコンピュートなし

<details>
<summary>クイックスタート</summary>

## クイックスタート

### オプションA：ワンクリック＆ウェブインストーラー (Recommended)

Linux、macOS、Windows用のワンライナーコマンドまたはスタンドアロンインストーラー：
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-jalang.md)**

---

##Option B:手動インストール(Developers / Git)

1。 このリポジトリをダウンロードまたはクローンする
2. OS (see `setup/` folder) のセットアップスクリプトを実行します。
- Linuxの(Arch/Manjaro):`bash setup/manjaro_arch_setup.sh`
- Linuxの(Ubuntu/Debian):`bash setup/ubuntu_setup.sh`
- Linuxの(openSUSE):`bash setup/suse_setup.sh`
- Linux (NixOS): `nix-shell setup/shell.nix` 以降 `bash setup/nixos_setup.sh`
===> ⚠️ 実験的 — 作者によってテストされていない、フィードバック歓迎! エスプレッソ
- macOS:`bash setup/macos_setup.sh`の
- ウィンドウズ:`setup/windows11_setup_with_ahk_copyq.bat`
3. Auraの開始:`./scripts/restart_venv_and_run-server.sh`
4。 あなたのホットキーを押して話す - **[full guide →](../docs/GettingStarted.i18n/GettingStarted-jalang.md)**

---

### アンインストール
SL5 Auraの背景サービス、自動起動エントリ、仮想環境を削除します。
- **Linux / macOS:** `bash setup/uninstall.sh`
- **Windows (PowerShell):** `powershell -File setup/uninstall.ps1`
*(Your custom rules in `config/maps/` are kept safe by default unless you specify `--purge`).*

---


**注記事項と互換性**

※Windows:** ✅ 完全対応(uses AutoHotkey/PowerShell)
※MacOS:** ✅ 完全対応(uses AppleScript)
***Linux (X11/Xorg):** ✅ 完全サポート
***Linux (Wayland):** ✅ 完全にサポートされている(tested on KDE Plasma 6 / Wayland).
***Linux (CachyOS / Arch-based rolling release):** ✅ 完全サポート
glibc 2.43 の互換性のために mimalloc (`sudo pacman -S mimalloc`) が必要です。
***Linux (NixOS):** 実験 — コミュニティが組み込まれたセットアップは、まだテストされていない。
是非お試し下さい。ぜひご活用ください。 エスプレッソ
***Linux (Manjaro):** New : システム全体ホットキーがfzf-like、キーボード駆動インターフェイスを開くので、デスクトップ(completely decoupled from the active window)のどこからでもAuraコマンドを実行できます。 このホットキー主導のランチャーは、現在、Linux (Manjaro) で実装およびテストされています。他のディストリビューションは動作するかもしれませんが、セットアップが必要です。 [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-jalang.md)   で見る


    
SL5 Aura は、**Vosk** (for Speech-to-Text) と **LanguageTool** (for Grammar/Style) 上に構築された、**オフラインの音声アシスタント** です。この機能は、クリエイティブなレスポンスと高度なファジーマッチングのために、オプションの **Local LLM (Ollama) Fallback** を備えています。 音声を正確なアクションとテキストに変換し、プラグイン可能なルールシステムと動的スクリプティングエンジンを使用して究極のカスタマイズのために設計されています。
    
翻訳: このドキュメントは[other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n)にも存在します。


注意: 多くのテキストは、元の英語文書の機械で生成された翻訳であり、一般的なガイダンスのみを目的としています。 矛盾や曖昧さの場合、英語バージョンは常に優先します。 コミュニティからこの翻訳を改善するためのお手伝いをします!

</details>

<details>
<summary>デモXHTMLタグ19X

##### クラウド デモ

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **ヒント:** より良い端末体験については、[Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-jalang.md) をご覧ください。

### ◀ ビデオチュートリアル
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Alternative link: XMDLINK1X)*

</details>

<details>
<summary>Keyの特徴</summary>

## 主な特長

*** オフライン&プライベート:** 100%ローカル。 データを残さない
***ダイナミックスクリプトエンジン:** テキスト置換を超えて行きます。 ルールは、カスタムPythonスクリプト(`on_match_exec`)を実行して、APIs (e.g., search Wikipedia)を呼び出したり、(e.g., manage a to-do list)とやり取りしたり、動的コンテンツ(e.g., a context-aware email greeting)を生成したりするなどの高度なアクションを実行できます。
***Context-Aware Rules:** 特定のアプリケーションにルールを制限します。 `only_in_windows` を使うと、特定のウィンドウのタイトル (e.g., "Terminal", "VS Code" or "Browser") がアクティブになっている場合にのみルールがトリガーされます。 これは、(Linux, Windows, macOS)のクロスプラットフォームで動作します。
***高制御変換エンジン:** 構成主導の、高度にカスタマイズ可能な処理パイプラインを実装します。 ルールの優先順位、コマンドの検出、およびテキストの変換は、Fuzzy Maps のルールの順序で純粋に決定されます。**configuration を必要としません。
* **保守的なRAMの使用法:** メモリをインテリジェントに管理し、十分な空きRAMが利用可能な場合のみモデルをプリロードし、他のアプリケーション(like your PC games)は常に優先しています。
* **十字プラットホーム:** Linux、macOS、Windows で動作します。
*** 完全自動化:** 独自のランゲージツールサーバー (but you can also use an external one) を管理します。
***速い*Blazing:**理性的なキャッシュは即刻の「リスト...」の通知および速い処理を保障します。
***トリノによる動的状態管理:** インターフェイス-awareの構成エンジン
`speech`、`terminal`、`web` の設定を分離します。
他人に影響を与える。 リアルタイム **管理者ダッシュボード** (port 8084).
</details>

<details>
<summary> 🔌 使いやすい統合</summary>
  
    
## 🔌 既知の統合

SL5-Auraは、**100以上の事前構成プラグインの広大な生態系が付属しています**。 ここにいくつかのハイライトがあります。

## OculiX / SikuliX IDE 音声制御
SL5-Auraは、**OculiX**と**SikuliX IDE**の一流の音声サポートを提供します。 この統合により、自動化コードを「話す」することができます。

* **ボイス・ツー・スニペット:** "click"、"wait"、"find all"、"Services は、正しい Python コード (e.g., `click("image.png")`) を IDE に即座にタイプします。
* **窓-Aware:** プラグインは文脈に敏感です。OculiX/SikuliX ウィンドウが集中したときにのみ有効です。
***スマート英語サポート:** `en-US` は、(e.g., German-English phonetics) の非ネイティブなアクセントに焦点を合わせ、グローバルコミュニティの高評価精度を保証します。
*** 拡張可能:** `FUZZY_MAP_pre.py`形式を簡単に編集できます。

> **ステータス:** OculiXチーム(see XMDLINK0X)のコミュニティプラグインとして認識。

### LibreOffice IDE 音声操作

### 紀元0年 音声コントロール

---

</details>


<details>
XHTMLタグ2XドキュメンテーションXHTMLタグ3X

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)

## ドキュメンテーション

すべてのモジュールとスクリプトを含む完全な技術的リファレンスについては、公式ドキュメントページをご覧ください。これは自動的に生成され、常に最新の状態に保たれています。

👉 [**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)

## 機能スポットライト
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-jalang.md) — デュアルパン`fzf`ルール検索、ライブコンテキストプレビュー、`Enter`/`Ctrl+R`によるインスタントコマンド実行、および`Ctrl+E`によるエディタ統合。 グローバルなホットキー (`Super+S`) と複数の専用の検索環境で、ボイスコマンドで事前設定を行えます。

## ビルドステータス

[![Linux Manjaro](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)

[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/mac_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/win11_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![OculiX Compatible](https://img.shields.io/badge/OculiX-Compatible-blueviolet?style=for-the-badge&logo=python)](https://github.com/oculix-org/Oculix)
<div align="left">
<a href="https://github.com/sl5net/SL5-aura-service/stargazers">
<img src="https://img.shields.io/github/stars/sl5net/SL5-aura-service?style=social" alt="Stargazers">
</a>
<img src="https://img.shields.io/github/license/sl5net/SL5-aura-service" alt="License">
<a href="https://sl5net.github.io/SL5-aura-service/">
<img src="https://img.shields.io/badge/documentation-live-brightgreen" alt="Documentation">
</a>
</div>

</details>

他の言語でこれを読む:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-jalang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-jalang.md) | [🇪🇸 Español](../README.i18n/README-eslang-jalang.md) | [🇫🇷 Français](../README.i18n/README-frlang-jalang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-jalang.md) | [🇯🇵 日本語](../README.i18n/README-jalang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-jalang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-jalang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-jalang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-jalang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-jalang.md)

---

<details>
<summary>インストール</summary>

## インストール

## ◀ モデレーションなしでクイックインストール(Manjaro/Arch Video)
6分間のセットアッププロセスをすべて見る:
※ダウンロード:**〜3分
*** 設定と最初のスタート:** ~3分(including Welcome Wizard)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


セットアップは2段階のプロセスです:
1。 最新のリリースまたはマスター( https://github.com/sl5net/SL5-aura-service/archive/master.zip )をダウンロードするか、このリポジトリをコンピュータにクローンします。
2。 オペレーティングシステム用のワンタイムセットアップスクリプトを実行します。

セットアップスクリプトは、システム依存性、Python環境、および必要なモデルをダウンロードし、GitHubリリースから直接(~4GB)をダウンロードし、最大速度を実現します。


Linux、macOS、Windows (with Optional Language Exclusion) 用の #### ### ## ## ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

ディスク容量と帯域幅を保存するには、設定中に特定の言語モデル(`de`, `en`)またはすべてのオプションモデル(`all`)を除外できます。 **コアコンポーネント (LanguageTool, lid.176) は常に含まれています。**

プロジェクトのルートディレクトリのターミナルを開き、システム用のスクリプトを実行します。

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

# For Arch-based systems (Manjaro, CachyOS, EndeavourOS, etc.):
`bash setup/manjaro_arch_setup.sh`

```sudo pacman -S mimalloc```


# Examples:
# Install everything (Default):
# bash setup/manjaro_arch_setup.sh

# Exclude German models:
# bash setup/manjaro_arch_setup.sh exclude=de

# Exclude all VOSK language models:
# bash setup/manjaro_arch_setup.sh exclude=all

# For Windows in an Admin-Powershell session

setup/windows11_setup.ps1 -Exclude [OPTION]

# Examples:
# Install everything (Default):
# setup/windows11_setup.ps1

# Exclude English models:
# setup/windows11_setup.ps1 -Exclude "en"

# Exclude German and English models:
# setup/windows11_setup.ps1 -Exclude "de,en"

# Or (recommend) - Run the BAT file: 
windows11_setup.bat -Exclude "en"
```

Windows用の#####
セットアップスクリプトを管理者権限で実行します。

**、[CopyQ](https://github.com/hluk/CopyQ) や [AutoHotkey v2](https://www.autohotkey.com/)** など、読み、実行するためのツールをインストールします。 これは、テキスト入力の監視者に必須です。

インストールは完全に自動化され、新しいシステムで2つのモデルを使用する場合は**8-10分かかります。

1。 `setup`フォルダに移動します。
2。**`windows11_setup_with_ahk_copyq.bat`**をダブルクリックします。
* スクリプトは管理者権限を自動でプロンプトします。*
*コアシステム、言語モデル、**AutoHotkey v2**、**CopyQ**をインストールします。*
3. インストールが完了すると、**Aura Dictation**が自動的に起動します。

> **注意:** 事前にPythonやGitをインストールする必要はありません。スクリプトはすべてを処理します。

---

#### 高度/注文の取付け
クライアントツール(AHK/CopyQ)をインストールしたり、特定の言語を除外してディスクスペースを保存したい場合は、コマンドラインでコアスクリプトを実行できます。

```powershell
# Core Setup only (No AHK, No CopyQ)
setup/windows11_setup_with_ahk_copyq.bat

# Exclude specific language models (saves space):
# Exclude English:
setup/windows11_setup_with_ahk_copyq.bat -Exclude "en"

# Exclude German and English:
setup/windows11_setup_with_ahk_copyq.bat -Exclude "de,en"
```

---
</details>


<details>
<summary>UsageXHTMLタグ6X

## 使用法

##1. サービスを開始

###LinuxとmacOSの
単一のスクリプトはすべてを処理します。 メインディクテーションサービスと、バックグラウンドで自動的にファイル監視を開始します。
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

Windowsの#####
サービスの開始は2段階の手動プロセスです**:

1。**メインサービスを開始:** `start_aura.bat`を実行または`python3`でサービスを開始

##2. ホットキーの設定

予測をトリガーするには、特定のファイルを作成するグローバルホットキーが必要です。 クロスプラットフォームの[CopyQ](https://github.com/hluk/CopyQ)を推奨しています。

##### 推奨事項: CopyQ

グローバルなショートカットで CopyQ で新しいコマンドを作成します。

Linux/macOS のコマンド:**
```bash
touch /tmp/sl5_record.trigger
```

**[CopyQ](https://github.com/hluk/CopyQ)を使用するWindowsのためにCommand:**
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


**[AutoHotkey](https://AutoHotkey.com)を使用するWindowsのためにCommand:**
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


##3. ディクティングを開始!
テキストフィールドをクリックし、ホットキーを押し、"リスニング..."通知が表示されます。 明確に話します。, その後、一時停止. 修正されたテキストは入力されます。

</details>

---


<details>
<summary>Advanced 設定 (オプション)</summary>

## 高度の構成(任意)

ローカル設定ファイルを作成すると、アプリケーションの動作をカスタマイズできます。

1。 `config/`ディレクトリに移動します。
2。 `config/settings_local.py_Example.txt`のコピーを作成し、`config/settings_local.py`に名前を変更します。
3. `config/settings_local.py` の編集(`config/settings.py` ファイルから任意の設定を上書き)

この`config/settings_local.py`ファイルはデフォルトでGitによって無視されますので、個人的な変更は更新によって上書きされません。

##プラグイン構造とロジック

システムのモジュール性は、プラグイン/ディレクトリを介して堅牢な拡張を可能にします。

処理エンジンは厳密に**階層優先鎖に付着します**:

1. **モジュールのローディング順序(高い優先度):** コア言語パック(de-DE、en-US)から読み込まれたルールは、プラグイン/ディレクトリ(最後のアルファベット順に読み込まれる)から読み込まれたルールを優先します。
    
2.**ファイル内注文(マイクロ優先度):** 指定したマップファイル(FUZZY MAP pre.py)内では、** 行番号**(最上位)で厳密にルールが処理されます。
    

このアーキテクチャは、コアシステムルールが保護されていることを保証します。プロジェクト固有のまたはコンテキストアウェアルール(CodeIgniterやゲームコントロールなどのもの)は、プラグインによる低優先拡張機能として簡単に追加できます。

</details>

<details>
Windowsユーザー用の<summary>Keyスクリプト</summary>






## Windowsユーザー向けの主要スクリプト

ここに、Windowsシステムでアプリケーションをセットアップ、更新、実行するために最も重要なスクリプトのリストがあります。

### セットアップと更新

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat`: 環境の**最初の一度限りのセットアップ**のためのメインスクリプト。
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : プロジェクトフォルダからこれを実行して、**最新のコードと依存関係を取得**します。

### アプリケーションの実行
*   `start_aura.bat`: **音声認識サービスを開始する**ための主要なスクリプト。

### コアおよびヘルパースクリプト
*   `aura_engine.py`: コアPythonサービス（通常は上記のスクリプトのいずれかによって起動されます）。
*   `get_suggestions.py`: 特定の機能のためのヘルパースクリプト。

</details>



## OSTキー機能とOSの互換性

<details>
OSの互換性のための<summary>Legend</summary>

OS対応のレジェンド:  
* Linux** (例、Archi、Ubuntu)  
* macOS**  は、
*Windows**   は、
* ◀**Android**(モバイル固有の機能の場合)  

---

</details>



##**Core Speech-to-Text (Aura) エンジン**
オフラインの音声認識と音声処理の主力エンジン。

    
<details>
<summary>AuraコアXHTMLタグ2X
Aura-Core/** 🐧 X   ** ** ** ** **
├─ `aura_engine.py` (Aura のメイン Python サービスのオーケストレーション)
├┬ **ライブホットリロード** (Config & Maps) 🐧  
│├ **Secure Private Mapローディング(Integrity-First)** 🔒 X X   
││ * **ワークフロー:** パスワード保護されたZIPアーカイブをロードします。 エスプレッソ
│├ **テキスト処理と修正/** 言語によってグループ化(例:`de-DE`、`en-US`、...)  
│├ 1。 `normalize_punctuation.py`(プンクチュエーションポストトランスクリプションを標準化) 🐧  
│├ 2。 **インテリジェントなプレコレクション** (`FuzzyMap Pre` - [The Primary Command Layer](../docs/CreatingNewPluginModules.i18n/CreatingNewPluginModules-jalang.md)) 🐧  
││ ***ダイナミックスクリプトの実行:** ルールは、API 呼び出し、ファイル I/O などの高度なアクションを実行したり、動的応答を生成したりするために、カスタム Python スクリプト (`on_match_exec`) をトリガーできます。 エスプレッソ
││ ***Cascading 実行:** 規則は順次処理され、その効果は**累積**です。 後でルールは、以前の規則で変更されたテキストに適用されます。  
││ ***最も優先順位の停止基準:** 規則が**フルマッチ**(^...$)を達成した場合、そのトークンの処理パイプライン全体が直ちに停止します。 この仕組みは、信頼性の高い音声コマンドを実装するために不可欠です。 エスプレッソ
│├ 3。 `correct_text_by_languagetool.py`(文法/スタイルの補正のための言語ツールを統合) 🍏  
│├ **4. Ollama AIフォールバックで階層RegEx-Rule-Engine** 🐧 X  
││ *** 決定制御:** RegEx-Rule-Engineを使用して、正確で高優先コマンドとテキスト制御を行います。 エスプレッソ
│├ **Vector-Search Plugin**(レイジーローディング):Ollama/LLMフォールバックレイヤーとローカルのベクトル埋め込みを接続することで、セマンティック検索を有効にします。
││ ※「オラマAI(ローカルLLM)」フォールバック:** *creative 回答、Q&A、および高度な Fuzzy マッチングのオプション、低優先度チェックとして機能します** 決定的なルールが満たされていない場合。  
││ ***Status:**ローカルLM統合。
│└ 5。 **インテリジェントなポストコレクション**(`FuzzyMap`)** - ポストLTの改良** 🐧  
││ * LT固有の出力を修正するために LanguageTool の後に適用される。 前処理レイヤーと同じ厳格なキャスケーディング優先ロジックに従ってください。  
││ ***ダイナミックスクリプトの実行:** ルールは、API 呼び出し、ファイル I/O などの高度なアクションを実行したり、動的応答を生成するために、カスタム Python スクリプト ([on_match_exec](../docs/advanced-scripting.i18n/advanced-scripting-jalang.md)) をトリガーできます。 エスプレッソ
││ ***ファジーフォールバック:** **Fuzzy 類似性 Check** (例えば、85%) は最優先誤差層として機能します。 前項の決定書/キャスケーディング規則が一致(current rule matched is False)が見つからなかった場合にのみ実行され、可能な限り遅いファジーチェックを回避することでパフォーマンスを最適化します。 エスプレッソ
├┬ **モデル管理/**   
│├─ `prioritize_model.py` (使い方に基づいてモデルの読み込み/アンロードを最適化) 🐧  
│└─ `setup_initial_model.py`(初回モデルの設定) 🐧 X X X   
├─ **適応VADタイムアウト** 🐧 X  
├─ **適応ホットキー(スタート/ストップ)** 🐧  
├─ **Instant Language Switching** (モデルプリロードによる実験) 🐧   
├─ **Airflow Orchestration**(DAGベースのワークフロー自動化) 🐧 🍏 🪟
│   ドッカー・UI:`http://localhost:8081` 🍏  
├─ **Trino State Engine** (音声/ターミナル/ウェブごとのインターフェイス-aware構成) 🐧 🍏 🪟
└─  ドッカー・管理者UI:`http://localhost:8084` 🐧X  

**システムユーティリティ/**   
├┬ **言語ツールサーバ管理/**   
│├─ `start_languagetool_server.py` (ローカルランゲージツールサーバーを初期化) 🐧 X X X   
│└─ `stop_languagetool_server.py` (ランゲージツールサーバをシャットダウン) 🐧 🍏 
├─ `monitor_mic.sh` (例:ヘッドセットを使用せずにキーボードとモニター) 🐧 X  

##**モデルとパッケージ管理**  
大規模な言語モデルの堅牢な処理のためのツール。  

**モデル管理/** 🐧  
├─ **Robust Model Downloader** (GitHub Release chunks) 🐧 X X X    🐧 ** ** ** ** ** ** ** ** ** ** ** ** ** **  
├─ `split_and_hash.py` (リポジトリの所有者が大きなファイルを分割し、チェックサムを生成するためのユーティリティ) 🐧  
└─ `download_all_packages.py`(エンドユーザがマルチパートファイルをダウンロード、検証、再構築するためのツール)  

</details>


<details>
<summary>開発と展開ヘルプ</summary>

##**  の開発と展開のヘルプ  
環境設定、テスト、サービスの実行のためのスクリプト。 エスプレッソ  

*Tip: glogg を使用すると、ログファイル内の興味深いイベントを検索するために正規表現を使うことができます。* エスプレッソ  
ログファイルと関連付ける際は、チェックボックスをご確認ください。 エスプレッソ  
https://glogg.bonnefon.org/ エスプレッソ  
    
*Tip: 正規表現パターンを定義した後、`python3 tools/map_tagger.py` を実行して、CLI ツールの検索可能な例を自動的に生成します。 詳細は [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-jalang.md) をご覧ください。*

その後、ダブルクリック
`log/aura_engine.log`
    
**DevHelpers/**   **  
├┬ **仮想環境管理/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧   (`scripts/restart_venv_and_run-server.sh`)  
│└ `scripts/restart_venv_and_run-server.ahk` (ウィンドウズ) 🪟  
├┬ **システム全体のディシテーションの統合/**  
│├ Vosk-System-Listenerの統合 🍏  
│├ `scripts/monitor_mic.sh` (Linux 固有のマイク監視)  
│└ `scripts/type_watcher.ahk`(AutoHotkeyは認識されたテキストを聞き、システム全体でタイプします) 🪟  
└─ **CI/CDのオートメーション/**  
    └─ GitHub ワークフロー拡張 (インストール、テスト、ドキュメントの展開) 🐧  * *(GitHub アクションの実行)*  

</details>

<details>
<summary>実験的特徴</summary>
  
    
##**アップコム/実験的特徴**  
開発中、または開発中の状況下にある機能。  

**実験的特徴/**  
├─ **ENTER AFTER DICTATION REGEX ** 例のアクティベーションルール "(例AplicationThatNotExist|Pi, your personal AI)"  
├┬プラグイン  
│╰┬ **ライブレイジーリロード** (*) 🐧  
(*プラグインのアクティベーション/無効化の変更、およびその設定は、サービス再起動なしの次の処理実行に適用されます。*)  
│ ├ **git command** (git コマンドを送信するためのVoice 制御) 🐧 X X  
│ ├ **wannweil** (所在地ドイツ-Wannweilの地図) 🐧  
│ ├ **Poker Plugin (Draft)** (火かき棒の塗布のための声制御) 🐧  
│ └ **0 A.D. プラグイン (Draft)** (0 A.D. ゲームのVoice制御)   
├─ **セッションの開始または終了時の音声出力** (説明の終了) の  
├─ **Speech Output for Visually Impaired** (Description pending) 🐧   (Description pending) 🐧   (Description pending)  
└─ **SL5 Aura Android Prototype** (まだ完全にオフラインではありません) ◀  

---

*(注:Archi(ARL)やUbuntu(UBT)などの特定のLinuxディストリビューションは、一般的なLinuxのシンボルで覆われています。 詳しい説明は、インストールガイドで覆われている可能性があります。)*
</details>

<details>
<summary>Click では、このスクリプトリスト</summary> を生成するために使用されるコマンドが表示されます。

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>アーキテクチャのグラフィカルな概要</summary>

### アーキテクチャのグラフィカルな概要:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>使用モデル</summary>

## はモデルを使用しました:

推奨: ミラー https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 からモデルを使用する (おそらく高速)

これらのzipモデルは`models/`フォルダに保存する必要があります

`mv vosk-model-*.zip models/`


| モデル | サイズ | ワードエラー率・スピード | ノート | ライセンス |
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1.8G | 5.69(librispeech test-clean)<br/>6.05(tedlium)<br/>29.78(callcenter) | 正確な一般的な米国英語モデル | Apache 2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) | 1.9G | 9.83(Tuda-de test)<br/>24.00(Podcast)<br/>12.82(cv-test)<br/>12.42(ml)<br/>33.26(mtedx) | テレフォニー・サーバー向け大型ドイツモデル | Apache 2.0 | Apache 2.0 |

この表は、サイズ、単語のエラー率、速度、メモ、ライセンス情報など、さまざまなVoskモデルの概要を提供します。


- **Vosk-Models:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **言語ツール:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**言語ツールのライセンス:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

## プロジェクトをサポート
こちらのツールがお役に立ちましたら、お買い求めください! あなたのサポートは未来の改善に燃料を供給するのに役立ちます。

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

