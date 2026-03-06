### Markdown 文档 (`docs/AHK_SCRIPTS.md`)

# SL5-Aura-Service 的 AutoHotkey 基础设施

由于 Windows 处理文件锁和系统热键的方式与 Linux 不同，因此该项目使用一组 AutoHotkey (v2) 脚本来弥合 Python STT 引擎和 Windows 用户界面之间的差距。

## 脚本概述

### 1. `trigger-hotkeys.ahk`
* **用途：** 用于控制服务的主用户界面。
* **主要特点：**
* 拦截 **F10** 和 **F11** 以开始/停止听写。
* 使用“键盘挂钩”覆盖默认的 Windows 系统行为（例如，F10 激活菜单栏）。
* **部署：** 设计为通过具有“最高权限”的 Windows 任务计划程序进行注册，因此即使用户在管理员级别的应用程序中工作，它也可以捕获热键。

### 2.`type_watcher.ahk`
* **用途：** 充当 STT 管道中的“消费者”。
* **主要特点：**
* 监视 Python 引擎生成的传入“.txt”文件的临时目录。
* **状态机（僵尸映射）：** 实现基于内存的映射，以确保每个文件只输入一次。这可以防止由冗余 Windows 文件系统事件（添加/修改）引起的“双重键入”。
* **安全键入：** 使用 `SendText` 确保在任何活动编辑器中正确处理特殊字符。
* **可靠的清理：** 使用重试逻辑来管理文件删除，以处理 Windows 文件访问锁。

### 3. `scripts/ahk/sync_editor.ahk`
* **目的：** 确保磁盘和文本编辑器（例如 Notepad++）之间的无缝同步。
* **主要特点：**
* **按需保存：** 可以由 Python 触发，在引擎读取文件之前在编辑器中强制使用“Ctrl+S”。
* **对话框自动器：** 自动检测并确认“文件被另一个程序修改”重新加载对话框，创建流畅的实时更新体验。
* **视觉反馈：** 提供短暂的通知框，通知用户正在应用更正。

### 4. `scripts/notification_watcher.ahk`
* **用途：** 为后台进程提供 UI 反馈。
* **主要特点：**
* 监视特定状态文件或事件以向用户显示通知。
* 将“计算”消息 (Python) 的逻辑与“显示”消息 (AHK) 的逻辑分离，确保主 STT 引擎不会被 UI 交互阻塞。


---

### 非管理员后备
如果应用程序在没有管理员权限的情况下运行：
- **功能：** 该服务保持完整功能。
- **热键限制：** 系统保留键（如 **F10**）仍可能触发 Windows 菜单。在这种情况下，建议将热键更改为非系统键（例如“F9”或“Insert”）。
- **任务计划程序：** 如果“AuraDictation_Hotkeys”任务是在管理员安装期间创建的，则即使对于标准用户，该脚本也将以高权限运行。如果没有，“start_dictation.bat”将静默启动本地用户级实例。

---

### 3. Warum“nervige Meldungen”erscheinen und wie man sie im AHK-Code stoppt
Um sicherzustellen，dass das Skript selfiemals den Nutzer mit Popups stört，füge diese“Silent-Flags” oben in deine `.ahk` Dateien ein：

__代码_块_0__

### 4. 热键策略（F10 替代）
Da F10 ohne Admin-Rechte unter Windows fast unmöglich sauber abzufangen ist, könntest du im `trigger-hotkeys.ahk` eine Weiche einbauen:

__代码_块_1__

### Zusammenfassung der Verbesesserungen：
1. **批处理日期：** Nutzt `start "" /b`，um das schwarze Fenster zu vermeiden，und prüft vorher，ob der Admin-Task schon läuft。
2. **透明：** Die Doku erklärt nun offen：“Kein Admin？Kein Problem，nimm einfach eine andere Taste als F10”。
3. **AHK-Skript：** Nutzt `#SingleInstance Force`，um den“一个较旧的实例正在运行”- 对话 zu unterdrücken。

Damit wirkt die Software viel professionaleller（“Smooth”），da sie im Hintergrund startet，ohne dass der Nutzer mit technischen Details oder Bestätigungsfenstern konfrontiert wird。
X空格符X
X空格符X
---

### 为什么本文档很重要：
通过记录 **“僵尸地图”** 和 **“任务计划程序/管理员”** 要求，您可以向其他开发人员（以及未来的您）解释为什么代码比简单的 Linux 脚本更复杂。它将“奇怪的解决方法”转变为“针对 Windows 限制的工程解决方案”。

(s,29.1.'26 11:02 星期四)