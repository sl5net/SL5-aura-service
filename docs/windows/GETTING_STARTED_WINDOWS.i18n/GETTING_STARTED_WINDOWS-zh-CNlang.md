# Windows 入门

## 第 1 步：运行安装程序
双击“setup/windows11_setup_with_ahk_copyq.bat”。
- 如果出现提示，右键单击→“以管理员身份运行”。
- 该脚本安装 Python、AutoHotkey v2、CopyQ，并下载语音模型 (~4GB)。
- 这大约需要 8-10 分钟。

## 第 2 步：启动 Aura
双击项目文件夹中的“start_aura.bat”。
您应该听到启动声音 - Aura 已准备就绪。

**什么也没发生？**检查日志：
日志\aura_engine.log

## 步骤 3：配置您的热键
安装程序会自动安装 CopyQ。触发听写：
1. 打开 CopyQ → 命令 → 添加命令
2. 将命令设置为：
cmd /c 回显。 > C:\tmp\sl5_record.trigger
3. 指定全局快捷键（例如“F9”）

## 步骤 4：第一次听写
1. 单击任意文本字段
2. 按热键 — 等待“Listening...”通知
3.说“世界你好”
4. 再次按热键 — 出现文本

## 步骤 5：查找语音命令
说：**“Aura Search”** — 将打开一个窗口，其中包含所有可用规则。

## 故障排除
|症状|修复 |
|---|---|
|没有启动声音|检查 `log\aura_engine.log` |
|热键不执行任何操作 |检查 `C:\tmp\sl5_record.trigger` 是否已创建 |
|未输入文字 |检查“type_watcher.ahk”是否在任务管理器中运行 |
|启动时崩溃 |以管理员身份再次运行安装程序 |

> 完整故障排除：[TROUBLESHOOTING.md](../../TROUBLESHOOTING.i18n/TROUBLESHOOTING-zh-CNlang.md)