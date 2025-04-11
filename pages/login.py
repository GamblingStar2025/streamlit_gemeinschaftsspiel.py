
import streamlit as st
from datetime import datetime, timedelta

st.title("🔐 Login – EuroGenius Zugangskontrolle")

# Dummy-Datenbank mit Gast-/Premiumstatus & Startdatum
benutzer_db = {
    "test@euromillion.ch": {"passwort": "1234", "rolle": "premium", "startdatum": "2024-01-01"},
    "gast@demo.com": {"passwort": "demo", "rolle": "gast", "startdatum": "2025-04-01"},
}

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
    st.session_state["user_email"] = None
    st.session_state["rolle"] = None
    st.session_state["startdatum"] = None

if not st.session_state["is_logged_in"]:
    email = st.text_input("📧 E-Mail")
    pw = st.text_input("🔑 Passwort", type="password")
    
    if st.button("🔓 Login"):
        if email in benutzer_db and benutzer_db[email]["passwort"] == pw:
            st.session_state["is_logged_in"] = True
            st.session_state["user_email"] = email
            st.session_state["rolle"] = benutzer_db[email]["rolle"]
            st.session_state["startdatum"] = datetime.strptime(benutzer_db[email]["startdatum"], "%Y-%m-%d")
            st.success("✅ Login erfolgreich!")
            st.experimental_rerun()
        else:
            st.error("❌ Login fehlgeschlagen. Prüfe E-Mail oder Passwort.")

else:
    rolle = st.session_state["rolle"]
    email = st.session_state["user_email"]
    startdatum = st.session_state["startdatum"]
    heute = datetime.now()
    ablaufdatum = startdatum + timedelta(days=7)

    st.success(f"✅ Eingeloggt als {email}")
    st.info(f"Rolle: **{rolle.upper()}**")
    st.markdown(f"🗓️ Startdatum: {startdatum.date()}")

    if rolle == "gast":
        st.markdown(f"⏳ Testzeitraum gültig bis: **{ablaufdatum.date()}**")

    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.experimental_rerun()
