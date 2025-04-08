
import streamlit as st

st.set_page_config(page_title="EuroGenius", layout="centered")

st.image("logo_gold.png", use_container_width=True)
st.markdown("# Willkommen bei EuroGenius 🎯")

if st.button("🚀 Starte App"):
    st.switch_page("pages/main_app.py")
