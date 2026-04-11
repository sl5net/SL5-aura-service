# PowerShell 集成 (Windows)

为了更轻松地与 STT（语音转文本）CLI 进行交互，您可以向 PowerShell 配置文件添加快捷方式功能。这使您可以在任何 PowerShell 窗口中简单地键入“您的问题”。

> **适用于：** Windows PowerShell 5.1 和 PowerShell 7+（推荐）。 PowerShell 7 可以从 [Microsoft Store](https://aka.ms/powershell) 或通过“winget install Microsoft.PowerShell”安装。

## 设置说明

### 1.允许脚本执行（一次性设置）

PowerShell 默认情况下会阻止脚本。 **以管理员身份**打开 PowerShell 并运行：

__代码_块_0__

### 2. 打开您的 PowerShell 配置文件

__代码_块_1__

如果该文件尚不存在，请先创建它：

__代码_块_2__

### 3. 将以下块粘贴到文件末尾

__代码_块_3__

### 4. 重新加载您的个人资料

__代码_块_4__

## Windows 特定注释

- **Python 路径**：在 Windows 上，虚拟环境二进制文件位于“.venv\Scripts\python.exe”，而不是“.venv/bin/python3”。如果您的设置不同，请调整“$PY_EXEC”。
- **`PROJECT_ROOT` 环境变量**：在系统环境变量中设置此变量，或在配置文件中的函数上方添加以下行：
__代码_块_5__
- **`timeout` / `mktemp`**：这些 Unix 工具本身不可用。上面的脚本使用 PowerShell 原生等效项（带有毫秒超时的“WaitForExit”和“GetTempFileName()”）。
- **`pgrep`**：替换为 `Get-Process -Name "streamlit"`。
- **`start_service` / `update_github_ip`**：这些必须在同一配置文件中的 `s` 函数之前定义为 PowerShell 函数（`Start-Service-STT`、`Update-GithubIp`）。
- **WSL Kiwix 脚本**：如果 `bash` 可用（通过 WSL），则 `.sh` 帮助程序脚本将按原样运行。否则，将其改编为“.ps1”或“.bat”等效文件。
- **多个 PowerShell 版本**：“$PROFILE”指向 Windows PowerShell 5.1 和 PowerShell 7 的不同文件。要检查哪个配置文件处于活动状态，请在每个版本中运行“$PROFILE”。

＃＃ 特征

- **动态路径**：通过“PROJECT_ROOT”环境变量自动查找项目根目录。
- **自动重启**：如果后端关闭，它会尝试运行“Start-Service-STT”和本地维基百科服务。
- **智能超时**：首先尝试 2 秒快速响应，然后退回到 70 秒深度处理模式。