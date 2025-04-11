
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Dashboard", layout="centered")
st.title("📊 Dashboard")

if "rolle" in st.session_state:
    rolle = st.session_state["rolle"]
    startdatum = st.session_state.get("startdatum", datetime.utcnow().isoformat())
    ablauf = datetime.fromisoformat(startdatum) + timedelta(days=7)
    st.info(f"👤 Rolle: **{rolle}**")
    if rolle == "gast":
        st.warning(f"Gastzugang gültig bis: **{ablauf.strftime('%Y-%m-%d')}**")
else:
    st.warning("Bitte zuerst einloggen.")
