
import streamlit as st
from st_supabase_connection import SupabaseConnection
from custom_style import eurogenius_css

st.set_page_config(page_title="Login / Registrierung", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)
st.title("🔐 EuroGenius – Login & Registrierung")

conn = st.connection("supabase", type=SupabaseConnection)
supabase = conn.client

mode = st.radio("🔄 Modus wählen", ["🔓 Login", "📝 Registrieren"])

email = st.text_input("📧 E-Mail")
pw = st.text_input("🔑 Passwort", type="password")

if mode == "🔓 Login":
    if st.button("➡️ Login"):
        try:
            auth_response = supabase.auth.sign_in_with_password({"email": email, "password": pw})
            user = auth_response.user
            if user:
                st.success(f"✅ Eingeloggt als {user.email}")
                st.session_state["is_logged_in"] = True
                st.session_state["user_email"] = user.email
                st.rerun()
        except Exception as e:
            st.error("❌ Login fehlgeschlagen: " + str(e))

elif mode == "📝 Registrieren":
    if st.button("🚀 Registrierung abschicken"):
        try:
            response = supabase.auth.sign_up({"email": email, "password": pw})
            if response.user:
                st.success("✅ Registrierung erfolgreich! Bitte E-Mail bestätigen.")
            else:
                st.warning("⚠️ Anmeldung hat nicht funktioniert.")
        except Exception as e:
            st.error("❌ Registrierung fehlgeschlagen: " + str(e))

if st.session_state.get("is_logged_in"):
    st.markdown(f"👤 Eingeloggt als: `{st.session_state['user_email']}`")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()
