
import streamlit as st

st.set_page_config(page_title="EuroGenius", layout="centered")

st.markdown("## 🎯 Willkommen bei EuroGenius")
st.markdown("Die smarte App für deine Lotto-Strategie – mit KI, Statistik & Superjackpot-Features.")

st.image("https://upload.wikimedia.org/wikipedia/commons/5/53/Lottery_icon.png", width=100)

if st.button("🎲 Jetzt starten"):
    st.switch_page("pages/login.py")
