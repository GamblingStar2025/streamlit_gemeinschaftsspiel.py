
import streamlit as st
import random
from custom_style import eurogenius_css

st.set_page_config(page_title="Strategie-Setup", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)

st.title("🧠 Strategie-Setup mit Analyse")

tabs = st.tabs(["🔥 Heiße Zahlen", "❄️ Kalte Zahlen", "🎲 Zufallsstrategie", "🧪 KI-Strategie"])
strategie_wahl = {}

with tabs[0]:
    st.subheader("🔥 Heiße Zahlen")
    strategie_wahl["heiss"] = st.slider("Anteil heiße Zahlen (%)", 0, 100, 60)

with tabs[1]:
    st.subheader("❄️ Kalte Zahlen")
    strategie_wahl["kalt"] = st.slider("Anteil kalte Zahlen (%)", 0, 100, 40)

with tabs[2]:
    st.subheader("🎲 Zufallsstrategie")
    strategie_wahl["zufall"] = sorted(random.sample(range(1, 51), 5))
    st.json(strategie_wahl["zufall"])

with tabs[3]:
    st.subheader("🧪 KI-Strategie (Mock)")
    strategie_wahl["ki"] = st.slider("Monte Carlo Simulationen", 1000, 10000, 5000)

if st.button("💾 Strategie speichern"):
    st.success("✅ Strategie gespeichert! (Demo)")

# Navigation
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/main_app.py", label="⬅️ Zurück", icon="◀️")
with col2:
    st.page_link("pages/dashboard.py", label="➡️ Weiter", icon="▶️")
