# Wayland 上的 dotool — 设置和故障排除

Aura 需要“dotool”才能在 Wayland 上的其他应用程序中输入文本。
与“xdotool”不同，它通过“uinput”直接与Linux内核通信
并且适用于 **X11 和 Wayland**。

在 X11 上，默认使用“xdotool”。 `dotool` 在 X11 上是可选的，但是
建议使用以获得更好的布局稳定性（尤其是元音变音）。

---

## 1.安装dotool

**Arch / Manjaro / CachyOS (AUR):**
__代码_块_0__

**Ubuntu / Debian（如果在存储库中可用）：**
__代码_块_1__

**如果不在存储库中 - 从源代码构建：**
__代码_块_2__

---

## 2.允许dotool在没有root的情况下运行（必需）

`dotool` 需要访问 `/dev/uinput`。如果没有这个，它就会默默地失败。

__代码_块_3__

**群组更改后需要重新登录**才能生效。

---

## 3.验证安装

__代码_块_4__

如果“groups”不显示“input”，请注销并重新登录（或重新启动）。

---

## 4. Aura 如何使用 dotool

Aura 的 `type_watcher.sh` 自动：

- 通过 `$WAYLAND_DISPLAY` 检测 Wayland 并选择 `dotool`
- 如果存在且未运行，则在后台启动“dotoold”守护进程
- 如果未安装“dotool”，则回退到“xdotool”（仅限 X11）
- 设置活动 Vosk 模型的键盘布局（例如 `de` → `XKB_DEFAULT_LAYOUT=de`）

不需要手动守护进程管理——Aura 在启动时处理这个问题。

---

## 5. 故障排除

**Aura 转录但没有文字出现：**
__代码_块_5__

**缺少或乱码的字符（尤其是变音符号）：**

增加`config/settings_local.py`中的输入延迟：
__代码_块_6__

**dotool 在终端中有效，但在 Aura 中无效：**

检查“输入”组在桌面会话（而不仅仅是新终端）中是否处于活动状态。
`gpasswd` 之后需要完全重新登录。

**在 X11 上强制使用 dotool**（可选，以获得更好的布局稳定性）：
__代码_块_7__

---

## 6. dotool 无法安装时的回退

如果“dotool”在您的系统上不可用，Aura 将回退到 X11 上的“xdotool”。
在没有 `dotool` 的 Wayland 上，**不支持** - 这是一个 Wayland
安全限制，而不是 Aura 限制。

可能适用于特定合成器的替代工具：

|工具|适用于 |
|---|---|
| `xdotool` |仅限 X11 |
| `dotool` | X11 + Wayland（推荐） |
| `ydotool` | X11 + Wayland（替代）|

要使用“ydotool”作为手动解决方法：
__代码_块_8__
注意：Aura 本身不集成 `ydotool` — 需要手动配置。