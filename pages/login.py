
import streamlit as st
from custom_style import eurogenius_css

st.set_page_config(page_title="Login", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)

st.title("🔐 Login – EuroGenius")

email = st.text_input("📧 E-Mail")

if st.button("🔓 Login (Demo ohne Passwort)"):
    st.session_state["is_logged_in"] = True
    st.session_state["user_email"] = email

    if email.strip().lower() == "test@euromillion.ch":
        st.session_state["rolle"] = "premium"
    else:
        st.session_state["rolle"] = "gast"

    st.success(f"✅ Eingeloggt als {email} ({st.session_state['rolle']})")

if st.session_state.get("is_logged_in"):
    st.markdown(f"👤 Rolle: **{st.session_state['rolle']}**")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.experimental_rerun()
