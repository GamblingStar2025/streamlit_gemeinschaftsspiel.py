
import streamlit as st
st.set_page_config(page_title="EuroGenius", layout="centered")
from custom_style import eurogenius_css

eurogenius_css()
st.title("🎯 EuroGenius Lotto App")
st.write("Willkommen zur Analyse- und Strategie-App für Euromillion & Swiss Lotto!")
st.page_link("pages/login.py", label="🔐 Login / Registrierung", icon="🔐")
st.page_link("pages/dashboard.py", label="📊 Dashboard", icon="📊")
st.page_link("pages/strategie.py", label="🧠 Strategie", icon="🧠")
