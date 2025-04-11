
import streamlit as st
from supabase_connector import get_user, add_user

st.set_page_config(page_title="Login", layout="centered")

st.title("🔐 Login – EuroGenius")

email = st.text_input("📧 E-Mail")
if st.button("🔓 Login (Demo ohne Passwort)"):
    user = get_user(email)
    if user.data:
        st.session_state["is_logged_in"] = True
        st.session_state["user_email"] = email
        st.session_state["rolle"] = user.data.get("rolle", "gast")
        st.success(f"✅ Eingeloggt als {email}")
    else:
        # Erstelle neuen Gast
        add_user(email=email)
        st.session_state["is_logged_in"] = True
        st.session_state["user_email"] = email
        st.session_state["rolle"] = "gast"
        st.success("✅ Neuer Gastzugang erstellt!")

if st.session_state.get("is_logged_in"):
    st.markdown(f"👤 Rolle: **{st.session_state['rolle']}**")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.experimental_rerun()
