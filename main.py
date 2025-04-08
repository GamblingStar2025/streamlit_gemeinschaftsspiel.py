
import streamlit as st

st.set_page_config(page_title="EuroGenius – Start", layout="centered")

st.image("https://upload.wikimedia.org/wikipedia/commons/5/53/Lottery_icon.png", width=100)
st.title("🎯 Willkommen bei EuroGenius")
st.markdown("Die intelligente App zur Analyse & Vorhersage von EuroMillions mit KI und Strategie.")
st.page_link("pages/analyse.py", label="➡️ Starte mit der CSV-Analyse")
