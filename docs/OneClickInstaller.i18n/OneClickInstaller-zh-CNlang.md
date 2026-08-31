# 一键式安装程序（零安装）

只需单击一下，即可在您的计算机上启动并运行 **Aura**。无需编程知识、终端命令或手动 Python 设置。

---

## 零先决条件

您**不需要**需要：
- 预装Python
- Git 或代码存储库
- 命令行或终端经验

---

## 快速入门

### 方法 1：Web One-Liner（最快且推荐用于 Linux / macOS）
节省大约 30 秒的手动文件处理时间并立即在终端中启动：

**Linux 和 macOS：**

__代码_块_0__

**Windows（PowerShell）：**
__代码_块_1__

方法 2：独立二进制（Windows 和桌面单击）

### 2.1 下载安装程序
从 [最新 GitHub 版本] 下载与您的操作系统匹配的单个安装程序文件：

- **Windows：** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **Linux：** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS：** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2。运行安装程序

将 aura-installer-windows.exe.zip 重命名为 aura-installer-windows.exe

双击下载的文件。将出现一个设置窗口并自动准备环境。

### 2.3。开始听写
完成后，Aura 会创建一个桌面快捷方式并立即开始收听。

---

## 自动发生什么？

当您运行安装程序时，Aura 会自动：
- 配置本地私有语音识别引擎。
- 下载默认语音模型。
- 设置所有必要的系统快捷方式和桌面启动器。

---

## 安装细节和要求

- **安装持续时间：** 大约 2-3 分钟。
- **所需磁盘空间：** 最小 ~1.5 GB（最多 2.5 GB，具体取决于所选语言模型）。
- **安装目录：**
- **Linux 和 macOS：** `~/opt/sl5-aura-service`
- **Windows:** `%LOCALAPPDATA%\sl5-aura-service`

---

## 后续步骤

- **奶奶模式：** 在规则文件中输入一个单词并观看 Aura 自动创建规则。
- **与 Koans 一起学习：** 探索 [Getting Started](../GettingStarted.i18n/GettingStarted-zh-CNlang.md) 中的逐步概念。