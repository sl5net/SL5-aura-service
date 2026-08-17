# CLI 工作流程工具安装指南

路径导航器插件中的某些操作依赖于外部命令行实用程序来执行模糊搜索、列出文件和操作剪贴板。如果缺少这些工具，您将在系统控制台中看到警告。

以下是每个支持的操作系统的安装说明。

## 所需的实用程序

* **`fzf`**：通用命令行模糊查找器。
* **`find`**（或`fd`）：标准文件搜索实用程序。
* **剪贴板工具**：用于将输出直接传输到系统剪贴板。
* **Linux:** `xclip`（需要 X11 环境）。
* **macOS：** `pbcopy`（预安装）。
* **Windows：** `clip`（预安装）。
* **`文件`**：确定完整终端预览的文件类型。

---

## 安装说明

### 1. Linux (Arch / Manjaro)
由于您的系统在 Manjaro 上运行，因此您可以使用 pacman 安装所需的软件包：

__代码_块_0__

### 2. Linux (Debian / Ubuntu / Mint)
在基于 Debian 的系统上，使用 `apt`：

__代码_块_1__

### 3.macOS
使用 [Homebrew](https://brew.sh/) 包管理器安装缺少的工具：

__代码_块_2__

### 4. Windows
如果您使用的是 Windows，我们建议通过 [Scoop](https://scoop.sh/) 或 [Winget](https://github.com/microsoft/winget-cli) 安装 `fzf`：

__代码_块_3__
__代码_块_4__