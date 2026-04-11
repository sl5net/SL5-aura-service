# 命令提示符 (CMD) 集成 (Windows)

为了更轻松地通过 Windows 命令提示符与 STT（语音转文本）CLI 进行交互，您可以创建一个“s.bat”批处理文件并将其放在“PATH”中。这允许您在任何 CMD 窗口中简单地输入“您的问题”。

> **注意：** CMD (cmd.exe) 是旧版 Windows shell，与 PowerShell 或 Unix shell 相比具有显着的局限性。为了获得更丰富的体验，请考虑改用 [PowerShell Integration](.././powershell-integration.i18n/powershell-integration-zh-CNlang.md) 或 [WSL Integration](.././wsl-integration.i18n/wsl-integration-zh-CNlang.md)。

## 设置说明

### 1. 为您的个人脚本创建一个目录（如果尚未完成）

__代码_块_0__

### 2. 将该目录添加到您的 PATH（一次性设置）

打开 **系统属性 → 环境变量** 并将 `%USERPROFILE%\bin` 添加到您的用户 `PATH` 变量中。

或者，在提升的 CMD 提示符下运行此命令（重新打开 CMD 后生效）：

__代码_块_1__

### 3.创建批处理文件

打开记事本或任何文本编辑器并将以下内容保存为“%USERPROFILE%\bin\s.bat”：

__代码_块_2__

### 4. 测试一下

打开一个新的 CMD 窗口（以便加载更新的 PATH）并键入：

__代码_块_3__

## CMD 特定注释

- **没有本机进程超时**：CMD 没有相当于 Unix 的“超时”。该脚本将超时逻辑委托给 PowerShell 的“WaitForExit”。 PowerShell 必须可用（它适用于所有现代 Windows 系统）。

- **帮助脚本**：`update_github_ip.bat` 和 `start_service.bat` 必须存在于您的 `PATH` 或 `%USERPROFILE%\bin` 中。这些是 `update_github_ip` 和 `start_service` shell 函数的 CMD 等效项。
- **Kiwix 脚本的`bash`：如果安装了 WSL，则 CMD 中可以使用 `bash`，并且`.sh` 脚本将直接运行。否则，将 `kiwix-docker-start-if-not-running.sh` 修改为等效的 `.bat`。
- **报价处理**：CMD 具有严格且脆弱的报价规则。如果您的查询包含特殊字符（`&`、`|`、`>`、`<`），请将整个查询用双引号引起来：`s "your & Question"`。
- **`set /p` 限制**：`set /p` 只读取文件的第一行。对于多行输出，使用“type”直接打印文件（如长超时分支中所做的那样）。

＃＃ 特征

- **动态路径**：通过“PROJECT_ROOT”环境变量自动解析路径。
- **自动重启**：如果后端关闭，则调用“start_service.bat”并尝试启动本地维基百科服务。
- **智能超时**：首先尝试 2 秒快速响应，然后退回到 70 秒深度处理模式。