# scripts/py/chat/streamlit-admin.py
# Aura Admin Interface — Port 8084
import re
import sys
from pathlib import Path
from importlib import metadata
import logging
logger = logging.getLogger(__name__)
try:
    ver = metadata.version("streamlit")
    print("streamlit version:", ver)
except metadata.PackageNotFoundError:
    print("streamlit nicht installiert")
    from scripts.py.func.try_auto_install_package import try_auto_install_package
    try_auto_install_package('streamlit',logger=logger)

import streamlit as st

sys.path.insert(0, str(Path(__file__).parents[3]))

st.set_page_config(page_title="Aura Admin", page_icon="⚙️", layout="wide")

from scripts.py.func.config.dynamic_settings import settings

if not getattr(settings, "TRINO_ENABLED", False):
    st.title("⚙️ Aura Admin Dashboard")
    st.info("Trino database features are currently disabled in your settings (`TRINO_ENABLED = False`).")
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

try:
    from scripts.py.func.db.aura_state import (
        get_all_status,
        enable_translation,
        disable_translation,
        ensure_fuzzy_map_in_sync,
    )

    statuses = get_all_status()
    db_ready = True
except Exception as e:
    connection_error_details = str(e)
    err_msg_lower = connection_error_details.lower()

    if "connection refused" in err_msg_lower or "failed to establish a new connection" in err_msg_lower or "max retries exceeded" in err_msg_lower:
        error_category = "connection_refused"

    # elif "schema 'aura' does not exist" in err_msg_lower:
    elif re.search(r"(schema|table) .* does not exist", err_msg_lower):

        from scripts.py.func.db.init_trino_db import init_all as init_trino
        try:
            init_trino()
            st.rerun()
        except Exception as e:
            st.error(f"Auto-init failed: {e}")
            st.stop()


if not db_ready:
    if error_category == "connection_refused":
        st.title("🔌 Database Connection Refused")
        st.error("The Aura Admin Dashboard cannot connect to the Trino database on port 8083.")
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
