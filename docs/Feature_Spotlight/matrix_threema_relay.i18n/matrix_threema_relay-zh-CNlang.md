> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../matrix_threema_relay.md).*

# 元素 ↔ Threema 测试版 GUI 中继

一个小型守护进程，在 **Element Desktop**（Matrix）之间镜像消息并
**Threema 测试版**（Threema 桌面客户端）在 Linux/X11 上通过驱动两者
像用户一样操作 Windows：键盘快捷键、剪贴板和几次鼠标点击。

没有 API，没有令牌，没有额外的 Python 库。仅使用标准的 X11 命令行工具。

## 它的功能

| 方向 | 会发生什么 |
|---|---|
| **Element → Threema** | 最后你在 Element 中写的消息将被读取，如果是新消息，则粘贴到 Threema Beta 并发送。 |
| **Threema → Element** | 通过 Threema 打开的聊天的最后一条*接收*消息通过其上下文菜单复制，如果是新的，则粘贴到 Element 并发送。 |

典型用法：在 Element 房间中口述或输入（例如使用 Aura 的情况下）
语音转文本) 并让文本出现在 Threema 聊天中，并查看
Threema 回复会出现在同一个 Element 房间中。

两个窗口都必须打开、登录，并显示你想要中继的聊天/房间。

□ 循环保护

一个天真双向的镜子 将永远回弹 每一个信息。 中继器
以短历史( `relay_history.py`) 防止这种情况 :

1. 每一份转发的文本在发送前被记住**,共180秒。
2. 如果有一段文字出现在历史上的另一边,那就是我们自己的
   回声:标记为所见,但**没有**再次转发。
3. 新的 * 和 * 未知的文本是一个真实的信息,正在转发。

文本被比作白空间崩溃, 所以换行差异从
复制/复制不会打败警卫。 因为条目死了,你可以发送
窗口过后再次出现相同的文字(例如"ok").

启动时,每一方的当前最后一条信息被读作**基线**,并且是
* 未提交。 只有启动后到达的消息会被转发.

## 要求

- Linux 使用 **X11**（`echo $XDG_SESSION_TYPE` 必须打印 `x11`）。不支持 Wayland。
- `xdotool`、`xclip`、`wmctrl` 和 `xset`（可选，用于禁用屏幕保护程序）
- Element 桌面（窗口管理器类 `element.Element`）
- Threema Beta（WM 类 `threema beta.Threema Beta`，例如 Flatpak）
  `ch.threema.threema-desktop`)
- 带有项目虚拟环境的 Python 3
- 用于一次性校准脚本的 `zsh`

□设置:一次性校正

Trema Beta绘制了无法用键盘操作的自有上下文菜单,
因此,中继点击鼠标的位置相对于
三马花窗. 测量一次:

```zsh
scripts/py/func/threema/threema-relay.zsh calibrate
```

