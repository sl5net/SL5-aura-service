# docs/Developer_Guide/Trino_Integration.md
```markdown
# Trino Integration Guide

This document outlines the setup for Trino (SQL query engine) and the roadmap for migrating our configuration management to a centralized Trino-backed system.

## Local Environment Setup

### 1. Docker Installation & Image
To ensure you have the latest image, pull it first:
```bash
ventana acoplable tirar trinodb/trino
```

### 2. Run Trino Container
Start a local instance with port mapping (mapping internal `8080` to local `8083`):
```bash
ventana acoplable rm trino 2>/dev/null || verdadero
ventana acoplable ejecutar -d --name trino -p 8083:8080 trinodb/trino
```

Check logs to confirm the server is ready:
```bash
ventana acoplable registra trino -f | grep -m1 "SERVIDOR INICIADO"
```

### 3. Python Integration
Install the official Trino client:
```bash
instalación de pip trino
```

Test the connection:
```python
importar trino
conexión = trino.dbapi.connect(host='localhost', puerto=8083, usuario='aura')
cur = conexión.cursor()
cur.execute('SELECCIONAR 1')
print('Verificación de conexión de Trino:', cur.fetchone())
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
Capa 2 (Terminal) ─┐
Capa 3 (Streamlit) ─┼── ► Trino ── ► Tabla: user_configs
Capa 3.5 (Web) ─┘ ├── terminal: {traducir: verdadero}
├── web: {idioma: "DE", traducir: falso}
└── user_id: {custom_overrides}
```

### Current File Structure
- `config/settings.py`: Main entry point.
- `config/settings_local.py`: Local developer overrides (ignored by git).
- `config/filters/`: Context-specific logging filters.

---
*Note: This integration is part of the Sl5 Aura ecosystem.*
```