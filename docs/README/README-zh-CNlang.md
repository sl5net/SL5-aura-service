# 系统范围内的离线语音命令或文本，可插拔系统

**⚠️系统要求和兼容性**

* **Windows：** ✅ 完全支持（使用 AutoHotkey/PowerShell）。
* **macOS：** ✅ 完全支持（使用 AppleScript）。
* **Linux (X11/Xorg)：** ✅ 完全支持。推荐以获得最佳体验。
* **Linux (Wayland)：** ⚠️ **有限/实验性。**
* *由于安全限制，全局热键和自动输入通常无法在 Wayland 上运行。*
* *请在登录时切换到 **X11 会话**（例如“Plasma (X11)”或“Ubuntu on Xorg”）以使用所有功能。*


欢迎来到 SL5 Aura 服务！本文档快速概述了我们的主要功能及其操作系统兼容性。

Aura 不仅仅是一个转录器；它也是一个转录器。它是一个强大的离线处理引擎，可以将您的声音转换为精确的动作和文本。

它是一个完整的**离线语音助手**，基于**Vosk**（用于语音转文本）和**LanguageTool**（用于语法/风格）构建，现在具有可选的**本地 LLM (Ollama) 后备**，用于创意响应和高级模糊匹配。它旨在通过可插入规则系统和动态脚本引擎实现最终定制。

