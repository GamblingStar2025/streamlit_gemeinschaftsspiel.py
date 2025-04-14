
import streamlit as st

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 Login")

rolle = st.radio("Login als:", ["gast", "premium"], horizontal=True)

if rolle == "gast":
    st.subheader("🔓 Gastzugang")
    email = st.text_input("E-Mail (ohne Passwort)")
    if st.button("✅ Gast-Login"):
        if "@" in email and "." in email:
            st.session_state["is_logged_in"] = True
            st.session_state["user_email"] = email
            st.session_state["rolle"] = "gast"
            st.success("🎉 Eingeloggt als **Gast**.")
            if st.button("➡️ Weiter zur App"):
                st.switch_page("pages/main_app.py")
        else:
            st.error("❌ Bitte eine gültige E-Mail-Adresse eingeben.")

elif rolle == "premium":
    st.subheader("💎 Premiumzugang")
    email = st.text_input("E-Mail")
    password = st.text_input("Passwort", type="password")
    if st.button("🔐 Premium-Login"):
        if "@" in email and "." in email and len(password) >= 4:
            # Hier könnte Supabase Auth oder eine echte Nutzerprüfung folgen
            st.session_state["is_logged_in"] = True
            st.session_state["user_email"] = email
            st.session_state["rolle"] = "premium"
            st.success("💎 Eingeloggt als **Premium**.")
            if st.button("➡️ Weiter zur App"):
                st.switch_page("pages/main_app.py")
        else:
            st.error("❌ Ungültige E-Mail oder Passwort.")
