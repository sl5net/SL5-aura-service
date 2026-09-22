> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

# ⬟ SL5 氛围 – 你的声音。你的规则。

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 100% 离线，隐私优先的语音助手框架。  
> 准确定义你的声音所做的事情——从一个单词开始
> 完整的 Python 脚本。无云端。数据不会离开你的机器。
> 可以在终端、浏览器中运行，或作为后台服务运行——适用于 Linux、macOS 和 Windows。

| 👵 初学者 | 🎓 学习者 | 🧑‍💻 开发者 |
|---|---|---|
| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-zh-CNlang.md#the-oma-modus-beginner-shortcut)：只需写一个单词，Aura 会处理其余部分 | 通过公案学习——一次一个概念 | 完整的 Python 脚本、插件、API 调用 |
| 🗄️ 状态管理 | Trino + Airflow 编排, fzf, CopyQ, 语音/终端命令, 浏览器用户界面 |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **每次测试约 2.87 焦耳** (39 tests without LanguageTool across >800 maps @ 0.07s warm / 0.36s cold 🌿 measured with XMDLINK1X) · 无云计算

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **完整测试套件：** 使用 LanguageTool 对超过 800 张地图进行了 94 个测试，预热时间 0.07 秒 / 冷启动时间 0.46 秒 · 无云计算

<details>
XHTML标签2X快速开始XHTML标签3X

## 快速开始

### 选项 A：一键安装和网页安装器 (Recommended)

适用于 Linux、macOS 和 Windows 的单行命令或独立安装程序：
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-zh-CNlang.md)**

---

* 备选案文B:手动安装(开发者/吉特)

1. 下载或复制此存储库
2. 运行您的OS的设置脚本(见 `setup/` 文件夹):
- Linux(Arch/Manjaro):`bash setup/manjaro_arch_setup.sh`号卫星
- Linux(乌邦图/德比安):`bash setup/ubuntu_setup.sh`
- Linux (openSUSE): `bash setup/suse_setup.sh` (英语).
- Linux (NixOS):`nix-shell setup/shell.nix`,然后是`bash setup/nixos_setup.sh`
QQ实验——作者未试,反馈欢迎!.    存档副本.  
- 马可斯:`bash setup/macos_setup.sh`
- 视窗:`setup/windows11_setup_with_ahk_copyq.bat`
3. 启动奥拉:`./scripts/restart_venv_and_run-server.sh`
4. 按下你的热门键并讲话——------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

---

解装
要删除 SL5 Aura 的背景服务、 自动启动条目和虚拟环境 :
- **Linux/macOS:** `bash setup/uninstall.sh`
- ** Windows(PowerShell):** `powershell -File setup/uninstall.ps1`(电站壳):
*(您在 `config/maps/` 中的自定义规则默认保存安全,除非您指定了 `--purge`). *

---


* 系统要求和兼容性**

* ** Windows:** 完全支持(使用AutoHotkey/PowerShell).
* **macOS:** 完全支持(使用 AppleScript).
* ** 利纳克斯(X11/Xorg):**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     完全支持。
* **Linux (Wayland):** 完全支持(在 KDE Plasma 6 / Wayland上测试).
* **Linux (CachyOS / Arch-based 滚动放出):** ✅. 完全支持。
由于 glibc 2.43 相容性,需要 mimalloc (`sudo pacman -S mimalloc`) .
***Linux (NixOS):**QQ实验——由社区贡献的设置,尚未测试.
如果你尝试,请打开一个问题 或公关与你的发现!    存档副本.  
* ** 利纳克(马尼亚罗):** 新:全系统的热键打开了类似fzf,键盘驱动的接口,这样就可以从桌面上的任何位置运行Aura命令(完全从活动窗口解开). 这种由热键驱动的发射装置目前已在Linux(曼扎罗)上被执行并测试;其他分发可能有效但需要设置. 参见[docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-zh-CNlang.md)   


    
SL5 Aura是一个完整的,**离线语音助理**,基于**Vosk**(用于语音到文本)和**语言工具**(用于语法/Style),其特点是一个可选的**本地LLM(Ollama)倒置**,用于创造性响应和高级模糊匹配. 它将你的声音转化为精确的动作和文字,通过可插接的规则系统和动态脚本引擎来设计最终定制.
    
