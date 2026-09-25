> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../OneClickInstaller.md).*

# 一键安装程序（零配置）

只需点击一次，即可在您的电脑上启动 **Aura**。无需编程知识、终端命令或手动安装 Python。

---

## 零先决条件

你**不**需要：
- 预装 Python
- Git 或代码仓库
- 命令行或终端经验

---

## 快速开始

### 方法1：网页单行命令（最快且推荐用于Linux / macOS）
节省约 30 秒的手动文件处理时间，并在终端中立即启动：

**Linux 和 macOS:**
QQ 网络一环码Berg
```bash
curl -sSL https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | bash
```
或者说
*                                                                           
```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

** 窗户(PowerShell):**
#### Web 单行 CodeBerg

```bash
irm https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | iex
```
或者
#### Web One-Liner github
```bash
irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

方法 2：独立二进制（Windows 和桌面单击）

& 2.1 下载安装器
从 [Lastest GitHub Release] 下载匹配您的操作系统的单个安装器文件 :

- ** 窗户:** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- ** 林纳:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)(英语:[aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)).


QQ 2.2. 运行安装器

将aura-installer-windows.exe.zip更名为aura-installer-windows.ex.

双击已下载文件 。 设置窗口将出现并自动准备环境.

2.3. 开始录音
完成后,Aura创建了桌面快捷键并立即开始收听.

---

□什么是自动发生的?

当运行安装器时, Aura 自动:
- 配置本地,私人语音识别引擎.
- 下载默认语音模式。
- 设置所有必要的系统快捷键和桌面发射器.

---

□ 安装细节和要求

- ** 安装时间:** 大约2至3分钟。
- ** Disk Space Required:** 最小~1.5 GB(根据所选语言模型,最高为2.5 GB).
- ** 安装目录:**
  - ** Linux & macOS:** `~/opt/sl5-aura-service` 存档副本.
  - ** 窗户:** `%LOCALAPPDATA%\sl5-aura-service`

---

□ 下一步

- ** 奶奶-模式:** 在规则文件中输入一个单词,并观看Aura自动创建规则.
- **与Koans一起学习:**探索[Getting Started](../GettingStarted.i18n/GettingStarted-zh-CNlang.md)中的分步概念.
