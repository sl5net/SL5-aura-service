# docs/Developer_Guide/Trino_Integration.md
```markdown
# Trino Integration Guide

This document outlines the setup for Trino (SQL query engine) and the roadmap for migrating our configuration management to a centralized Trino-backed system.

## Local Environment Setup

### 1. Docker Installation & Image
To ensure you have the latest image, pull it first:
```bash
df -h / /home 2>/dev/null    
docker pull trinodb/trino
```

### 2. Run Trino Container
Start a local instance with port mapping (mapping internal `8080` to local `8083`):
```bash
docker rm trino 2>/dev/null || true
docker run -d --name trino -p 8083:8080 trinodb/trino
```

Check logs to confirm the server is ready:
```bash
docker logs trino -f | grep -m1 "SERVER STARTED"
```

### 3. Python Integration
Install the official Trino client:
```bash
pip install trino
```

Test the connection:
```python
import trino
conn = trino.dbapi.connect(host='localhost', port=8083, user='aura')
cur = conn.cursor()
cur.execute('SELECT 1')
print('Trino connection check:', cur.fetchone())
```

---

## Configuration Architecture Roadmap

### Legacy State
Currently, all layers read from a central `config.json`. This lacks flexibility for different execution contexts.
`config.json` ———► Terminal / Streamlit / Web

### Future State: Centralized Context-Aware Config
We are moving towards a Trino-backed configuration store (`user_configs`) to allow specific overrides per user and platform.

**Logic Flow:**
```text
Layer 2 (Terminal)   ─┐
Layer 3 (Streamlit)  ─┼──► Trino ──► Table: user_configs
Layer 3.5 (Web)      ─┘              ├── terminal: {translate: true}
                                     ├── web:      {lang: "DE", translate: false}
                                     └── user_id:  {custom_overrides}
```

### Current File Structure
- `config/settings.py`: Main entry point.
- `config/settings_local.py`: Local developer overrides (ignored by git).
- `config/filters/`: Context-specific logging filters.

---
*Note: This integration is part of the Sl5 Aura ecosystem.*
```
