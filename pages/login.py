
import streamlit as st
st.set_page_config(page_title="Login", layout="centered")
from supabase_connector import add_user, get_user
from datetime import datetime, timedelta

st.title("🔐 Login / Registrierung")

email = st.text_input("📧 E-Mail eingeben")
if st.button("Als Gast starten"):
    response = get_user(email)
    if response.status_code == 200 and response.json():
        user = response.json()[0]
        st.session_state["rolle"] = user["rolle"]
        st.session_state["email"] = email
        st.session_state["startdatum"] = user.get("startdatum")
        st.success(f"Willkommen zurück, {user['rolle']}!")
    else:
        add_user(email=email, rolle="gast", premium=False)
        st.session_state["rolle"] = "gast"
        st.session_state["email"] = email
        st.session_state["startdatum"] = datetime.utcnow().isoformat()
        st.success("Gastzugang erstellt – 7 Tage gültig.")
