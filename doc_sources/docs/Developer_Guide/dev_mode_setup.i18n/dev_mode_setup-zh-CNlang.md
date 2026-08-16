# DEV_MODE 设置指南

＃＃ 问题

由于我们与 Weyland 兼容，因此我们使用“threading.Lock”进行日志记录。

现在（26 年 3 月 21 日星期六）记录规则已更改。在 Manjaro，这没有问题。

当“DEV_MODE = 1”处于活动状态时，Aura 每秒生成数百个日志条目
来自多个线程。这可能会导致“SafeStreamToLogger”死锁，使得
第一次听写触发后，光环会挂起。

## 修复：使用 LOG_ONLY 过滤器

使用“DEV_MODE = 1”进行开发时，您**必须**还配置日志过滤器：
`config/filters/settings_local_log_filter.py`

### DEV_MODE 的最小工作过滤器：
__代码_块_0__

## settings_local.py 的一行代码
添加此评论作为 DEV_MODE 设置旁边的提醒：
__代码_块_1__

## 根本原因
`SafeStreamToLogger` 使用 `threading.Lock` 来保护 stdout 写入。
在高日志负载 (DEV_MODE) 下，锁争用会导致系统死锁
积极的线程调度（例如具有较新内核/glibc 的 CachyOS）。