
import streamlit as st
from supabase import create_client\n\nurl = st.secrets['SUPABASE_URL']\nkey = st.secrets['SUPABASE_KEY']\nsupabase = create_client(url, key)

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 Login")

rolle = st.radio("Login als:", ["gast", "premium"], horizontal=True)

if rolle == "gast":
    st.subheader("🔓 Gastzugang")
    email = st.text_input("E-Mail (nur für Gastzugang)")
    if st.button("📩 Bestätigungslink senden (Demo)"):
        if "@" in email and "." in email:
            st.success(f"✅ Eine Bestätigungsmail wurde an {email} *simuliert* gesendet.")
            st.session_state["is_logged_in"] = True
            st.session_state["user_email"] = email
            st.session_state["rolle"] = "gast"
            if st.button("➡️ Weiter zur App"):
                st.switch_page("pages/main_app.py")
        else:
            st.error("❌ Bitte eine gültige E-Mail-Adresse eingeben.")

elif rolle == "premium":
    st.subheader("💎 Premiumzugang (mit Supabase Auth)")
    email = st.text_input("E-Mail")
    password = st.text_input("Passwort", type="password")
    if st.button("🔐 Einloggen"):
        if "@" in email and len(password) >= 4:
            try:
                supabase = get_client()
                result = supabase.auth.sign_in_with_password({ "email": email, "password": password })
                st.success("✅ Login erfolgreich über Supabase.")
                st.session_state["is_logged_in"] = True
                st.session_state["user_email"] = email
                st.session_state["rolle"] = "premium"
                if st.button("➡️ Weiter zur App"):
                    st.switch_page("pages/main_app.py")
            except Exception as e:
                st.error(f"❌ Supabase Login fehlgeschlagen: {e}")
        else:
            st.error("❌ Bitte gültige E-Mail und Passwort eingeben.")

st.markdown("---")
st.subheader("✨ Alternativ: Magic-Link-Login (ohne Passwort)")
magic_email = st.text_input("Magic-Link E-Mail")
if st.button("🚀 Magic-Link senden"):
    try:
        supabase = get_client()
        supabase.auth.sign_in_with_otp({ "email": magic_email })
        st.success("📩 Magic-Link wurde gesendet – bitte E-Mail prüfen.")
    except Exception as e:
        st.error(f"❌ Fehler beim Senden des Magic-Links: {e}")
