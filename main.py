import streamlit as st
st.set_page_config(page_title="EuroGenius", layout="centered")

st.title("Willkommen bei EuroGenius")
st.sidebar.page_link("pages/login.py", label="🔐 Login")
st.sidebar.page_link("pages/strategie.py", label="🧠 Strategie")
