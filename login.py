import streamlit as st
from auth import login_user

st.title("🔑 Login")

user_type = st.radio("Account-Typ:", ["Gast", "Premium"])
email = st.text_input("E-Mail")
password = st.text_input("Passwort (nur für Premium)", type="password")

if st.button("Login"):
    if not email:
        st.warning("E-Mail fehlt.")
    else:
        user_type_key = "premium" if user_type == "Premium" else "gast"
        res = login_user(email, password if user_type_key == "premium" else None, user_type_key)
        st.success("Erfolgreich eingeloggt oder Mail gesendet. Weiterleitung folgt...")
        st.session_state["logged_in"] = True
        st.session_state["email"] = email