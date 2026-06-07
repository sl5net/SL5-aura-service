# scripts/py/chat/streamlit-admin.py
# Aura Admin Interface — Port 8084
import os
import re
import sys
from pathlib import Path
from importlib import metadata
import logging

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f'{PROJECT_ROOT}/log/{__name__}.log', mode='a', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


logger = logging.getLogger(__name__)
try:
    ver = metadata.version("streamlit")
    print("streamlit version:", ver)
except metadata.PackageNotFoundError:
    print("streamlit not installed")
    from scripts.py.func.try_auto_install_package import try_auto_install_package
    try_auto_install_package('streamlit',logger=logger)

import streamlit as st

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

sys.path.insert(0, str(Path(__file__).parents[3]))
st.info(f"DEBUG SYS.PATH: {sys.path}")
st.info(f"DEBUG {Path(__file__).resolve().relative_to(PROJECT_ROOT)}")
st.info(f"DEBUG PROJECT_ROOT = {PROJECT_ROOT}")
st.info("DEBUG 'from scripts.py.func.config.dynamic_settings import settings'")

# scripts/py/chat/streamlit-admin.py:44
from scripts.py.func.config.dynamic_settings import DynamicSettings
settings = DynamicSettings()
st.info(f"DEBUG settings.DEV_MODE: {settings.DEV_MODE}")

# scripts/py/chat/streamlit-admin.py:32
msg = f"DEBUG 1 CWD: {os.getcwd()}, settings.TRINO_ENABLED:{settings.TRINO_ENABLED}"
logger.info(msg)
print(msg)
st.info(msg)




# scripts/py/chat/streamlit-admin.py:40
msg = f"DEBUG 2 CWD: {os.getcwd()}, settings.TRINO_ENABLED:{settings.TRINO_ENABLED}"
logger.info(msg)
print(msg)
st.info(msg)


st.set_page_config(page_title="Aura Admin", page_icon="⚙️", layout="wide")


if not getattr(settings, "TRINO_ENABLED", False):
    st.title("⚙️ Aura Admin Dashboard")
    st.info(f"Trino database features are currently disabled in your settings (`TRINO_ENABLED = {settings.TRINO_ENABLED}`).")
    st.markdown("""
    To use the dynamic database-driven state management and dynamic translation configurations, 
    please enable Trino in your `settings_local.py` or dynamic settings.

    Once enabled and your Aura engine is restarted, this dashboard will become active.
    """)
    st.stop()  # Stoppt hier sauber

db_ready = False
statuses = []
connection_error_details = ""
error_category = "generic"

import os
import time
import urllib.request


def wake_up_docker_and_trino_or_get_error():
    # --- WINDOWS ON-DEMAND WAKEUP ---
    from subprocess import run

    trine_is_running = False
    if os.name == 'nt':
        docker_check = run(["docker", "info"], capture_output=True, text=True)

        if docker_check.returncode != 0:
            print("🚀 Docker schläft. Starte Docker Desktop On-Demand...")
            # Docker Desktop im Hintergrund starten (Standardpfad)
            docker_path = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
            if os.path.exists(docker_path):
                # os.startfile weckt die exe ohne das Terminal zu blockieren
                os.startfile(docker_path)

                # Warten, bis die Docker-Engine antwortet (Timeout ca. 30-40 Sek.)
            for _ in range(20):
                time.sleep(2)
                if run(["docker", "info"], capture_output=True).returncode == 0:
                    print("✅ Docker Engine ist jetzt wach!")
                    break

        # 2. Now that Docker is safely running, let's wake up the Trino container
        print("Starte Trino Container...")
        run(["docker", "start", "trino"], capture_output=True)

        # 3. Warten, bis Trino auf Port 8083 wirklich Anfragen annimmt
        for _ in range(15):
            time.sleep(2)
            try:
                # Schneller Ping auf die Trino API
                urllib.request.urlopen("http://localhost:8083/v1/info", timeout=2)
                print("✅ Trino ist voll erreichbar!")
                trine_is_running = True
                break
            except Exception:
                pass

    # --- LINUX ON-DEMAND WAKEUP ---
    else:
        run(["docker", "start", "trino"], capture_output=True)
        time.sleep(2)  # Kurze Atempause für Trino

    if trine_is_running:
        return None
    else:
        return f"trino is not running. trine_is_running={trine_is_running} "



try:
    from scripts.py.func.db.aura_state import (
        get_all_status,
        enable_translation,
        disable_translation,
        ensure_fuzzy_map_in_sync,
    )
    statuses = get_all_status()
    db_ready = True
