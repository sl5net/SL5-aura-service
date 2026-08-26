# Windows 自动启动

#start_aura.bat

请检查 SL5net Aura 项目文件夹中的文件 `start_aura.bat`。

**选项 A — 启动文件夹（最简单、可见的控制台窗口）**

1. 创建一个批处理文件，例如`C:\Users\<您的名字>\Scripts\aura_engine.bat`:

__代码_块_0__

2. 按“Win + R”，输入“shell:startup”，然后按 Enter。这将打开：
`C:\Users\<您的名字>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
3. 右键单击该文件夹 → **新建 → 快捷方式** → 将其指向 `aura_engine.bat`。现在它在每次登录时运行。

**选项 B — 任务计划程序（推荐：隐藏，无窗口闪烁）**

在 PowerShell 中运行一次：

__代码_块_1__

这将创建一个任务“AuraEngine”，该任务在每次登录时触发，完全在后台运行，并写入 Linux/Mac 版本中使用的相同“aura_engine.log”。

**不注销测试：**

__代码_块_2__

将 `Ubuntu` 调整为您的实际发行版名称 - 检查：

__代码_块_3__

**检查它是否已注册：**

__代码_块_4__

**禁用/删除：**

__代码_块_5__

您实际上是通过 Windows 计算机上的 WSL 运行此项目，还是需要对“restart_venv_and_run-server.sh”进行本机 Windows/PowerShell 重写（不涉及 WSL）？