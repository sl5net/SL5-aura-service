# 文档/Developer_Guide/Trino_Integration.md
__代码_块_0__
docker 拉 trinodb/trino
__代码_块_1__
docker rm trino 2>/dev/null ||真的
docker run -d --name trino -p 8083:8080 trinodb/trino
__代码_块_2__
docker 日志 trino -f | grep -m1“服务器已启动”
__代码_块_3__
pip 安装 Trino
__代码_块_4__
进口三诺
conn = trino.dbapi.connect（主机='localhost'，端口=8083，用户='aura'）
cur = conn.cursor()
cur.execute('选择 1')
print('Trino 连接检查：', cur.fetchone())
__代码_块_5__
第 2 层（终端）─┐
第 3 层 (Streamlit) ─┼──► Trino ──► 表：user_configs
3.5层（Web）─┘├──终端：{translate: true}
├── web: {lang: "DE", 翻译: false}
└── user_id: {custom_overrides}
__代码_块_6__