except Exception as init_e:
    from subprocess import run

    connection_error_details = str(init_e)
    err_msg_lower = connection_error_details.lower()

    # --- NEU: Late-Binding / On-Demand Installation für das 'trino' Paket ---
    if "no module named 'trino'" in err_msg_lower:
        import sys
        import importlib

        st.info("📦 Trino-Modul wird On-Demand installiert. Bitte warten...")
        try:
            # OS-unabhängige Installation ins aktuelle .venv
            run([sys.executable, "-m", "pip", "install", "trino"], check=True)
            # IMPORTANT for Windows: Clear the module cache so that Python sees the new package immediately!
            importlib.invalidate_caches()

            # Seite sofort neu laden, um im zweiten Anlauf erfolgreich zu verbinden
            st.rerun()
        except Exception as pip_e:
            st.error(f"❌ Fehler bei der On-Demand-Installation von Trino:\n\n{pip_e}")
            st.stop()
    # ------------------------------------------------------------------------

    # Detect if the error is a connection failure or a missing schema/table/column
    is_conn_error = "connection refused" in err_msg_lower or "failed to establish a new connection" in err_msg_lower or "max retries exceeded" in err_msg_lower
    is_schema_error = re.search(r"(schema|table|column) .* (does not exist|cannot be resolved)", err_msg_lower)


    if is_conn_error or is_schema_error:






        if not st.session_state.get('_db_init_attempted'):
            st.session_state['_db_init_attempted'] = True
            trino_eror = wake_up_docker_and_trino_or_get_error()
            if trino_eror:
                msg = trino_eror
                logger.info(msg)
                print(msg)
                st.info(msg)
            st.stop()

            from scripts.py.func.db.init_trino_db import init_all_sync
            try:
                init_all_sync()
                st.rerun()
                # statuses = get_all_status()

                # st.rerun()
            except Exception as init_e:
                import sys
                import traceback
                file = __file__
                st.error(f"""
                Auto-init failed 
                
                __file__= 
                
                {__file__.replace(str(PROJECT_ROOT), "")[1:]}:82
    
                __name__= {__name__}
                
                
                scripts.py.func.db.init_trino_db 
                
                import init_all as init_trino
                
                 \n\n {init_e}
                """)
                # traceback.print_exc(file=sys.stdout)
                st.info(f"{traceback.format_exc().replace(str(PROJECT_ROOT), '')}")

                st.stop()
        else:
            import datetime
            now = datetime.datetime.now().strftime("%H:%M:%S")
            st.error(f"[{now}] DB init already attempted this session — still failing. Reload the page manually to retry.")
            if getattr(settings, "DEV_MODE", False):
                logger.info('tip:  fuser -k 8084/tcp   ')
                logger.info('tip:  tail -n 30 log/scripts.py.func.db.init_trino_db.log   ')
                st.exception(connection_error_details)
                st.stop()
            else:
                logger.info('you not in DEV mode')
            st.stop()

if not db_ready:
    if error_category == "connection_refused":
        st.title("🔌 Database Connection Refused")
        st.error("The Aura Admin Dashboard cannot connect to the Trino database on port 8083. (scripts/py/chat/streamlit-admin.py)")
        st.markdown("""
        ### 🔍 Why did this happen?
        Trino is **enabled** in your settings, but the database port is closed. 
        Usually, this means either the **Docker daemon** is not running, or the **Trino container** has not started yet.

        ### 🛠️ How to fix it:

        #### Option 1: Start Docker and Trino manually
        Run these commands in your terminal to wake up the services:
        ```bash
        # 1. Start the Docker service
        sudo systemctl start docker

        # 2. Start the Trino container
        docker start trino
        ```

        #### Option 2: Configure On-Demand Activation (Recommended for Linux)
        If you don't want the heavy Docker service running constantly in the background, you can configure systemd to start Docker **automatically** only when Aura requests it (saving ~500MB of RAM):
        ```bash
        sudo systemctl stop docker.service
        sudo systemctl disable docker.service
        sudo systemctl enable docker.socket
        sudo systemctl start docker.socket
        ```
        """)

    elif error_category == "schema_missing":
        st.title("⚙️ Trino is running, but Schema is missing")
        st.warning("Successfully connected to Trino on port 8083, but the required database tables do not exist yet.")
        st.markdown("""
        ### 🔍 Why did this happen?
        Since Trino runs in-memory (`memory` catalog), all tables are cleared on every restart. 
        This error means the **background initialization thread** has either not finished yet, or it failed during startup.

        ### 🛠️ How to fix it:

        #### Option 1: Just wait a few seconds
        If you just booted your PC or restarted Aura, the background thread might still be setting up the tables. **Simply refresh this page in 10-15 seconds.**

        #### Option 2: Force manual initialization
        If the schema remains missing, you can manually trigger the database setup script in your terminal:
        ```bash
        .venv/bin/python3 scripts/py/func/db/init_trino_db.py
        ```

        #### Option 3: Restart Aura Engine
        Restarting your main `aura_engine.py` process will re-trigger the asynchronous background initialization thread.
        """)

    else:  # 'generic'
        st.title("❌ Unexpected Database Error")
        st.error("An unexpected error occurred while communicating with the Trino database.")
        st.markdown("""
        Please inspect the technical details below or check the Aura log files (`log/aura_engine.log`) for more information.
        """)

    st.divider()
    with st.expander("Technical Error Details"):
        st.code(connection_error_details, language="text")

    st.stop()  # Stoppt hier sauber und zeigt kein unvollständiges Dashboard

# --- Normal Dashboard Code (Only runs when everything is healthy) ---
st.title("⚙️ Aura Admin Dashboard")
st.subheader("Translation State")

for status in statuses:
    interface = status['interface']
    translation = status['translation']
    language = status['language'] or '-'

    col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
    with col1:
        st.write(f"**{interface}**")
    with col2:
        state_color = "🟢" if translation == 'on' else "🔴"
        st.write(f"{state_color} {translation}")
    with col3:
        st.write(f"🌐 {language}")
    with col4:
        if translation == 'on':
            if st.button("Disable", key=f"disable_{interface}"):
                disable_translation(interface)
                ensure_fuzzy_map_in_sync(interface)
                st.rerun()
        else:
            lang_input = st.selectbox(
                "Language",
                ['en', 'de', 'fr', 'es', 'pt-BR', 'ja', 'ar'],
                key=f"lang_{interface}"
            )
            if st.button("Enable", key=f"enable_{interface}"):
                enable_translation(interface, lang=lang_input)
                ensure_fuzzy_map_in_sync(interface)
                st.rerun()

st.divider()
st.subheader("Raw State")
st.json(statuses)
