# 混合下载器实施报告 24.3.'26 13:04 星期二

## 1. 项目状态总结
新的“download_release_hybrid.py”脚本已成功实施和集成。它复制了原始“download_all_packages.py”的核心逻辑，同时添加了 BitTorrent 混合层。

### 核心功能已验证：
* **CLI 参数解析：** 成功处理 `--exclude`、`--tag` 和 `--list`。
* **CI 环境检测：** 正确识别 GitHub Actions 并自动排除大型模型。
* **资产发现：** 成功地将发布资产分组到逻辑包（部件、校验和、Torrent）中。
* **强大的回退：** 脚本检测到 `libtorrent` 的缺失，并优雅地默认为 HTTP 回退模式。

---

## 2. 测试执行和结果
**执行的命令：**
`python 工具/download_release_hybrid.py --list`

### 观察到的输出：
* **依赖项检查：** `--> 信息：未找到“libtorrent”。混合种子已禁用。使用 HTTP 回退。`（当前系统上预期）。
* **API 连接：** 成功获取 `sl5net/SL5-aura-service @ v0.2.0` 的版本信息。
* **发现结果：** 识别出 5 个软件包：
1. `LanguageTool-6.6.zip`（3部分）
2.`lid.176.zip`（2部分）
3. `vosk-model-de-0.21.zip`（20 部分）
4. `vosk-model-en-us-0.22.zip`（19 部分）
5. `vosk-model-small-en-us-0.15.zip`（1 部分）

---

## 3. 错误报告：依赖问题
### 问题：`libtorrent` 安装失败
在当前的 **Manjaro/Arch Linux** 环境中，无法通过标准包管理器安装 BitTorrent 引擎 (`libtorrent`)。

* **尝试的命令：**
* `sudo pacman -S python-libtorrent` -> `目标未找到`
* `pamac build python-libtorrent-rasterbar` -> `目标未找到`
* `pamac build python-libtorrent` -> `目标未找到`
* **根本原因：** 基于 Arch 的系统中“libtorrent”的 Python 绑定在官方存储库中通常维护得很差，或者需要当前缺失或配置错误的特定 AUR 帮助器/构建工具（“base-devel”）。
* **影响：** BitTorrent 功能（P2P 和 Web-Seed）当前处于非活动状态。该脚本通过 **HTTP 回退** 保持完整功能。

---

## 4. 待办事项列表（后续步骤）

### 第一阶段：环境迁移
- [ ] **操作系统切换：** 将测试转移到不同的操作系统（例如 Ubuntu、Debian 或 Windows），其中“python3-libtorrent”或“pip install libtorrent”更容易使用。
- [ ] **依赖关系重新验证：** 确保“Motor”（`libtorrent`）在新操作系统上正确加载。

### 第 2 阶段：功能验证
- [ ] **完整下载测试：** 运行不带 `--list` 标志的脚本来验证部分下载、合并和 SHA256 验证。
- [ ] **排除测试：** 使用 `--exclude de` 运行以确认纯英语设置按预期工作。
- [ ] **Torrent 种子测试：** 使用 GitHub Web-Seed 创建“.torrent”文件，并验证混合下载器是否优先考虑 P2P/Web-Seed 而非标准 HTTP 部分。

### 第三阶段：清理
- [ ] **最终修剪检查：** 确认完整运行后最终本地目录结构中不存在“.i18n”或翻译文件。