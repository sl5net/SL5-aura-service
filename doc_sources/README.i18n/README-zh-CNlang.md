> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

# ⬟ SL5 气场 – 你的声音。你的规则。

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 100% 离线，隐私优先的语音助手框架。  
> 准确地定义你的声音所做的——从一个单词开始  
> 完整的 Python 脚本。不使用云。数据不会离开你的机器。  
> 可以在终端、浏览器中运行，或作为后台服务运行——适用于 Linux、macOS 和 Windows。

| 👵 初学者 | 🎓 学习者 | 🧑‍💻 开发者 |
|---|---|---|
| [grandma-mode](../../docs/GettingStarted.i18n/GettingStarted-zh-CNlang.md#the-oma-modus-beginner-shortcut)：只需写一个词，Aura 会完成其余部分 | 通过公案学习——一次掌握一个概念 | 完整的 Python 脚本、插件、API 调用 |
| 🗄️ 状态管理 | Trino + Airflow 编排, fzf, CopyQ, 语音/终端命令, 浏览器用户界面 |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ 每次测试约 **2.87 焦耳**（在超过 800 张地图上进行 39 次测试，不使用 LanguageTool，热启动 0.07 秒 / 冷启动 0.36 秒 🌿，使用 [Eco-CI](https://metrics.green-coding.io/index.html) 测量）· 无云计算

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **完整测试套件：** 使用 LanguageTool 对超过 800 张地图进行 94 个测试，预热时间 0.07 秒 / 冷启动时间 0.46 秒 · 无云计算

<details>
<summary>快速开始</summary>

## 快速开始

### 选项 A：一键安装 & 网页安装器（推荐）

适用于 Linux、macOS 和 Windows 的单行命令或独立安装程序：
- **[→ Installer Guide & Direct Downloads](../../docs/OneClickInstaller.i18n/OneClickInstaller-zh-CNlang.md)**

---

* 备选案文B:手动安装(开发者/吉特)

1. 下载或复制此寄存器
2. 运行您的 OS 的设置脚本( 见 XINLIN ECODE0X 文件夹 ):
   - Linux (Arch/Manjaro): `bash setup/manjaro_arch_setup.sh` (中文(简体) ).
   - Linux (Ubuntu/Debian): `bash setup/ubuntu_setup.sh` (英语).
   - Linux (openSUSE): `bash setup/suse_setup.sh` (中文(简体) ).
   - Linux (NixOS): `nix-shell setup/shell.nix`后为`bash setup/nixos_setup.sh`  then.
   QQ实验——作者未试,反馈欢迎!.   
   - macOS: `bash setup/macos_setup.sh` (英语).
   - 视窗: `setup/windows11_setup_with_ahk_copyq.bat`
3. 启动 Aura: `./scripts/restart_venv_and_run-server.sh`
4. 按下你的热门键,然后说话。

---

解装
要删除 SL5 Aura 的背景服务、 自动启动条目和虚拟环境 :
- ** Linux / macOS:** `bash setup/uninstall.sh` 互联网档案馆的存檔,存档日期2013-12-02.
- ** Windows(PowerShell):** `powershell -File setup/uninstall.ps1` (英语).
*(您在 `config/maps/` 中的自定义规则默认保存安全,除非您指定了 `--purge`). *

---


* 系统要求和兼容性**

*   ** Windows:** 完全支持(使用AutoHotkey/PowerShell).
*   **macOS:** QQ 完全支持(使用 AppleScript).
*   ** 利纳克斯(X11/Xorg):**                                                                                                                                                                                                                                                                                                                                                                                                                                                                   完全支持。
*   ** Linux (Wayland):** 完全支持(在 KDE Plasma 6 / Wayland上测试).
*   ** Linux (CachyOS / 基于 Arch的滚动发布):** QQ 完全支持。
    由于 glibc 2.43 相容性,需要 mimalloc (`sudo pacman -S mimalloc`) .
*   **Linux (NixOS):** QQ实验——社区贡献设置,尚未测试.
    如果你尝试,请打开一个问题 或公关与你的发现!    
*   ** 利努克(马尼亚罗):** 新:全系统的热键打开了类似fzf,键盘驱动的接口,这样就可以从桌面上的任何位置运行Aura命令(完全从活动窗口解开). 这种由热键驱动的发射装置目前已在Linux(曼扎罗)上被执行并测试;其他分发可能有效但需要设置. 见[docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-zh-CNlang.md)    


    
SL5 Aura是一个完整的,**离线语音助理**,基于**Vosk**(用于语音到文本)和**语言工具**(用于语法/Style),其特点是一个可选的**本地LLM(Ollama)倒置**,用于创造性响应和高级模糊匹配. 它将你的声音转化为精确的动作和文字,通过可插接的规则系统和动态脚本引擎来设计最终定制.
    
翻译: 该文件也存在于[other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


注:许多文本是英文文件原件的机器翻译,仅供一般指导之用。 如果不一致或含糊不清,英文文本总是优先。 我们欢迎社区帮助改进翻译工作!

</details>

<details>
<summary>演示</summary>

### 📺 终端演示

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **提示：** 想要获得更好的终端体验，请参见 [Zsh Integration](../../docs/linux/zsh-integration.i18n/zsh-integration-zh-CNlang.md)。

### 🎥 视频教程
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*（替代链接：[skipvids.com](https://skipvids.com/?v=BZCHonTqwUw)）*

</details>

<details>
<summary>主要特点</summary>

## 主要特点

*   **离线和私人：** 100% 本地。任何数据都不会离开您的机器。
*   **动态脚本引擎：** 超越文本替换。规则可以执行自定义 Python 脚本 (`on_match_exec`) 来执行高级操作，例如调用 API（例如，搜索维基百科）、与文件交互（例如，管理待办事项列表）或生成动态内容（例如，上下文感知的电子邮件问候语）。
*   **上下文感知规则：** 将规则限制到特定应用程序。使用 `only_in_windows`，您可以确保规则仅在特定窗口标题（例如“终端”、“VS Code”或“浏览器”）处于活动状态时触发。这适用于跨平台（Linux、Windows、macOS）。
*  **高控制转换引擎：** 实现配置驱动、高度可定制的处理管道。规则优先级、命令检测和文本转换纯粹由模糊映射中规则的顺序决定，需要**配置，而不是编码**。
*   **保守的 RAM 使用：** 智能管理内存，仅在有足够的可用 RAM 时才预加载模型，确保其他应用程序（例如您的 PC 游戏）始终具有优先权。
*   **跨平台：** 适用于 Linux、macOS 和 Windows。
*   **完全自动化：** 管理自己的 LanguageTool 服务器（但您也可以使用外部服务器）。
*   **极快：** 智能缓存可确保即时“正在监听...”通知和快速处理。
*   **通过 Trino 进行动态状态管理：** 接口感知配置引擎
    分离 `speech`、`terminal` 和 `web` 的设置 — 无需更改即可更改设置
    影响其他人。包括实时**管理仪表板**（端口 8084）。
</details>

<details>
<summary>🔌 即用型集成</summary>
    
## 🔌 即用型集成

SL5-Aura 配备了一个庞大的生态系统，包含超过 **100 多个预配置插件**。以下是一些亮点：

### OculiX / SikuliX IDE 语音控制
SL5-Aura 为 **OculiX** 和 **SikuliX IDE** 提供一流的语音支持。这种集成允许您“说出”您的自动化代码。

*   **语音到片段：** 说“单击”、“等待”或“查找全部”，该服务会立即将正确的 Python 代码（例如 `click("image.png")`）输入 IDE 中。
*   **Window-Aware：** 该插件是上下文相关的；它仅在 OculiX/SikuliX 窗口聚焦时激活。
*   **智能英语支持：** 针对 `en-US` 进行了优化，特别关注非母语口音（例如德语-英语语音），确保全球社区的高识别准确性。
*   **可扩展：** 使用易于编辑的 `FUZZY_MAP_pre.py` 格式。

> **状态：** 被 OculiX 团队认可为社区插件（请参阅 [Issue #204](https://github.com/oculix-org/Oculix/issues/204)）。

### LibreOffice IDE 语音控制

### 公元前0年 声控

---

</details>


<details>
<summary>文档</summary>

## 文档

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=zh-CN)

如需完整的技术参考，包括所有模块和脚本，请访问我们的官方文档页面。它是自动生成的并且始终是最新的。

[🇬🇧 English](https://sl5net.github.io/SL5-aura-service/README.html) | [🇸🇦 العربية](https://sl5net.github.io/SL5-aura-service/README.i18n/README-arlang.html) | [🇩🇪 Deutsch](https://sl5net.github.io/SL5-aura-service/README.i18n/README-delang.html) | [🇪🇸 Español](https://sl5net.github.io/SL5-aura-service/README.i18n/README-eslang.html) | [🇫🇷 Français](https://sl5net.github.io/SL5-aura-service/README.i18n/README-frlang.html) | [🇮🇳 हिन्दी](https://sl5net.github.io/SL5-aura-service/README.i18n/README-hilang.html) | [🇯🇵 日本語](https://sl5net.github.io/SL5-aura-service/README.i18n/README-jalang.html) | [🇰🇷 한국어](https://sl5net.github.io/SL5-aura-service/README.i18n/README-kolang.html) | [🇵🇱 Polski](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pllang.html) | [🇵🇹 Português](https://sl5net.github.io/SL5-aura-service/README.i18n/README-ptlang.html) | [🇧🇷 Português Brasil](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pt-BRlang.html) | [🇨🇳 简体中文](https://sl5net.github.io/SL5-aura-service/README.i18n/README-zh-CNlang.html)

### 功能亮点
- [Interactive Rule Search & Run](../../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-zh-CNlang.md) — 双面板 `fzf` 规则搜索，实时上下文预览，通过 `Enter`/`Ctrl+R` 即时执行命令，并通过 `Ctrl+E` 集成编辑器。支持全局快捷键（`Super+S`）和通过语音命令预配置的多个专用搜索环境。

### 构建状态

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

👉 **阅读其他语言版本：**

[🇬🇧 English](https://sl5net.github.io/SL5-aura-service/README.html) | [🇸🇦 العربية](https://sl5net.github.io/SL5-aura-service/README.i18n/README-arlang.html) | [🇩🇪 Deutsch](https://sl5net.github.io/SL5-aura-service/README.i18n/README-delang.html) | [🇪🇸 Español](https://sl5net.github.io/SL5-aura-service/README.i18n/README-eslang.html) | [🇫🇷 Français](https://sl5net.github.io/SL5-aura-service/README.i18n/README-frlang.html) | [🇮🇳 हिन्दी](https://sl5net.github.io/SL5-aura-service/README.i18n/README-hilang.html) | [🇯🇵 日本語](https://sl5net.github.io/SL5-aura-service/README.i18n/README-jalang.html) | [🇰🇷 한국어](https://sl5net.github.io/SL5-aura-service/README.i18n/README-kolang.html) | [🇵🇱 Polski](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pllang.html) | [🇵🇹 Português](https://sl5net.github.io/SL5-aura-service/README.i18n/README-ptlang.html) | [🇧🇷 Português Brasil](https://sl5net.github.io/SL5-aura-service/README.i18n/README-pt-BRlang.html) | [🇨🇳 简体中文](https://sl5net.github.io/SL5-aura-service/README.i18n/README-zh-CNlang.html)

---

<details>
<summary>安装</summary>

## 安装

### 🎥 无需审核即可快速安装（Manjaro/Arch 视频）
观看完整的 6 分钟设置过程：
* **下载：** ~3 分钟
* **设置和首次启动：** ~3 分钟（包括欢迎向导）

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


设置过程分为两步：
1.  下载最新版本或主版本 ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) 或将此存储库克隆到您的计算机。
2.  运行适用于您的操作系统的一次性安装脚本。

安装脚本处理一切：系统依赖项、Python 环境，以及直接从我们的 GitHub 版本下载必要的模型和工具（~4GB）以获得最大速度。


#### 适用于 Linux、macOS 和 Windows（可选择排除某些语言）

为了节省磁盘空间和带宽，您可以在安装过程中排除特定的语言模型（`de`，`en`）或所有可选模型（`all`）。**核心组件（LanguageTool，lid.176）始终包含。**

在项目的根目录中打开终端，并运行适合你系统的脚本：

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

#### 对于 Windows
使用管理员权限运行安装脚本。

**安装读取和运行工具，例如 [CopyQ](https://github.com/hluk/CopyQ) 或 [AutoHotkey v2](https://www.autohotkey.com/)**。这是文本输入观察者所必需的。

安装是完全自动化的，在新系统上使用 2 个型号时大约需要 **8-10 分钟**。

1. 导航到 `setup` 文件夹。
2. 双击 **`windows11_setup_with_ahk_copyq.bat`**。
   * *脚本将自动提示管理员权限。*
   * *它安装核心系统、语言模型、**AutoHotkey v2** 和 **CopyQ**。*
3. 安装完成后，**Aura Dictation** 将自动启动。

> **注意：** 您不需要预先安装Python或Git；脚本处理一切。

---

#### 高级 / 自定义安装
如果您不想安装客户端工具（AHK/CopyQ）或想通过排除特定语言来节省磁盘空间，您可以通过命令行运行核心脚本：

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
<summary>使用</summary>

＃＃ 用法

### 1. 启动服务

#### 在 Linux 和 macOS 上
一个脚本可以处理所有事情。它会在后台自动启动主要听写服务和文件观察器。
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

#### 在 Windows 上
启动服务是一个**两步手动过程**：

1.  **启动主服务：** 运行 `start_aura.bat`. 或从 `.venv` 使用 `python3` 启动服务

### 2. 配置您的热键

要触发听写，您需要一个创建特定文件的全局热键。我们强烈推荐跨平台工具[CopyQ](https://github.com/hluk/CopyQ)。

#### 我们的推荐：CopyQ

在 CopyQ 中创建一个带有全局快捷键的新命令。

**Linux/macOS 的命令：**
```bash
touch /tmp/sl5_record.trigger
```

**在使用 [CopyQ](https://github.com/hluk/CopyQ) 时的 Windows 命令：**
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


**在使用 [AutoHotkey](https://AutoHotkey.com) 时的 Windows 命令：**
```sh
; trigger-hotkeys.ahk
; AutoHotkey v2 script
#SingleInstance Force ; Ensures only one instance of the script runs

;===================================================================
; Hotkey to trigger Aura
; Press Ctrl + Alt + T to write the trigger file.
;===================================================================
f9::
f10::
f11::
{
    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("Aura Trigger activated!")
    SetTimer(() => ToolTip(), -1500)
}
```


### 3. 开始听写！
单击任何文本字段，按热键，将出现“正在收听...”通知。说清楚，然后停顿。系统将为您输入更正后的文本。

</details>

---


<details>
<summary>高级配置（可选）</summary>

## 高级配置（可选）

您可以通过创建本地设置文件来自定义应用程序的行为。

1.  导航到 `config/` 目录。
2.  创建 `config/settings_local.py_Example.txt` 的副本并将其重命名为 `config/settings_local.py`。
3.  编辑 `config/settings_local.py`（它会覆盖主 `config/settings.py` 文件中的任何设置）。

默认情况下，Git 会忽略此 `config/settings_local.py` 文件，因此您的个人更改不会被更新覆盖。

### 插件结构和逻辑

系统的模块化允许通过plugins/目录进行强大的扩展。

处理引擎严格遵守**分层优先级链**：

1. **模块加载顺序（高优先级）：** 从核心语言包（de-DE、en-US）加载的规则优先于从 plugins/ 目录（按字母顺序最后加载）加载的规则。
    
2. **文件内顺序（微优先级）：**在任何给定的地图文件 (FUZZY_MAP_pre.py) 中，规则严格按**行号**（从上到下）处理。
    

这种架构确保核心系统规则受到保护，而特定于项目或上下文感知的规则（例如 CodeIgniter 或游戏控件的规则）可以通过插件轻松添加为低优先级扩展。

</details>

<details>
<summary>Windows 用户的关键脚本</summary>






## Windows 用户的关键脚本

以下是设置、更新和运行 Windows 系统上应用程序的最重要脚本列表。

### 设置和更新

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat`：环境的**初始一次性设置**的主要脚本。
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` ：从项目文件夹运行它以**获取最新的代码和依赖项**。

### 运行应用程序
*   `start_aura.bat`：一个主要脚本，用于**启动听写服务**。

### 核心和帮助脚本
*   `aura_engine.py`：核心 Python 服务（通常由上述脚本之一启动）。
*   `get_suggestions.py`：用于特定功能的帮助程序脚本。

</details>



## 🚀 主要功能与操作系统兼容性

<details>
<summary>操作系统兼容性图例</summary>

操作系统兼容性说明：  
*   🐧 **Linux**（例如：Arch、Ubuntu）  
    *   🍏 **macOS**  
*   🪟 **窗户**  
*   📱 **安卓**（针对手机特定功能）  

---

</details>



** 核心语音对文本(Aura)引擎**
    我们的主引擎 离线语音识别和音频处理。

    
<details>
<summary>奥拉-科雷</summary>

** 奥拉-科雷** 🐧 🍏 🪟  
├─ `aura_engine.py` (主平通服务管弦乐于奥拉) 🐧 🍏 🪟  
├┬ ** Live Hot-Reload** (配置和地图) 🐧 🍏 🪟  
│├ ** 安全私人地图加载(完整性-第一)** 🔒  🐧 🍏 🪟  
││ * ** 工作流量:** 装入密码保护的 ZIP 档案 。   
│├ ** 文本处理和校正/** 按语言分组(例如:`de-DE`,`en-US`,.   
│├ 1. `normalize_punctuation.py` (标准标注后标注) 🐧 🍏 🪟  
│├ 2. **智能预校**(`FuzzyMap Pre` - [The Primary Command Layer](../../docs/CreatingNewPluginModules.i18n/CreatingNewPluginModules-zh-CNlang.md)). 🐧 🍏 🪟  
││ * ** 动态脚本执行:** 规则可以触发自定义的Python脚本(`on_match_exec`)来进行高级动作,如API呼叫,文件 I/O,或者生成动态响应.  
││ * ** 处决:** 规则按顺序处理,其效果为**累积**。 后来的规则适用于被更早的规则所修改的文本.  
││ * ** 最高优先级停止标准:** 如果一项规则实现了** 完全匹配** (^...美元),则该令牌的整个处理管道立即停止。 这一机制对于执行可靠的语音指令至关重要。  
│├ 3. `correct_text_by_languagetool.py`(用于语法/风格校正的集成语言工具) 🐧 🍏 🪟  
│├ **4. 与Ollama AI Fallback的分级RegEx规则工程** 🐧 🍏 🪟  
││ * ** 决定控制:**使用RegEx-Rule-Engine进行精确、高度优先的命令和文本控制。  
│├ ** Vector-Search 插件** (Lazy 加载): 通过连接本地矢量嵌入到 Ollama/LLM 倒置层来启用语义搜索 🐧  
││ * ** Ollama AI(当地LLM)倒计时:** 充当**创造性答案的可选,低优先级的检查,QQA,以及高级的"模糊匹配"**,当没有达到决定性规则时.  
││ * ** 现状:** 地方LLM一体化。
│└ 5. ** 智能后修正** (`FuzzyMap`) * * LT后改进** 🐧 🍏 🪟  
││ * 语言工具后用于校正 LT 特定输出. 遵循与"前校正"层相同的严格串联优先级逻辑.  
││ * ** 动态脚本执行:** 规则可以触发自定义的Python脚本([on_match_exec](../../docs/advanced-scripting.i18n/advanced-scripting-zh-CNlang.md))来进行高级动作,如API呼叫,文件一/O,或者生成动态响应.  
││ * ** Fuzzy 退后:** ** Fuzzy 相似度检查**(由阈值控制,例如85%)作为最低优先级错误校正层。 只有在前作的判定/缓存规则运行失败无法找到匹配(当前 rule compared is False)时才会执行,通过尽可能避免缓慢的模糊检查来优化性能.  
├┬ ** 模式管理/**   
│├─ `prioritize_model.py` (根据使用情况优化模型装载/卸载) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (设想首次模式设置) 🐧 🍏 🪟  
├─ ** 动态 VAD 超时** 🐧 🍏 🪟  
├─ ** 自动热键(启动/停止)** 🐧 🍏 🪟  
├─ ** 即时语言切换** (通过模型预装实验) 🐧 🍏         
├─ ** 空管** (基于DAG的工作流程自动化) 🐧 🍏 🪟
│   需要多克 ^ UI: `http://localhost:8081` 🐧 🍏 🪟  
├─ ** 特里诺州发动机**(每次演讲/文字/网络的界面意识配置) 🐧 🍏 🪟
└─  需要多克 ・ 管理 UI: `http://localhost:8084` 🐧 🍏 🪟  

** 系统/**   
├┬ ** 语言工具服务器管理/**   
│├─ `start_languagetool_server.py`(启动本地语言工具服务器) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py`(关闭语言工具服务器) 🐧 🍏 
├─ `monitor_mic.sh`(例如,不使用键盘和监视器而使用头盔) 🐧 🍏 🪟  

### **模型与包管理**  
    用于稳健处理大型语言模型的工具。  

**模型管理/** 🐧 🍏 🪟  
├─ **强大模型下载器**（GitHub 发布分块） 🐧 🍏 🪟  
├─ `split_and_hash.py`（供仓库所有者拆分大文件并生成校验和的工具） 🐧 🍏 🪟  
└─ `download_all_packages.py`（供最终用户下载、验证和重新组装多部分文件的工具） 🐧 🍏 🪟  

</details>


<details>
<summary>开发与部署助手</summary>

** 发展和部署援助人员**  
    用于环境设置,测试,以及服务执行的脚本.  

* Tip: glogg 使您能够使用正则表达式搜索日志文件中的有趣事件。 *     
请在安装与日志文件关联时检查复选框 。    
https://glogg.bonnefon.org/ (中文(简体) ).     
    
*Tip:在定义了您 regex 模式后,运行 `python3 tools/map_tagger.py` 以自动生成CLI 工具的可搜索示例. 详情见[Map Maintenance Tools](../../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-zh-CNlang.md)。 *

然后再双击
`log/aura_engine.log`
    
** 帮助者/**  
├┬ ** 虚拟环境管理/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) (英语). 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk`(窗户) 🪟  
├┬ ** 全系统拼写一体化/**  
│├ Vosk-System-听众集成 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh`(Linux特定麦克风监测) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey为识别文本收听并排出全系统) 🪟  
└─ ** CI/CD 自动化/**  
    └─ 已扩展的 GitHub 工作流( 安装、 测试、 文件部署 ) * * ( GitHub 动作运行) *  

</details>

<details>
<summary>实验特征</summary>
    
***即将到来/实验特征**  
    目前正在开发或处于起草状态。  

** 实验特征/**  
├─ ** 时间轴: 例活化规则"(例活化"That NotExist"-"Pi",即您的个人AI). 🐧  
├┬插件  
│** 《懒惰生活》** (*) 🐧 🍏 🪟  
(* 更换插件激活/停用及其配置,在下一次处理中应用,而不重新启动服务。 *)  
│ ├ ** 命令** (发送 git 命令的声音控制) 🐧 🍏 🪟  
│ ├ ** Wannweil**(德国-Wannweil地点地图) 🐧 🍏 🪟  
│ ├ ** 扑克插件(草案)**(扑克应用程序的声音控制) 🐧 🍏 🪟  
│ └ **0 公元插件(草案)**(公元0游戏的声音控制) 🐧   
├─ ** 开始或结束会话时声音输出** (描述待定) 🐧   
├─ ** 视觉障碍的语音输出** (描述待定) 🐧 🍏 🪟  
└─ **SL5 Aura Android 原型**(尚未完全下线) 📱  

---

*(注:Arch(ARL)或Ubuntu(UBT)等特定的Linux分布被一般Linux QQ符号所覆盖. 安装指南中可以包括详细的区分。 )
</details>

<details>
<summary>单击可查看用于生成此脚本列表的命令</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>架构的图形概述</summary>

### 架构的图形概览：

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>使用的模型</summary>

## 使用的模型：

推荐：使用 Mirror 的模型 https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1（可能更快）

这些压缩模型必须保存到 `models/` 文件夹中

`mv vosk-model-*.zip models/`


QQ 型号 QQ 大小 QQ 文字出错率/ Speed QQ 笔记 QQ 许可证 QQ 许可证
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
[vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) 1.8G 5.69 (librispeech test-clean) <br/>6.05 (terium) <br/>29.78 ( callcenter) 准确的美国通用英语型号 QQ Apache 2.0.
[vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) 1.9G 9.83 (图达-德测试) <br/>24.00 (podcast) <br/>12.82 (cv-test) <br/>12.42 (mls) <br/>33.26 (mtex) <br/>33.26 (mtx) <br/>24.00 (podcast) <br/>12.82 (cv-test) <br/>12.42 (mls) <br/>33.26 (mtx) Q 电话和服务器的德国大模型 XApache 2.0.

本表概述了不同的 Vosk 模型，包括它们的大小、词错误率或速度、备注以及许可信息。


- **Vosk-模型:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **语言工具：**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**LanguageTool 许可:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

## 支持该项目
如果你觉得这个工具有用，请考虑请我们喝杯咖啡！你的支持有助于推动未来的改进。

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

