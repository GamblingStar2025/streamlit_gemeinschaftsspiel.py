
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Login", layout="centered")

st.markdown("## 🔐 Login")

# Dummy-Datenbank mit Ablaufdatum
benutzer_db = {
    "test@euromillion.ch": {"passwort": "1234", "rolle": "premium", "startdatum": "2024-01-01"},
    "gast@demo.com": {"passwort": "demo", "rolle": "gast", "startdatum": "2025-04-01"},
}

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

if not st.session_state["is_logged_in"]:
    email = st.text_input("📧 E-Mail")
    pw = st.text_input("🔑 Passwort", type="password")

    if st.button("🔓 Login"):
        if email in benutzer_db and benutzer_db[email]["passwort"] == pw:
            st.session_state["is_logged_in"] = True
            st.session_state["user_email"] = email
            st.session_state["rolle"] = benutzer_db[email]["rolle"]
            st.session_state["startdatum"] = datetime.strptime(benutzer_db[email]["startdatum"], "%Y-%m-%d")
            st.experimental_rerun()
        else:
            st.error("❌ Falsche Zugangsdaten.")
else:
    rolle = st.session_state["rolle"]
    start = st.session_state["startdatum"]
    ablauf = start + timedelta(days=7)

    st.success(f"Eingeloggt als {st.session_state['user_email']}")
    st.info(f"Zugang: {rolle.upper()}")
    st.markdown(f"🗓️ Startdatum: {start.date()}")

    if rolle == "gast":
        st.markdown(f"⏳ Gültig bis: **{ablauf.date()}**")
        if datetime.now() > ablauf:
            st.warning("⚠️ Testzeitraum abgelaufen – bitte auf Premium upgraden.")
            st.switch_page("pages/upgrade.py")

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.experimental_rerun()
