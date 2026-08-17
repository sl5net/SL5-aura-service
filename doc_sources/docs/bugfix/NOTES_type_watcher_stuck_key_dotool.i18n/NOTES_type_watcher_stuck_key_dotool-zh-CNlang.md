# 注意：type_watcher.sh 卡住按键问题 (dotool)

## 症状
Manjaro 重启后不久，在“sl5net Aura”之后的第一次听写
自动启动，单个角色被卡住并无限重复
（例如“n”重复数百次）直到按下触发键
再次作为手动解决方法。

2026-07-21 ~09:44（周二）观察一次，文字：“Die Ideen niemand wrd
mehr gefragt, aber es soll trotzdem genauso sein wie...nnnnn..."。

## 时间线（通过日志证明）
- 09:29:17 - `type_watcher.sh` 启动 (log/type_watcher.log)
- 09:41:56 - 收到听写“ideen niemand wrd mehr gefragt...”
（日志/aura_engine.log，线程 13/14）
- 09:42:03 - 文本处理完成（`最佳模糊分数：0%`），
大概写入“tts_output_*.txt”文件
- ~09:42:04-09:42:09 - `type_watcher.sh` 崩溃了（推断：看门狗
轮询间隔为5s，见下文）
- 09:42:09 - 看门狗日志（log/type_watcher_keep_alive.log）：
“WATCHDOG：‘type_watcher.sh’未运行。立即启动。”
- 09:42:13 - `type_watcher.sh` 重新启动 (log/type_watcher.log)
- “ideen niemand...”文件没有“键入内容...”条目
在 log/type_watcher.log 中找到过 — 该特定的类型
文本从未完成/记录。

## 根本原因状态
- 已确认：“type_watcher.sh”在完成文本之间崩溃
处理（09:42:03）并且看门狗检测到它没有运行
（09:42:09）。看门狗（`type_watcher_keep_alive.sh`）只会杀死
并在配置文件时间戳更改时重新启动（`ts1`/`ts2`，
确认在此事件中未发生变化）或在以下情况下自动重新启动
`pgrep -f "type_watcher.sh"` 没有找到任何进程——也就是说，这非常
可能是自我崩溃，而不是外部杀戮。
- 假设（未证实）：“set -euo pipelinefail”（type_watcher.sh 第 5 行）
导致脚本在某些非零退出代码上退出
管道，可能是“do_type()”的“dotool”管道（第 125 行）
中流。如果 bash 进程在流入 `dotool` 时终止，
单独的“dotoold”守护进程（保持独立运行）
可以让钥匙处于“向下”状态而没有匹配的“向上”状态
收到，导致操作系统级按键重复。
- 尚未证明：导致非零的确切命令/行
在“set -euo pipelinefail”下退出。崩溃时没有 stderr
`type_watcher.sh` 进程被捕获（看门狗将其称为
没有任何输出重定向，`type_watcher_keep_alive.sh`第79行）。
- 受影响的键在不同的版本中并不总是相同的字符
此错误的发生次数（用户报告：之前也是“t”）。

## 已经调查并排除
- 不是配置更改触发的重新启动（由用户确认：config
未更改，并且 `ts1_old != ts1_new` 检查将记录“配置已更改”）。
- 不是与“type_watcher.sh”重叠的重复自动启动
本身（崩溃前只有一个“Hello from Watcher”条目）。
- `do_type()` 的 `dotool type` 调用对于每次调用都是原子的，并且不会
本身不发送每个字符的键向下/向上 - 排除“type_watcher.sh”
应用程序逻辑是正常情况下卡住按键的直接来源
（非崩溃）操作。

## 已应用修复（回退/缓解，不是根本原因修复）
`type_watcher.sh` 中的 `cleanup()` 和 `do_cleanup()` 中
`keep-keys-up.sh` 之前仅发布了修饰键（shift、ctrl、
alt 等）通过 `dotool`/`xdotool`。这对于卡住的普通人来说没有任何作用
键（字母、数字、标点符号）。

- `type_watcher.sh`：`cleanup()` 现在发送 `dotool key <name>:up`
所有字母、数字和常见标点符号/空格键，不
只是修饰符。
- `type_watcher.sh`：`INPUT_METHOD` 现在在检测后导出，因此
其他脚本可以查看哪个后端（`dotool` / `xdotool`）处于活动状态。
- `keep-keys-up.sh`：`do_cleanup()` 获得了一个 `dotool` 分支（使用
`keyup` 动词，没有每个键的延迟，为了性能）仅在以下情况下有效
`INPUT_METHOD=dotool`，镜像现有的 `xdotool keyup` 调用
对于修饰符。

这并不能修复`type_watcher.sh`的底层崩溃；仅此而已
确保如果再次发生崩溃，卡住的按键会被释放
下一个清理过程（`--cleanup`，在每个 `do_type()` 之后调用，并且
通过“陷阱清理 EXIT INT TERM”处理程序）而不是重复
无限期地直到按下手动触发键。

## 如果再次发生这种情况，下一步
- 崩溃时捕获 `type_watcher.sh` 的 stderr。现在
`type_watcher_keep_alive.sh` 第 79 行调用它时没有重定向，所以
任何 bash 错误消息都会丢失（转到看门狗自己的
stdout/stderr，无论是由自动启动机制引导的地方）。
- 考虑调试模式，例如`bash -x 脚本/type_watcher/type_watcher.sh
2>> log/type_watcher_debug.log`，通过环境变量切换，例如
`TYPE_WATCHER_DEBUG=1`，捕获下一个确切的失败行
碰撞。
- 检查 Manjaro 启动时启动 `type_watcher_keep_alive.sh` 的内容
（自动启动 `.desktop` 文件、systemd `--user` 单元等）以及是否
它的 stdout/stderr 可以在任何地方捕获。
- 如果可重现，测试崩溃是否与
`dotoold` 仍在启动后立即初始化（请参阅 `sleep 0.1`
在 type_watcher.sh 第 8 行和 `dotoold` 启动循环中
102-110）。