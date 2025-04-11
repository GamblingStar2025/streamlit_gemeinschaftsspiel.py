
import streamlit as st

st.title("🔐 Login – EuroGenius Premium")

# Dummy-Datenbank mit E-Mail, Passwort, Premium-Status
benutzer_db = {
    "test@euromillion.ch": {"passwort": "1234", "premium": True},
    "gast@demo.com": {"passwort": "demo", "premium": False},
}

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
    st.session_state["user_email"] = None
    st.session_state["is_premium"] = False

if not st.session_state["is_logged_in"]:
    email = st.text_input("📧 E-Mail")
    pw = st.text_input("🔑 Passwort", type="password")
    
    if st.button("🔓 Login"):
        if email in benutzer_db and benutzer_db[email]["passwort"] == pw:
            st.session_state["is_logged_in"] = True
            st.session_state["user_email"] = email
            st.session_state["is_premium"] = benutzer_db[email]["premium"]
            st.success("✅ Login erfolgreich!")
            st.experimental_rerun()
        else:
            st.error("❌ Login fehlgeschlagen. Prüfe E-Mail oder Passwort.")

else:
    st.success(f"✅ Eingeloggt als {st.session_state['user_email']}")
    status = "Premium ✅" if st.session_state["is_premium"] else "Gast 🚫"
    st.info(f"Zugang: **{status}**")
    if st.button("🚪 Logout"):
        st.session_state["is_logged_in"] = False
        st.session_state["user_email"] = None
        st.session_state["is_premium"] = False
        st.experimental_rerun()