X空格符X
翻译：该文档也存在于[other languages](https://github.com/sl5net/SL5-aura-service/tree/master/docs)中。

注意：许多文本是原始英文文档的机器生成翻译，仅供一般指导。如有差异或歧义，始终以英文版本为准。我们欢迎社区帮助改进此翻译！

___

[![SL5 Aura (v0.16.1): HowTo crash SL5 Aura? -  seeh Hierarchical and Recursive Rule Engine](https://img.youtube.com/vi/d98ml86u68g/maxresdefault.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)
（ https://www.youtube.com/watch?v=BZCHonTqwUw 或 https://skipvids.com/?v=BZCHonTqwUw ）

## 主要特点

* **离线和私人：** 100% 本地。任何数据都不会离开您的机器。
* **动态脚本引擎：** 超越文本替换。规则可以执行自定义 Python 脚本（`on_match_exec`）来执行高级操作，例如调用 API（例如，搜索维基百科）、与文件交互（例如，管理待办事项列表）或生成动态内容（例如，上下文感知的电子邮件问候语）。
* **高控制转换引擎：** 实现配置驱动、高度可定制的处理管道。规则优先级、命令检测和文本转换纯粹由模糊映射中规则的顺序决定，需要**配置，而不是编码**。
* **保守的 RAM 使用：** 智能管理内存，仅在有足够的可用 RAM 时才预加载模型，确保其他应用程序（例如您的 PC 游戏）始终具有优先权。
* **跨平台：** 适用于 Linux、macOS 和 Windows。
* **完全自动化：** 管理自己的 LanguageTool 服务器（但您也可以使用外部服务器）。
* **极速：** 智能缓存可确保即时“正在收听...”通知和快速处理。

## 文档

如需完整的技术参考，包括所有模块和脚本，请访问我们的官方文档页面。它是自动生成的并且始终是最新的。

[**Go to Documentation >>**](https://sl5net.github.io/SL5-aura-service/)


### 构建状态
[![Linux Manjaro](https://img.shields.io/badge/Manjaro-Tested-27ae60?style=for-the-badge&logo=manjaro)](https://youtu.be/D9ylPBnP2aQ)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)
[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![Documentation](https://img.shields.io/badge/documentation-live-brightgreen)](https://sl5net.github.io/SL5-aura-service/)

**阅读其他语言版本：**

[🇬🇧 English](README.md) | [🇸🇦 العربية](./README-arlang.md) | [🇩🇪 Deutsch](./README-delang.md) | [🇪🇸 Español](./README-eslang.md) | [🇫🇷 Français](./README-frlang.md) | [🇮🇳 हिन्दी](./README-hilang.md) | [🇯🇵 日本語](./README-jalang.md) | [🇰🇷 한국어](./README-kolang.md) | [🇵🇱 Polski](./README-pllang.md) | [🇵🇹 Português](./README-ptlang.md) | [🇧🇷 Português Brasil](./README-pt-BRlang.md) | [🇨🇳 简体中文](./README-zh-CNlang.md)

---







＃＃ 安装

设置过程分为两步：
1. 下载最新版本或主版本 ( https://github.com/sl5net/Vosk-System-Listener/archive/master.zip ) 或将此存储库克隆到您的计算机。
2. 运行适用于您的操作系统的一次性安装脚本。

安装脚本处理一切：系统依赖项、Python 环境，以及直接从我们的 GitHub 版本下载必要的模型和工具（~4GB）以获得最大速度。


#### 适用于 Linux、macOS 和 Windows（具有可选语言排除）

为了节省磁盘空间和带宽，您可以在安装过程中排除特定语言模型（“de”、“en”）或所有可选模型（“all”）。 **始终包含核心组件（LanguageTool、lid.176）。**

在项目根目录中打开终端并运行适用于您的系统的脚本：

__代码_块_0__

#### 对于 Windows
使用管理员权限运行安装脚本。

**安装一个用于读取和运行的工具，例如[CopyQ](https://github.com/hluk/CopyQ) 或 [AutoHotkey v2](https://www.autohotkey.com/)**。这是文本输入观察者所必需的。

安装是完全自动化的，在新系统上使用 2 个型号时大约需要 **8-10 分钟**。

1. 导航至“setup”文件夹。
2. 双击 **`windows11_setup_with_ahk_copyq.bat`**。
* *脚本会自动提示管理员权限。*
* *它安装核心系统、语言模型、**AutoHotkey v2** 和 **CopyQ**。*
3. 安装完成后，**Aura Dictation** 将自动启动。

> **注意：** 您不需要预先安装Python或Git；脚本处理一切。

---

#### 高级/自定义安装
如果您不想安装客户端工具（AHK/CopyQ）或希望通过排除特定语言来节省磁盘空间，您可以通过命令行运行核心脚本：

__代码_块_1__


---

＃＃ 用法

### 1.启动服务

#### 在 Linux 和 macOS 上
一个脚本可以处理所有事情。它会在后台自动启动主要听写服务和文件观察器。
__代码_块_2__

#### 在 Windows 上
启动服务是一个**两步手动过程**：

1. **启动主服务：** 运行`start_dictation_v2.0.bat`。或使用“python3”从“.venv”服务启动

### 2. 配置您的热键



#### 我们的推荐：CopyQ

使用全局快捷方式在 CopyQ 中创建新命令。

**Linux/macOS 命令：**
__代码_块_3__

**使用 [CopyQ](https://github.com/hluk/CopyQ) 时的 Windows 命令：**
__代码_块_4__


**使用 [AutoHotkey](https://AutoHotkey.com) 时的 Windows 命令：**
__代码_块_5__


### 3. 开始听写！
单击任何文本字段，按热键，将出现“正在收听...”通知。说清楚，然后停顿。系统将为您输入更正后的文本。

---


## 高级配置（可选）

您可以通过创建本地设置文件来自定义应用程序的行为。

1. 导航到“config/”目录。
2. 创建 `config/settings_local.py_Example.txt` 的副本并将其重命名为 `config/settings_local.py`。
3. 编辑 `config/settings_local.py` （它会覆盖主 `config/settings.py` 文件中的任何设置）。

Git（可能）会忽略此“config/settings_local.py”文件，因此您的个人更改（可能）不会被更新覆盖。

### 插件结构和逻辑

系统的模块化允许通过plugins/目录进行强大的扩展。

处理引擎严格遵守**分层优先级链**：

1. **模块加载顺序（高优先级）：** 从核心语言包（de-DE、en-US）加载的规则优先于从 plugins/ 目录（按字母顺序最后加载）加载的规则。
X空格符X
2. **文件内顺序（微优先级）：** 在任何给定的映射文件 (FUZZY_MAP_pre.py) 中，规则严格按 **行号** （从上到下）处理。
X空格符X

这种架构确保核心系统规则受到保护，而特定于项目或上下文感知的规则（例如 CodeIgniter 或游戏控件的规则）可以通过插件轻松添加为低优先级扩展。
## Windows 用户的关键脚本

以下是在 Windows 系统上设置、更新和运行应用程序的最重要脚本的列表。

### 设置和更新
* `setup/setup.bat`：环境的**初始一次性设置**的主脚本。
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `运行 powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

* `update.bat` ：从项目文件夹运行这些**获取最新的代码和依赖项**。

### 运行应用程序
* `start_dictation_v2.0.bat`：**启动听写服务**的主要脚本。

### 核心和帮助脚本
* `aura_engine.py`：核心 Python 服务（通常由上述脚本之一启动）。
* `get_suggestions.py`：用于特定功能的帮助程序脚本。




## 🚀 主要功能和操作系统兼容性

操作系统兼容性图例：  
* 🐧 **Linux**（例如 Arch、Ubuntu）  
* 🍏 **macOS**  
* 🪟 **Windows**  
* 📱 **Android**（针对移动设备特定功能）  

---

### **核心语音转文本 (Aura) 引擎**
我们用于离线语音识别和音频处理的主要引擎。

X空格符X
**光环核心/** 🐧 🍏 🪟  
├─ `aura_engine.py`（编排 Aura 的主要 Python 服务）🐧 🍏 🪟  
├┬ **实时热重载**（配置和地图）🐧🍏🪟  
│├ **安全私有地图加载（完整性第一）** 🔒 🐧 🍏 🪟  
│ │ * **工作流程：** 加载受密码保护的 ZIP 存档。 X空格符X
│├ **文本处理和更正/** 按语言分组（例如 `de-DE`、`en-US`、...）   
│├ 1. `normalize_punctuation.py`（转录后标点符号标准化）🐧 🍏 🪟  
│├ 2. **智能预校正** (`FuzzyMap Pre` - [The Primary Command Layer](docs/CreatingNewPluginModules-zh-CNlang.md)) 🐧 🍏 🪟  
│ │ * **动态脚本执行：**规则可以触发自定义Python脚本（on_match_exec）来执行高级操作，例如API调用、文件I/O或生成动态响应。  
│ │ * **级联执行：**规则按顺序处理，其效果**累积**。后面的规则适用于前面的规则修改的文本。  
│ │ * **最高优先级停止标准：** 如果规则实现 **完全匹配** (^...$)，则该令牌的整个处理管道将立即停止。这种机制对于实现可靠的语音命令至关重要。  
│├ 3. ` Correct_text_by_languagetool.py` (集成LanguageTool用于语法/风格校正) 🐧 🍏 🪟  
│├ **4.具有 Ollama AI 后备功能的分层正则表达式规则引擎** 🐧 🍏 🪟  
│ │ * **确定性控制：** 使用 RegEx-Rule-Engine 进行精确、高优先级的命令和文本控制。  
││ * **Ollama AI（本地法学硕士）后备：** 在不满足确定性规则时，充当**创意答案、问答和高级模糊匹配**的可选、低优先级检查。  
│ │ * **状态：** 本地法学硕士整合。
│└ 5. **智能后校正** (`FuzzyMap`)**– LT后细化** 🐧 🍏 🪟
│ │ * 在 LanguageTool 之后应用以纠正 LT 特定的输出。遵循与预校正层相同的严格级联优先级逻辑。  
││ * **动态脚本执行：**规则可以触发自定义Python脚本（[on_match_exec](docs/advanced-scripting-zh-CNlang.md)）来执行高级操作，例如API调用、文件I/O或生成动态响应。  
││ * **模糊回退：** **模糊相似性检查**（由阈值控制，例如 85%）充当最低优先级的纠错层。仅当前面的整个确定性/级联规则运行未能找到匹配项（current_rule_matched 为 False）时才会执行它，通过尽可能避免缓慢的模糊检查来优化性能。  
├┬ **模型管理/**   
│├─ `prioritize_model.py` (根据使用情况优化模型加载/卸载) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (配置首次模型设置) 🐧 🍏 🪟  
├─ **自适应 VAD 超时** 🐧 🍏 🪟  
├─ **自适应热键（开始/停止）** 🐧 🍏 🪟  
└─ **即时语言切换**（通过模型预加载进行实验）🐧 🍏   

**系统实用程序/**   
├┬ **LanguageTool 服务器管理/**   
│├─ `start_languagetool_server.py` (初始化本地 LanguageTool 服务器) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py` (关闭 LanguageTool 服务器) 🐧 🍏
├─ `monitor_mic.sh` （例如，与耳机一起使用，而不使用键盘和显示器） 🐧 🍏 🪟  

### **模型和包管理**  
用于稳健处理大型语言模型的工具。  

**模型管理/** 🐧 🍏 🪟  
├─ **强大的模型下载器**（GitHub 发布块）🐧 🍏 🪟  
├─ `split_and_hash.py` （仓库所有者分割大文件并生成校验和的实用程序）🐧 🍏 🪟  
└─ `download_all_packages.py` （供最终用户下载、验证和重新组装多部分文件的工具） 🐧 🍏 🪟  


### **开发和部署助手**  
用于环境设置、测试和服务执行的脚本。  

*提示：glogg 使您能够使用正则表达式在日志文件中搜索有趣的事件。*   
安装时请选中该复选框以与日志文件关联。  X空格符X
https://translate.google.com/translate?hl=en&sl=en&tl=zh-CN&u=https://glogg.bonnefon.org/     
X空格符X
*提示：定义正则表达式模式后，运行“python3 tools/map_tagger.py”以自动生成 CLI 工具的可搜索示例。有关详细信息，请参阅 [Map Maintenance Tools](docs/Developer_Guide/Map_Maintenance_Tools-zh-CNlang.md)。*

然后也许双击
`日志/aura_engine.log`
X空格符X
X空格符X
**DevHelpers/**  
├┬ **虚拟环境管理/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ **全系统听写集成/**  
│├ Vosk-系统-监听器集成 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (Linux 专用麦克风监控) 🐧  
│└ `scripts/type_watcher.ahk` （AutoHotkey 侦听已识别的文本并在系统范围内将其输入）🪟  
└─ **CI/CD 自动化/**  
└─ 扩展的 GitHub 工作流程（安装、测试、文档部署）🐧 🍏 🪟 *（在 GitHub 操作上运行）*  

### **即将推出/实验性功能**  
目前正在开发或处于草稿状态的功能。  

**实验功能/**  
├─ **ENTER_AFTER_DICTATION_REGEX** 激活规则示例“(ExampleAplicationThatNotExist|Pi，您的个人 AI)” 🐧  
├┬插件  
│╰┬ **实时延迟重新加载** (*) 🐧 🍏 🪟  
（*对插件激活/停用及其配置的更改将应用于下一次处理运行，无需重新启动服务。*）  
│ ├ **git 命令**（发送 git 命令的语音控制）🐧 🍏 🪟  
│ ├ **万韦尔**（德国-万韦尔位置地图）🐧 🍏 🪟  
│ ├ **扑克插件（草案）**（扑克应用程序的语音控制）🐧 🍏 🪟  
│ └ **0 A.D. 插件（草稿）**（0 A.D. 游戏的语音控制）🐧   
├─ **开始或结束会话时的声音输出**（描述待定）🐧   
├─ **针对视障人士的语音输出**（描述待定）🐧 🍏 🪟  
└─ **SL5 Aura Android 原型**（尚未完全离线）📱  

---

*（注意：通用 Linux 🐧 符号涵盖了特定的 Linux 发行版，例如 Arch (ARL) 或 Ubuntu (UBT)。安装指南中可能会介绍详细的区别。）*









<详情>
<summary>点击查看生成此脚本列表所使用的命令</summary>

__代码_块_6__
</详情>


### 以图形方式查看后面的内容：

![yappi_call_graph](doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

X空格符X
![pydeps -v -o dependencies.svg scripts/py/func/main.py](doc_sources/dependencies.svg)


# 使用的型号：

建议：使用 Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 中的模型（可能更快）

此Ziped模型必须保存到“models/”文件夹中

`mv vosk-model-*.zip 模型/`


|型号|尺寸|字错误率/速度 |笔记|许可证|
| ------------------------------------------------------------------------------------------ | ---- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1.8G | 5.69（librispeech 测试清理）<br/>6.05（tedlium）<br/>29.78（呼叫中心）|精准通用美式英语模型|阿帕奇2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) | 1.9G| 9.83（Tuda-de 测试）<br/>24.00（播客）<br/>12.82（cv-测试）<br/>12.42（mls）<br/>33.26（mtedx）|德国大型电话和服务器模型|阿帕奇2.0 |

此表提供了不同 Vosk 型号的概述，包括其大小、字错误率或速度、注释和许可证信息。


- **Vosk 型号：** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **语言工具：**  
(6.6)[https://languagetool.org/download/](https://languagetool.org/download/)

**LanguageTool许可证：** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---

## 支持该项目
如果您觉得这个工具有用，请考虑给我们买杯咖啡！您的支持有助于推动未来的改进。

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)



IgnorePkg = linux66-nvidia-575xx nvidia-575xx-utils lib32-nvidia-575xx-utils

nvidia-575xx-设置 mhwd-nvidia-575xx