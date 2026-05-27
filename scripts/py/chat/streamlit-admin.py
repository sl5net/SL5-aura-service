# scripts/py/chat/streamlit-admin.py
# Aura Admin Interface — Port 8084
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[3]))

import streamlit as st
from scripts.py.func.db.aura_state import (
    get_all_status,
    enable_translation,
    disable_translation,
    set_language,
)

st.set_page_config(page_title="Aura Admin", page_icon="⚙️", layout="wide")
st.title("⚙️ Aura Admin Dashboard")

st.subheader("Translation State")

statuses = get_all_status()

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
            if st.button(f"Disable", key=f"disable_{interface}"):
                disable_translation(interface)
                st.rerun()
        else:
            lang_input = st.selectbox(
                "Language",
                ['en', 'de', 'fr', 'es', 'pt-BR', 'ja', 'ar'],
                key=f"lang_{interface}"
            )
            if st.button(f"Enable", key=f"enable_{interface}"):
                enable_translation(interface, lang=lang_input)
                st.rerun()

st.divider()
st.subheader("Raw State")
st.json(statuses)
