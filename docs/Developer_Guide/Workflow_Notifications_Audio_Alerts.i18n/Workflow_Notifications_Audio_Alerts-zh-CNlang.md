# 工作流程通知（音频警报）

为了提高工作效率，您可以配置本地 Git 别名，该别名会在 GitHub Actions 工作流程完成后推送您的代码并自动提醒您（通过语音或声音）。这可以防止“GitHub 观看疲劳”并让您专注于其他任务。

### 先决条件

您需要在系统上安装 **GitHub CLI** 和文本转语音引擎或声音播放器。

**对于 Manjaro / Arch Linux：**
__代码_块_0__

＃＃＃ 设置

在终端中运行以下命令来创建名为“pushsound”的全局 Git 别名：

__代码_块_1__

＃＃＃ 用法

只需运行以下命令即可代替“git Push”：
__代码_块_2__
您的终端将等待工作流程完成，然后宣布：*“所有 github 工作流程已完成”*。

---

### 定制和替代方案

根据您的偏好，您可能想要使用不同的别名或通知方法。

#### 1. 推荐的别名
如果 `pushsound` 太长而无法输入，请考虑以下替代方案：
* `git pw` (Push & Watch) — **推荐速度。**
*`gitsync`（意味着推动并等待“绿灯”）
* `git Palert`（推送警报）

#### 2. 通知样式
您可以将“espeak-ng”部分替换为其他类型的警报：

* **桌面通知：**
`... && 通知发送“GitHub 操作”“工作流程完成！”`
* **系统声音（铃声）：**
`... && papplay /usr/share/sounds/freedesktop/stereo/complete.oga`
* **组合（声音+语音）：**
`... && papplay /usr/share/sounds/freedesktop/stereo/message.oga && espeak-ng“完成”`

#### 3. 高级：团队安全版本
如果多个开发人员同时推送到同一个存储库，默认命令可能会跟踪错误的运行。使用此“分支安全”版本仅监视您自己的当前分支：

##### 仅检查第一个工作流：

__代码_块_3__

##### 检查所有 GitHub 注册的工作流程

git config --global alias.pushsound '!f() { git push && echo "正在等待 GitHub 注册工作流程..." && sleep 5 && SHA=$(git rev-parse HEAD) && SUCCESS=0 && for id in $(gh run list --commit $SHA --json databaseId -q ".[].databaseId"); do echo "正在观看工作流程 $id..." && gh run watch $id --exit-status ||成功=1；完毕; [ $SUCCESS -eq 0 ] && espeak-ng "所有工作流程成功" || espeak-ng“至少一个工作流程失败”； }; f'


### 故障排除
* **“未找到运行”：** 我们包含“睡眠 3”，因为 GitHub 需要一些时间来注册推送并启动工作流程。如果您的连接速度非常慢，您可能需要将其增加到“睡眠 5”。
* **终端蜂鸣声：** 如果 `espeak-ng` 不起作用，请确保您的音频未静音并且软件包已正确安装。