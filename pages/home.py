
import streamlit as st
from custom_style import eurogenius_css

st.set_page_config(page_title="EuroGenius", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)

st.image("https://upload.wikimedia.org/wikipedia/commons/5/53/Lottery_icon.png", width=100)
st.markdown("## 🎯 Willkommen bei EuroGenius")
st.markdown("**Dein KI-gestützter Lotto-Assistent für EuroMillions**")

if st.button("🎲 Jetzt starten"):
    st.switch_page("pages/login.py")
