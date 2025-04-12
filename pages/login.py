import streamlit as st
from supabase_connector import add_user, get_user

st.set_page_config(page_title="Login", layout="centered")

st.title("🔐 Login")
email = st.text_input("E-Mail")
if st.button("Einloggen"):
    user = get_user(email)
    if user:
        st.session_state["email"] = email
        st.success("Eingeloggt!")
    else:
        add_user(email)
        st.session_state["email"] = email
        st.success("Neuer Benutzer erstellt und eingeloggt.")
