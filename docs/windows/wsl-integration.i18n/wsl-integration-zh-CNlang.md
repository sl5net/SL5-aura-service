# WSL（适用于 Linux 的 Windows 子系统）集成

WSL 允许您直接在 Windows 上运行完整的 Linux 环境。设置完成后，STT shell 集成的工作方式**与 Linux Bash 或 Zsh 指南相同** — shell 功能本身不需要针对 Windows 进行特定的调整。

> **推荐给：** 熟悉 Linux 终端或已安装 WSL 进行开发工作的 Windows 用户。 WSL 提供最忠实的体验和最少的兼容性妥协。

## 先决条件

### 安装 WSL（一次性安装）

**以管理员身份**打开 PowerShell 或 CMD 并运行：

__代码_块_0__

默认情况下，这会在 Ubuntu 上安装 WSL2。出现提示时重新启动计算机。

要安装特定发行版：

__代码_块_1__

列出所有可用的发行版：

__代码_块_2__

### 验证您的 WSL 版本

__代码_块_3__

确保“版本”列显示“2”。如果显示“1”，请升级：

__代码_块_4__

## WSL 内部的 Shell 集成

WSL 运行后，打开 Linux 终端并按照您首选 shell 的 **Linux shell 指南** 进行操作：

|壳牌|指南|
|--------|--------|
| Bash（WSL 默认）| [bash-integration.md](../../linux/bash-integration.i18n/bash-integration-zh-CNlang.md) |
|泽什 | [zsh-integration.md](../../linux/zsh-integration.i18n/zsh-integration-zh-CNlang.md) |
|鱼 | [fish-integration.md](../../linux/fish-integration.i18n/fish-integration-zh-CNlang.md) |
|克什 | [ksh-integration.md](../../linux/ksh-integration.i18n/ksh-integration-zh-CNlang.md) |
| POSIX sh / 破折号 | [posix-sh-integration.md](../../linux/posix-sh-integration.i18n/posix-sh-integration-zh-CNlang.md) |

对于使用 Bash 的默认 Ubuntu/Debian WSL 设置，快速路径是：

__代码_块_5__

## WSL 特定注意事项

### 从 WSL 访问 Windows 文件

您的 Windows 驱动器安装在 `/mnt/` 下：

__代码_块_6__

如果您的项目位于 Windows 文件系统上（例如“C:\Projects\stt”），请将“PROJECT_ROOT”设置为：

__代码_块_7__

将此行添加到“~/.bashrc”（或 shell 的等效内容）“s()”函数的**上方**。

> **性能提示：** 为了获得最佳 I/O 性能，请将项目文件保存在 WSL 文件系统内（例如 `~/projects/stt`），而不是放在 `/mnt/c/...` 上。 WSL 和 Windows 之间的跨文件系统访问速度明显变慢。

### WSL 内的 Python 虚拟环境

在 WSL 中创建并使用标准 Linux 虚拟环境：

__代码_块_8__

函数中的“PY_EXEC”路径（“$PROJECT_ROOT/.venv/bin/python3”）将按原样正常工作。

### 从 Windows 终端运行 `s`

[Windows Terminal](https://aka.ms/terminal) 是在 Windows 上使用 WSL 的推荐方法。它支持每个 WSL 发行版的多个选项卡、窗格和配置文件。从 Microsoft Store 或通过以下方式安装：

__代码_块_9__

在 Windows 终端设置中将 WSL 发行版设置为默认配置文件，以获得最无缝的体验。

### WSL 中的 Docker 和 Kiwix

Kiwix 帮助程序脚本（`kiwix-docker-start-if-not-running.sh`）需要 Docker。安装适用于 Windows 的 Docker Desktop 并启用 WSL 2 集成：

1.下载并安装[Docker Desktop](https://www.docker.com/products/docker-desktop/)。
2. 在 Docker Desktop → 设置 → 资源 → WSL 集成中，启用 WSL 发行版。
3.在WSL内部验证：
__代码_块_10__

### 从 Windows 调用 WSL `s` 函数（可选）

如果您想在不打开 WSL 终端的情况下从 Windows CMD 或 PowerShell 窗口调用 `s` 快捷方式，您可以将其包装：

__代码_块_11__

__代码_块_12__

> `-i` 标志加载一个交互式 shell，以便自动获取您的 `~/.bashrc` （和 `s` 函数）。

＃＃ 特征

- **完全 Linux 兼容性**：所有 Unix 工具（`timeout`、`pgrep`、`mktemp`、`grep`）都可以本机工作 — 无需解决方法。
- **动态路径**：通过 shell 配置中设置的“PROJECT_ROOT”变量自动查找项目根目录。
- **自动重启**：如果后端关闭，它会尝试运行 `start_service` 和本地维基百科服务（Docker 必须正在运行）。
- **智能超时**：首先尝试 2 秒快速响应，然后退回到 70 秒深度处理模式。