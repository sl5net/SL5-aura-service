#!/usr/bin/env python3
"""
Trino connectivity diagnostic — tools/tests/diagnose_trino.py
Run directly:  python tools/tests/diagnose_trino.py
Primes, starts, and verifies Trino connection on-the-fly.
"""
import sys
import socket
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.py.func.db.trino_client import get_connection, TRINO_HOST, TRINO_PORT  # type: ignore

SEP = "─" * 60

def check(label, fn):
    try:
        result = fn()
        print(f"  ✓  {label}: {result}")
        return True
    except Exception as e:
        print(f"  ✗  {label}: {type(e).__name__}: {e}")
        return False

def tcp_check():
    s = socket.socket()
    s.settimeout(3)
    try:
        s.connect((TRINO_HOST, TRINO_PORT))
        return "port open"
    finally:
        s.close()

print(SEP)
print(f"  Trino target:  {TRINO_HOST}:{TRINO_PORT}")
print(SEP)

# 1. Check TCP port, trigger auto-init on-demand if closed (Late-Binding)
tcp_ok = check("TCP port reachable", tcp_check)

if not tcp_ok:
    print("\n  ➜  Port is closed. Attempting on-demand Trino initialization...")
    try:
        from scripts.py.func.db.init_trino_db import init_all_sync
        init_all_sync()
        # Retry TCP check after initialization
        time.sleep(1.0)
        tcp_ok = check("TCP port reachable (after init)", tcp_check)
    except Exception as e:
        print(f"  ✗  Auto-init trigger failed: {e}")

if not tcp_ok:
    print()
    print("  ➜  Port remains closed. Trino could not be started.")
    print("     Ensure Docker service is running or use systemd socket activation.")
    sys.exit(1)

# 2. Trino HTTP / SELECT 1
def ping():
    conn = get_connection(schema='default')
    cur  = conn.cursor()
    cur.execute("SELECT 1")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

check("SELECT 1", ping)

# 3. Schema visibility
def show_schemas():
    conn = get_connection(schema='default')
    cur  = conn.cursor()
    cur.execute("SHOW SCHEMAS FROM memory")
    rows = [r[0] for r in cur.fetchall()]
    cur.close(); conn.close()
    return rows

schemas_ok = check("SHOW SCHEMAS FROM memory", show_schemas)

# 4. Tables (only if schema exists)
def show_tables():
    conn = get_connection(schema='aura')
    cur  = conn.cursor()
    cur.execute("SHOW TABLES FROM memory.aura")
    rows = [r[0] for r in cur.fetchall()]
    cur.close(); conn.close()
    return rows

if schemas_ok:
    check("SHOW TABLES FROM memory.aura", show_tables)

print(SEP)
