# docs/Developer_Guide/Trino_Integration.md
```markdown
# Trino Integration Guide

This document outlines the setup for Trino (SQL query engine) and the roadmap for migrating our configuration management to a centralized Trino-backed system.

## Local Environment Setup

### 1. Docker Installation & Image
To ensure you have the latest image, pull it first:
```bash
df -h //home 2>/dev/null   
docker pull trinodb/trino
```

### 2. Run Trino Container
Start a local instance with port mapping (mapping internal `8080` to local `8083`):
```bash
docker rm trino 2>/dev/null || verdadeiro
docker run -d --name trino -p 8083:8080 trinodb/trino
```

Check logs to confirm the server is ready:
```bash
docker registra trino -f | grep -m1 "SERVIDOR INICIADO"
__CODE_BLOCO_3__
pip instalar trino
```

### 3. Python Integration
Install the official Trino client:
```bash
importar trino
conn = trino.dbapi.connect(host='localhost', porta=8083, usuário='aura')
cur = conn.cursor()
cur.execute('SELECIONE 1')
print('Verificação de conexão Trino:', cur.fetchone())
__CODE_BLOCO_5__
Camada 2 (Terminal) ─┐
Camada 3 (Streamlit) ─┼──► Trino ──► Tabela: user_configs
Camada 3.5 (Web) ─┘ ├── terminal: {traduzir: verdadeiro}
├── web: {lang: "DE", tradução: falso}
└── ID_do_usuário: {custom_overrides}
```

Test the connection:
```python