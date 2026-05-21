# 文档/Developer_Guide/Trino_Integration.md
历史|少  ✔
10093 docker rm trino 2>/dev/null; docker run -d --name trino -p 8083:8080 trinodb/trino
10094 docker 日志 trino -f | grep -m1“服务器已启动”
10095 源 .venv/bin/activate
10096 pip 安装三诺
10098 点显示三重奏
10099 python3 -c "\nimport trino\nconn = trino.dbapi.connect(host='localhost', port=8083, user='aura')\ncur = conn.cursor()\ncur.execute('SELECT 1')\nprint('Trino 连接:', cur.fetchone())\n"




现在：
config.json ──────► Ebene 2 (终端)
└──► Ebene 3 (Streamlit)
└──► Ebene 3.5（网页版）
↑
ALLE 柴油机配置

想法：

Ebene 2 (终端) ─┐
Ebene 3 (Streamlit) ─┼──► Trino ──► user_configs
Ebene 3.5 (Web) ─┘ ├── 终端: EN 翻译 = true
├── 网页：DE、kein翻译
└── 每个用户：eigene 覆盖




配置/
├── settings.py ← Haupt-Config
├── settings_local.py ← lokale 覆盖
├──settings_local.py_Example.txt
├──settings_local.py_Example_user_...txt
└── 过滤器/.backlock/first_run/
└── settings_local_log_filter.py ← einziger “上下文分割”

+ 多样化的 JSON-Dateien 和 verschiedenen Orten