脚本要求三个鼠标位置, 每个位置都有倒计时( 不要触摸
键盘, 不移动或调整窗口大小 :

1. ** 右键点击** 最后一个消息( 左侧有泡泡) 离开
   菜单打开了
2. 将鼠标移动到 ** “ 信件” ** 上, 不单击 。
3. 将鼠标移动到 ** message 输入字段** 。

结果被存储在 `~/.config/threema-relay.conf` 中:

关键 意思是
|---|---|
`FX` 水平点击位置作为窗口宽度的一小部分
`BOTTOM` 点击位置,窗口下边缘上方的像素
`DX`,`DY` 从点击点到"Copy Message"的偏移 QQ
`INPUT_FX`, `INPUT_BOTTOM` 信件输入字段位置 QQ
`DELAY_MENU`,`DELAY_COPY` 选取等数秒(默认为0.30/0.20) |.

用聊天中的最后一条新消息检查校准：

```zsh
scripts/py/func/threema/threema-relay.zsh test
```

它打印复制的文本而不进行转发。校准依赖于窗口
几何：如果你频繁更改 Threema 窗口大小，请重新校准。

## 使用方法

从仓库根目录开始：

```zsh
PYTHONPATH=. .venv/bin/python3 scripts/py/func/threema/matrix_threema_relay.py
```

选项：

| 选项 | 效果 |
|---|---|
| `--poll SECONDS` | 轮询间隔（默认 `2.0`） |
| `--no-threema-to-element` | 仅中继元素 → Threema |
| `--no-element-enter` | 将 Threema 消息粘贴到 Element 的输入框中，但**不要**发送它们（安全测试模式） |

停止使用 `Ctrl+C`。

推荐首次运行：使用 `--no-element-enter`，在 Threema 给自己发送一条消息
并检查它是否出现在 Element 的输入字段中。然后在不使用该选项的情况下运行。

示例日志：

```
[INFO] Initial Element baseline: 'Test'
[INFO] Initial Threema baseline: 'kaa'
[INFO] New Element message -> Threema: 'Hallo Welt'
[INFO] New Threema message -> Element: 'müsli'
[INFO] Element shows our own relayed text - not sending back.
```

# 如何运作 #

```
every poll interval
├─ Element:  focus window (wmctrl) → Up, Ctrl+A, Ctrl+C, Escape (xdotool) → read clipboard (xclip)
│            new + unknown  → paste into Threema + Return, remember text
│            new + known    → echo, ignore
└─ Threema:  focus window → right-click last incoming bubble → click "Copy Message"
                          → click input field (restores focus) → read clipboard
             new + unknown  → paste into Element (+ Return), remember text
             new + known    → echo, ignore
```

- *Up * 在 Euments 的作曲中编辑您最后的自己的消息; * Ctrl+A / Ctrl+C * 副本
  它和 * Escape* 离开编辑模式。 这就是为什么只有**你自己的**最后一个元素
  消息已转发给Treema。
- 对Treema来说,首先将**sentinel字符串**放入剪贴板。 如果还是
  之后,没有复制任何信息(例如,由于您自己的信息是
  最后一个和点击没有出气泡),尝试被忽略了.

## 文件

* * 文件 * * 目的 *
|---|---|
`matrix_threema_relay.py` 主循环,CLI,决定逻辑 (`classify_candidate`) |.
`read_last_element_message.py` 读取元素自己最后的讯息 QQ
`send_to_threema_window.py` 将文本粘入 三马贝塔
`read_last_threema_message.py` 读取了Treema最后发来的消息,装入校正QQ
`send_to_element_window.py` 将文本粘入元素
`relay_history.py` 循环保护
`threema-relay.zsh` 校正和人工测试工具(`calibrate`,`test`) |.
`test_threema_relay.py` 单位测试(不需要X11) QQ

使用以下命令运行测试：

```zsh
PYTHONPATH=. .venv/bin/python3 -m unittest scripts.py.func.threema.test_threema_relay
```

□ 限制

- ** 中继器使用鼠标和键盘焦点。 页:1 在每一次民意调查中,
  元素Windows被聚焦,鼠标会短暂地跳出(被还原). 别
  在民意测验运行时键入,或使用更长的`--poll`。
- 覆盖每个民调的剪贴板 。
- ** 当您自己的讯息是三马的最后一则时,
  恰克,一个没有被看见的回复
- ** 每个民意测验只读最后一条信息**。 如果有几条消息到达其中之一
  间隔, 只有最新的被转发 。
- ** 只有文本。 ** 图像,文件,反应和编辑都不被转发.
- ** 一对聊天。 ** 使用每个窗口中打开的聊天/房间。
- ** 元素输入字段中的草稿** 将与下一个粘贴字合并。
  留言。
- 只有11个** Wayland阻断了合成输入和窗口焦点的变化.
- 中继启动时会禁用X11屏幕保护器和DPMS(`xset s off -dpms`);
  在你重新登入或重新登入之前,他们都不要来

## 故障排除

{\fn黑体\fs22\bord1\shad0\3aHBE\4aH00\fscx67\fscy66\2cHFFFFFF\3cH808080}============================================================================= -=========================================================================================================================================================
|---|---|
请检查access-date=中的日期值 (帮助) `Threema window ... not found` 请检查access-date=中的日期值 (帮助) `xdotool search --class "Threema Beta"`和 `xprop WM_CLASS` (点击窗口).
`Nothing copied` / no Threema = Element = 重新运行 `calibrate`;运行 `test`,以收到的消息作为最后一个消息. 在慢机配置中增加 `DELAY_MENU`/ `DELAY_COPY` 。
`INPUT_FX`/`INPUT_BOTTOM` 从校正中检查 `INPUT_BOTTOM`。
QQ 三马文本出现在元素中,但没有发送QQ 接力开始于`--no-element-enter`. XQ.
`0,9353`等十进制数字在配置中由更古老的脚本版本在德文地块下编写. Python 代码接受它们; 用当前脚本再次校正写出点. |
