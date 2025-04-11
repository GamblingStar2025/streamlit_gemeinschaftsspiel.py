
import streamlit as st

st.markdown("## 🔐 Login")

email = st.text_input("📧 E-Mail")
pw = st.text_input("🔑 Passwort", type="password")

col1, col2 = st.columns(2)
with col1:
    st.button("Login")
with col2:
    st.button("Als Gast testen")

st.markdown("---")
st.markdown("Oder melde dich an mit:")
st.button("🔵 Google Login (Demo)")
