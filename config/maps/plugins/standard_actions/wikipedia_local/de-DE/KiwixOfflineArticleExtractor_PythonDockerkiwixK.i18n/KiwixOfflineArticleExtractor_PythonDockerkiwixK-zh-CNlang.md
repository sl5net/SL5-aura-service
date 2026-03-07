## Kiwix 离线文章提取器 (Python/Docker/kiwix-serve)

本文档提供了设置和使用 Python 脚本的分步指南，该脚本使用在 Docker 容器内运行的“kiwix-serve” Web 服务器从离线 ZIM 文件中提取维基百科文章的完整、干净的文本。

### 先决条件

您的 Manjaro 系统上必须安装以下软件：

1. **Docker：** 运行官方 `kiwix-tools` 服务器而不会出现编译问题。
2. **Python 3：** 使用虚拟环境（`venv`）。
3. **ZIM 文件：** 离线维基百科数据库（例如“wikipedia_de_all_mini_2025-09.zim”）。

### 1.系统设置（Docker）

确保 Docker 服务已安装并正在运行。

__代码_块_0__

### 2.Python环境设置

设置 Python 虚拟环境并安装必要的库。

__代码_块_1__

### 3. 运行 Kiwix 服务器（核心依赖项）

该脚本依赖于在端口“8080”上运行的“kiwix-serve”。此命令使用官方稳定的 Docker 映像，并将当前目录（包含 ZIM 文件）绑定到容器。

**重要提示：** 在运行此命令之前，请将您的 ZIM 文件（例如“wikipedia_de_all_mini_2025-09.zim”）放入“kiwix_cli”目录中。

__代码_块_2__
服务器现在正在“http://localhost:8080”上运行。

### 4.文章提取脚本

创建一个名为“article_extractor.py”的文件，并将以下最终工作代码粘贴到其中。

__代码_块_3__

### 5. 应用和清理

1. **运行脚本：**
__代码_块_4__

2. **停止 Docker 服务器（完成后）：**
您必须停止 Docker 容器，否则它会继续使用端口 8080。
__代码_块_5__
X空格符X
X空格符X