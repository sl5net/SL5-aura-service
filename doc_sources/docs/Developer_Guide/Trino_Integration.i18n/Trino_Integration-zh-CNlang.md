# Trino 集成 — 开发人员指南

＃＃ 建筑学
光环接口：
语音 → INTERFACE=语音（.py 中的默认后备）
终端 → INTERFACE=终端（在 s() zshrc 中显式）
web→INTERFACE=web（在start_service中显式）
↓
aura_state.py ← 供开发人员使用的高级 API
↓
trino_client.py ← 低级数据库操作
↓
Trino 内存目录
memory.aura.features ← 每个界面的翻译开/关
memory.aura.translation_state ← 每个界面的目标语言

## 本地设置

### 1. Docker

__代码_块_0__

### 2.Python客户端

__代码_块_1__

### 3. DB 初始化（Aura 启动时自动调用）

__代码_块_2__

## 开发者 API — aura_state.py

__代码_块_3__

## 管理界面

http://本地主机:8084

开始：
__代码_块_4__

## Trino UI（查询监视器）

http://localhost:8083/ui/

脚本/py/func/db/
├── 初始化.py
├── trino_client.py ← 低级：获取/设置 feature_state、target_lang
├── init_trino_db.py ←启动：Docker启动+模式+表
└── aura_state.py ← 开发者高级API
脚本/py/聊天/
└──streamlit-admin.py ← 端口 8084 上的管理 UI


## 路线图

- [x] Trino 在 Docker 中运行
- [x] Python 客户端已连接
- [x] DB 在 Aura 启动时初始化
- [x] 接口感知翻译状态
- [x] Web (Streamlit) 与语音/终端分离
- [x] 端口 8084 上的管理 UI
- [ ] 终端和语音完全独立
- [ ] 用户特定覆盖（多用户）
- [ ] 持久存储（替换内存目录）