翻译: 该文件也存在于[other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


注:许多文本是英文文件原件的机器翻译,仅供一般指导之用。 如果不一致或含糊不清,英文文本总是优先。 我们欢迎社区帮助改进翻译工作!

</details>

<details>
<summary> 德莫克HTMLTAG3X 德莫克HTMLTAG1X 德莫克HTMLTAG3X 德莫克HTMLTAG1X 德莫克HTMLTAG1X 德莫克HTMLTAG3X 德莫克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克克

### 📺 终端演示

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **提示：** 为了获得更好的终端体验，请参见 [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-zh-CNlang.md)。

### 🎥 视频教程
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(备用链接：[skipvids.com](https://skipvids.com/?v=BZCHonTqwUw))*

</details>

<details>
XHTML标签2X主要特性XHTML标签3X

□ 关键特性

* ** Offline & Private:** 100%本地。 没有数据离开你的机器。
* ** 动态脚本引擎:** 超越文本替换。 规则可以执行自定义的 Python 脚本(`on_match_exec`)来进行高级动作,如调用API(例如搜索维基百科),与文件互动(例如管理待办事宜列表),或生成动态内容(例如了解上下文的电子邮件问候).
* ** 内容了解规则:** 将规则限于具体应用。 使用`only_in_windows`,只有在特定窗口标题(如"Terminal","VS代码"或"浏览器")活动时,才能确保规则触发. 这个工作跨平台(Linux,Windows,macOS).
* ** 高控制转换引擎:** 实施配置驱动,高度自定义的加工管线. 规则优先权,命令检测,和文本转换完全由"模糊地图"中规则的相继顺序决定,需要**配置,而不是编码**.
*** 保守内存的使用:** 智能管理内存,只有在有足够的免费RAM可用的情况下才会预装模型,确保其他应用程序(如你的PC游戏)总是有优先权.
* ** 交叉-公式:** 在Linux,macOS,和Windows上工作.
* ** Fully Automatic:** 管理自有的"语言工具"服务器(但您也可以使用外部服务器).
***快闪快:**智能卡通能确保即时"听..."通知和快速处理.
* 通过Trino的动态国家管理:** 界面感知配置引擎
将 `speech` 、 `terminal` 和 `web` 的设置区分开来 — 在不修改的情况下更改一个
影响他人。 包括一个实时的**Admin Dashboard**(8084港)。
</details>

<details>
<summary> 准备使用集成</summary>
    
## 🔌 即用集成

SL5-Aura 配备了一个庞大的生态系统，拥有超过 **100+ 个预配置插件**。以下是一些亮点：

OculiX / SikuliX IDE 语音控制器
SL5-Aura为**奥库利X**和**SikulIX IDE**提供一等语音支持. 这种集成使您能够"说出"您的自动化代码.

* ** 对片段:** 表示"点击","等",或"查找全部",服务即刻将正确的Python代码(如`click("image.png")`)输入到IDE.
* ** Window-Award:** 该插件对上下文敏感;它只在OculiX/SikuliX窗口被聚焦时激活.
* ** Smart English Support:** 为`en-US`优化,并特别关注非本地口音(如德英口音),确保了全球社会的高度识别精度.
*** 可延长:** 使用易编辑的`FUZZY_MAP_pre.py`格式.

> ** 现状:** 被OculiX团队确认为社区插座(参见[Issue #204](https://github.com/oculix-org/Oculix/issues/204)).

自由办公室 IDE 语音控制

公元0年 语音控制

---

</details>


<details>
<summary> 文档 </summary>

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)

□ 文档

关于包括所有模块和脚本在内的完整技术参考,请访问我们的正式文件页。 它是自动生成的,并且总是最新的.

👉 [**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)

· 特性焦点
-[Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-zh-CNlang.md)-双板`fzf`规则搜索,现场上下文预览,通过`Enter`/`Ctrl+R`即时命令执行,并通过`Ctrl+E`实现编辑器集成. 由一款全球热键(`Super+S`)和多款专用搜索环境通过语音指令预配置而来支持.

++ 构建状态

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

** 用其他语言读取:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-zh-CNlang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-zh-CNlang.md) | [🇪🇸 Español](../README.i18n/README-eslang-zh-CNlang.md) | [🇫🇷 Français](../README.i18n/README-frlang-zh-CNlang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-zh-CNlang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-zh-CNlang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-zh-CNlang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-zh-CNlang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-zh-CNlang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-zh-CNlang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang.md)

---

<details>
XHTMLTAG11 安装</summary>

□ 安装

QQ 快速安装不节制(马扎罗/Arch视频)
观看完整的6分钟设置过程 :
* ** 下载:** ~3分钟
* ** Setup & First Start: ** ~3分(包括欢迎向导)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


设置是一个分两步走的过程:
1. 下载最新版本或主机(https://github.com/sl5net/SL5-aura-service/archive/master.zip)或复制此存储器到您的计算机。
2.运行您的操作系统的一次性设置脚本.

设置脚本处理一切:系统依赖性,Python环境,以及直接从我们的GitHub发行中下载必要的模型和工具(~4GB),以达到最高速度.


QQ 对于 Linux, macOS, 和 Windows (包含可选语言排除)

为了保存磁盘空间和带宽,可以在设置期间排除特定语言模型(`de`,`en`)或所有可选模型(`all`). ** 核心组件(LanguageToole, id.176)始终包括在内。 **

在工程的根目录中打开终端并运行您的系统的脚本 :

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

QQ 用于窗口
以管理员权限运行设置脚本 。

** 安装一个读取并运行的工具,例如:[CopyQ](https://github.com/hluk/CopyQ)或[AutoHotkey v2](https://www.autohotkey.com/)**. 此为出字观者所取.

安装是完全自动化的,在使用2个型号的新型系统时需要约**8-10分钟**.

1. 导航到 `setup` 文件夹.
2.双击QQINLINECODE1X**.
* 脚本将自动提示管理员权限。 *
**它安装了核心系统,语言模型,**AutoHotkey v2**和**CopyQ**.*
3. 一旦安装完成,** Aura Dictation**将自动发射。

> ** 说明:** 您不需要事先安装 Python 或 Git; 脚本处理所有事务 。

---

高级/ 自定义安装
如果您不愿安装客户端工具(AHK/CopyQ)或希望通过排除特定语言来保存磁盘空间,可以通过命令行运行核心脚本:

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
<summary> Usage</summary> (英语).

□ 使用量

1. 启动服务

在 Linux 和 macOS 上
单行本处理一切. 它在背景中自动启动主拼写服务和文件监视器.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

QQ 在窗口上
开始服务是一个 ** 二步手动过程 **:

1. ** 启动主服务:** 运行 `start_aura.bat`.或从`.venv`开始与`python3`的服务.

& 2. 配置您的热键

要触发拼写, 您需要一个创建特定文件的全局热键 。 我们高度推荐跨平台工具[CopyQ](https://github.com/hluk/CopyQ).

我们的建议:复制Q

在 CopyQ 中创建一个带有全局快捷键的新命令 。

** Linux/macOS的命令:**
```bash
touch /tmp/sl5_record.trigger
```

** 当使用 [CopyQ](https://github.com/hluk/CopyQ)时, Windows 命令:**
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


** 当使用 [AutoHotkey](https://AutoHotkey.com)时, Windows 命令:**
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


3. 开始指挥!
点击任意文本字段, 按下您的热键, 将会出现“ 听... ” 通知 。 说清楚,然后暂停。 将为您输入更正文本 。

</details>

---


<details>
<summary>先进配置(可选) </summary>

□ 高级配置( 可选)

您可以通过创建本地设置文件来定制应用程序的行为 。

1. 导航到 `config/` 目录.
2. 创建`config/settings_local.py_Example.txt`并重命名为`config/settings_local.py`.
3. 编辑 `config/settings_local.py`(它覆盖了主`config/settings.py`文件中的任何设置).

这个`config/settings_local.py`文件默认被Git忽略了,因此您的个人更改不会被更新所覆盖.

++ 插件结构和逻辑

系统的模块化允许通过插件/目录进行强大的扩展.

处理引擎严格遵循**高优先级链**:

1. ** 模块装入顺序(高度优先):** 从核心语言包(de-DE, en-US)中加载的规则优先于从插件/ 目录中加载的规则(上个字母加载).
    
2. ** 在文件顺序(Micro优先级):** 在任何给定的地图文件中(FUZZY MAP pre.py),规则严格由**行号**(从上到下)处理.
    

这种架构确保了核心系统规则得到保护,而项目特定规则或上下文意识规则(如用于CodeIgniter或游戏控制的规则)可以通过插件作为低优先级扩展而容易被添加.

</details>

<details>
用于 Windows 用户的 <summary>Key 脚本</summary>






□ Windows 用户的密钥脚本

以下是一个Windows系统设置,更新,运行应用程序的最重要脚本列表.

QQ 设置更新

*   `chmod +x update.sh; ./update.sh`
* `setup/setup.bat`:**首次一次性设置环境**的主要剧本.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

* `update.bat`:从项目文件夹运行到**获取最新的代码和依赖**.

QQ 运行应用程序
* `start_aura.bat`:一个主要脚本来**启动口述服务**.

& 帮助脚本
* `aura_engine.py`:核心Python服务(通常由上面的脚本之一开始).
* `get_suggestions.py`:用于特定功能的辅助脚本.

</details>



# # # # 关键特性和操作系统兼容性

<details>
<summary> OS相容性</summary>

OS兼容性图例:   
*** 利纳克斯**(如Arch, Ubuntu)  
* * * 马科斯* SPACEBREAKX  
* 温多斯 SPACEBREAKX  
***Android**(用于移动特性)  

---

</details>



** 核心语音对文本(Aura)引擎**
我们的主引擎 离线语音识别和音频处理。

    
<details>
<summary>AURA-Core</summary> 机车牵引电动机
** Aura-Core/** SPACEBREAKX  
├─ `aura_engine.py` (主Python 服务 管弦乐 Aura) QQ SPACEBREAKX  
├┬ ** 生活热重装** (图和图) * * * * * * * * SPACEBREAKX  
│├ ** 安全私人地图加载(完整性-第一)** SPACEBREAKX  
││ * ** 工作流量:** 装入密码保护的 ZIP 档案 。    存档副本.  
│├ ** 文本处理和校正/** 按语言分组(例如:`de-DE`,`en-US`,.)   
│├ 1. `normalize_punctuation.py` (标准字后标注) QQ SPACEBREAKX  
│├ 2. **智能预更正**(`FuzzyMap Pre`-[The Primary Command Layer](../docs/CreatingNewPluginModules.i18n/CreatingNewPluginModules-zh-CNlang.md)) QQQ SPACEBREAKX  
││ * ** 动态脚本执行:** 规则可以触发自定义的Python脚本(`on_match_exec`)来进行高级动作,如API呼叫,文件 I/O,或者生成动态响应.    存档副本.  
││ * ** 处决:** 规则按顺序处理,其效果为**累积**。 后来的规则适用于由更早的规则所修改的文本.   
││ * ** 最高优先级停止标准:** 如果规则实现** 完全匹配** (^...美元),则该令牌的整个处理管道立即停止。 这一机制对于执行可靠的语音指令至关重要。    存档副本.  
│├ 3. `correct_text_by_languagetool.py`(用于语法/风格校正的集成语言工具) QQ SPACEBREAKX  
│├ **4. 与Ollama AI Fallback** 的等级化RegEx规则引擎  
││ * ** 决定性控制:** 用于精确、高度优先的命令和文本控制。    存档副本.  
│├ ** Vector-Search 插件** (Lazy 加载): 通过连接本地的矢量嵌入与 Ollama/ LLM 倒置层 QQSPACEBREAKX 启用语义搜索  
││ * ** Ollama AI(当地LLM):** 作为对**创造性答案的可选低优先级检查,QQA,以及高级模糊匹配** 当没有达到决定性规则时.   
││ * ** 现状:** 地方LLM一体化。
│└ 5. ** 智能后更正** (`FuzzyMap`) * * LT后改进** * * * * * * * * * * SPACEBREAKX  
││ * 在LanguageTool之后用于校正LT特定输出. 遵循与前校正层相同的严格串联优先级逻辑.   
││ * ** 动态脚本执行:** 规则可以触发自定义的Python脚本([on_match_exec](../docs/advanced-scripting.i18n/advanced-scripting-zh-CNlang.md))来进行高级动作,如API呼叫,文件一/O,或者生成动态响应.    存档副本.  
││ * * Fuzzy 退后:** ** Fuzzy 相似度检查**(由阈值控制,例如85%)作为最低优先级错误校正层。 只有在前作的判定/缓存规则运行失败无法找到匹配(当前 rule compared is False)时才会执行,通过尽可能避免缓慢的模糊检查来优化性能.    存档副本.  
├┬ ** 模型管理/**   
│├─ `prioritize_model.py`(根据用法优化型号加载/卸载) QQQ SPACEBREAKX  
│└─ `setup_initial_model.py` (配置初代模式设置) QQQ SPACEBREAKX  
├─ ** 动态 VAD 超时**  
├─ ** 自动热键(启动/停止)**  
├─ ** 即时语言切换** (通过型号预装实验) 🍏   
├─ ** 空管** (基于DAG的工作流程自动化) 🐧 🍏 🪟
│   需要多克 ^ UI: `http://localhost:8081` ××× SPACEBREAKX  
├─ ** 特里诺州发动机**(每次演讲/文字/网络的界面意识配置) 🐧 🍏 🪟
└─  需要多克 ・ 管理 UI: `http://localhost:8084` → QQ SPACEBREAKX  

** 系统/**   
├┬ **语言工具服务器管理/**   
│├─ `start_languagetool_server.py`(启动本地语言工具服务器) QQQ SPACEBREAKX  
│└─ `stop_languagetool_server.py`(关闭语言工具服务器) 🐧 🍏 
├─ `monitor_mic.sh`(例如,用于不使用键盘和监视器的头盔) QQQ SPACEBREAKX  

** 模型和软件包管理  
大力处理大型语言模型的工具。  

** 管理模式/** SPACEBREAKX  
├─ ** Robust 模型下载器** (GitHub Release blocks) * * * * * * SPACEBREAKX  
├─ `split_and_hash.py`(Repo所有者可以分割大文件和生成校验和) QQQ SPACEBREAKX  
└─ `download_all_packages.py`(供最终用户下载、核实和重新组合多部分文件使用的工具) QQ SPACEBREAKX  

</details>


<details>
<summary> 开发和部署辅助人员</summary>

** 发展和部署援助人员  
用于环境设置,测试,以及服务执行的脚本.    存档副本.  

* Tip: glogg 使您能够使用正则表达式搜索日志文件中的有趣事件。 *    存档副本.  
请在安装与日志文件关联时检查复选框 。    存档副本.  
https://glogg.bonnefon.org/ (中文(简体) ).    存档副本.  
    
*Tip:在定义了您 regex 模式后,运行 `python3 tools/map_tagger.py` 以自动生成CLI 工具的可搜索示例. 详情见[Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-zh-CNlang.md)。 *

然后再双击
`log/aura_engine.log`
    
** Develfers/ SPACEBREAKX 互联网档案馆的存檔,存档日期2014-12-02.  
├┬ ** 虚拟环境管理/SPACEBREAKX  
│├ `scripts/restart_venv_and_run-server.sh` (英语:Linux (macOS)) 🐧 (SPACEBREAKX).  
│└ `scripts/restart_venv_and_run-server.ahk`(窗户) SPACEBREAKX  
├┬ ** 全系统语法融合/SPACEBREAKX  
│├ Vosk-System-Listener 集成 QQ SPACEBREAKX 互联网档案馆的存檔,存档日期2011-10-02.  
│├ `scripts/monitor_mic.sh` (Linux特有麦克风监控) SPACEBREAKX  
│└ `scripts/type_watcher.ahk` (AutoHotkey听取公认文本并排出全系统) SPACEBREAKX  
└─ ** CI/CD 自动化/SPACEBREAKX  
    └─ 已扩展的 GitHub 工作流程( 安装、 测试、 文件部署) QQ QQ * ( GitHub 动作运行) SPACEBREAKX  

</details>

<details>
<summary> 实验特性 </summary>
    
** 即将进入/实验性特征  
目前正在开发或处于起草状态的特点。  

** 实验特征/SPACEBREAKX  
├─ ** 时间轴: 例活化规则"(例活化"That NotExist"Pi,即您个人的AI)" QQSPACEBREAKX  
├┬插件  
│################################################################################################################################################################################################################################################################  
(* 插件活化/停用的变化及其配置在下一次处理运行时不重新启动服务。 *)   
│ ├ ** git 命令 ** (发送 git 命令的声音控制) QQ SPACEBREAKX  
│ ├ ** Wannweil ** (德国-Wannweil地点地图)  
│ ├ ** 扑克插件(草案)** (扑克应用程序的声音控制) * * * * * * SPACEBREAKX  
│ └ **0 公元插件 (草案)** (公元0 游戏的声音控制)   
├─ ** 开始或结束会话时声音输出** (描述待定)   
├─ **视觉障碍的语音输出**(描述待定) * * * * * * SPACEBREAKX  
└─ **SL5 Aura Android原型**(尚未完全下线) SPACEBREAKX  

---

*(注:Arch(ARL)或Ubuntu(UBT)等特定的Linux分布被一般Linux QQ符号所覆盖. 安装指南中可以包括详细的区分。 )
</details>

<details>
<summary>Click 查看用于生成此脚本列表的命令</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>A 架构图形概述 </summary>

建筑图解:

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary> 已使用型号 </summary>

□ 用过的模型 :

建议:使用镜像网站https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1中的模型(可能更快)

这些已拉链的模型必须保存到 `models/` 文件夹

`mv vosk-model-*.zip models/`


QQ 型号 QQ 大小 QQ 文字出错率/ Speed QQ 笔记 QQ 许可证 QQ 许可证
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
[vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) 1.8G 5.69 (librispeech test-clean) <br/>6.05 (terium) <br/>29.78 ( callcenter) 准确的美国通用英语型号 QQ Apache 2.0.
[vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) 1.9G 9.83 (图达-德测试) <br/>24.00 (podcast) <br/>12.82 (cv-test) <br/>12.42 (mls) <br/>33.26 (mtex) <br/>33.26 (mtx) <br/>24.00 (podcast) <br/>12.82 (cv-test) <br/>12.42 (mls) <br/>33.26 (mtx) Q 电话和服务器的德国大模型 XApache 2.0.

本表概述了不同的沃斯克模型,包括它们的大小,词错误率或速度,注释,以及许可证信息等.


- ** Vosk-模型:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **语言工具:SPACEBREAKX  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**语言工具的语素:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

□ 支持项目
如果你觉得这个工具有用,请考虑给我们买杯咖啡! 你们的支持有助于未来的改进。

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

