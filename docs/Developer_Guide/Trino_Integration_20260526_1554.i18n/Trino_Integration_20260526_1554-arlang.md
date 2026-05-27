#docs/Developer_Guide/Trino_Integration.md
```markdown
# Trino Integration Guide

This document outlines the setup for Trino (SQL query engine) and the roadmap for migrating our configuration management to a centralized Trino-backed system.

## Local Environment Setup

start docker
```bash
                                     Sudo systemctl start docker && docker ps
                                                  ls -la /var/run/docker.sock

```

check if trino runns:
```bash
                        عامل ميناء ملاحظة -a | grep ترينو
```

if it not runs (Exited) run it:
```bash
                                        عامل ميناء بدء ترينو
 سجلات عامل الإرساء trino -f | grep -m1 "بدأ الخادم"
```

check GUI:
```bash
                                                        http://localhost:8083
```

### 1. Docker Installation & Image
To ensure you have the latest image, pull it first:
```bash
                                       df -h / /home 2>/dev/null XSPACEbreakX
                         عامل ميناء سحب ترينودب/ترينو
```

### 2. Run Trino Container
Start a local instance with port mapping (mapping internal `8080` to local `8083`):
```bash
              عامل الميناء rm ترينو 2>/dev/null || حقيقي
تشغيل عامل الميناء -d - اسم ترينو -p 8083:8080 ترينودب/ترينو
```

Check logs to confirm the server is ready:
```bash
 سجلات عامل الإرساء trino -f | grep -m1 "بدأ الخادم"
```

### 3. Python Integration
Install the official Trino client:
```bash
                                               نقطة تثبيت ترينو
```

Test the connection:
```python
                                                    استيراد ترينو
        conn = trino.dbapi.connect(host=\'localhost', port=8083, user='aura')
                                                          cur = conn.cursor()
                                                     cur.execute(\'حدد 1')
         طباعة ("التحقق من اتصال Trino:"، cur.fetchone ())
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
                            الطبقة الثانية (المحطة) ─┐
الطبقة 3 (مباشرة) ─┼──► Trino ──► الجدول: user_configs
الطبقة 3.5 (الويب) ─┘ ├── المحطة الطرفية: {ترجمة: صحيح}
            ├── الويب: {اللغة: "DE"، الترجمة: خطأ}
                      └── معرف_المستخدم: {custom_overrides}
```

### Current File Structure
- `config/settings.py`: Main entry point.
- `config/settings_local.py`: Local developer overrides (ignored by git).
- `config/filters/`: Context-specific logging filters.

---
*Note: This integration is part of the Sl5 Aura ecosystem.*
```