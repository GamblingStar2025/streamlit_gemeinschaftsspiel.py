
import streamlit as st

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 Login")

email = st.text_input("E-Mail")
rolle = st.radio("Rolle wählen", ["gast", "premium"], horizontal=True)

if st.button("✅ Einloggen"):
    if email:
        st.session_state["is_logged_in"] = True
        st.session_state["user_email"] = email
        st.session_state["rolle"] = rolle
        st.success(f"Erfolgreich eingeloggt als {rolle}!")

        if st.button("➡️ Weiter zur Hauptseite"):
            st.switch_page("pages/main_app.py")
    else:
        st.error("Bitte E-Mail eingeben.")
