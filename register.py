import streamlit as st
from auth import register_user

st.title("🔐 Registrierung")

user_type = st.radio("Account-Typ auswählen:", ["Gast", "Premium"])
email = st.text_input("E-Mail")
password = st.text_input("Passwort (nur für Premium)", type="password")

if st.button("Registrieren"):
    if not email:
        st.warning("Bitte gib eine E-Mail ein.")
    else:
        user_type_key = "premium" if user_type == "Premium" else "gast"
        res = register_user(email, password if user_type_key == "premium" else None, user_type_key)
        st.success("Überprüfe deine E-Mail zur Bestätigung.")