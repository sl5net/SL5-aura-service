# macOS Zsh Shell 集成

> **自 macOS Catalina (10.15) 起的默认 shell。** 如果您使用的是 macOS Mojave 或更早版本，请参阅 [macOS Bash Integration](.././mac-bash-integration.i18n/mac-bash-integration-zh-CNlang.md) 指南。

为了更轻松地与 STT（语音转文本）CLI 进行交互，您可以向 `~/.zshrc` 添加快捷方式功能。这使您只需在终端中输入“您的问题”即可。

## 设置说明

1. 使用您喜欢的编辑器打开您的 Zsh 配置：
__代码_块_0__

2. 将以下块粘贴到文件末尾：

__代码_块_1__

3. 重新加载您的配置：
__代码_块_2__

## macOS 特定注释

- **`timeout` 未内置于 macOS 中。** 在使用此功能之前，请通过 Homebrew 安装它：
__代码_块_3__
安装后，“timeout”可用作“gtimeout”。在上面的函数中添加别名或将“timeout”替换为“gtimeout”：
__代码_块_4__
在“~/.zshrc”中的“s()”函数上方添加别名。

- **`pgrep`** 默认在 macOS 上可用。

- **Python 路径**：确保您的虚拟环境设置在“$PROJECT_ROOT/.venv”。如果您使用“pyenv”或“conda”管理Python，请相应地调整“PY_EXEC”。

＃＃ 特征

- **动态路径**：通过“/tmp”标记文件自动查找项目根目录。
- **自动重启**：如果后端关闭，它会尝试运行“start_service”和本地维基百科服务。
- **智能超时**：首先尝试 2 秒快速响应，然后退回到 70 秒深度处理模式。