
import streamlit as st
import random
from custom_style import eurogenius_css

st.set_page_config(page_title="Strategie-Zentrale", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)

st.title("🧠 Strategie-Zentrale")

tabs = st.tabs([
    "🔥 Heiße Zahlen", 
    "❄️ Kalte Zahlen", 
    "🎲 Zufall", 
    "🧪 KI-basiert",
    "🧮 Zahlendichte",
    "📉 Anti-Hot",
    "🔁 Zyklen",
    "⚙️ Benutzerdefiniert",
    "📅 Wochentagsstrategie"
])

strategien = {}

with tabs[0]:
    st.subheader("🔥 Heiße Zahlen")
    strategien["heiss"] = st.slider("Anteil heiße Zahlen (%)", 0, 100, 60)

with tabs[1]:
    st.subheader("❄️ Kalte Zahlen")
    strategien["kalt"] = st.slider("Anteil kalte Zahlen (%)", 0, 100, 40)

with tabs[2]:
    st.subheader("🎲 Zufallsstrategie")
    strategien["zufall"] = sorted(random.sample(range(1, 51), 5))
    st.json(strategien["zufall"])

with tabs[3]:
    st.subheader("🧪 KI-Strategie (Mock)")
    strategien["ki"] = st.slider("Monte Carlo Simulationen", 1000, 10000, 5000)

with tabs[4]:
    st.subheader("🧮 Zahlendichte-Strategie")
    strategien["dichte"] = st.slider("Häufigkeitsgewichtung (%)", 0, 100, 70)

with tabs[5]:
    st.subheader("📉 Anti-Hot-Strategie")
    strategien["anti_hot"] = st.slider("Meide heiße Zahlen zu (%)", 0, 100, 50)

with tabs[6]:
    st.subheader("🔁 Zyklen-Strategie")
    strategien["zyklen"] = st.slider("Zyklenwechsel nach Ziehungen", 1, 20, 5)

with tabs[7]:
    st.subheader("⚙️ Benutzerdefinierte Strategie")
    strategien["custom_hot"] = st.slider("Hot-Anteil", 0, 100, 50)
    strategien["custom_cold"] = st.slider("Cold-Anteil", 0, 100, 50)

with tabs[8]:
    st.subheader("📅 Wochentag-Strategie")
    strategien["wochentag"] = st.selectbox("Ziehungstag", ["Dienstag", "Freitag"])

if st.button("💾 Strategie speichern"):
    st.success("✅ Strategie gespeichert! (Demo)")

# Navigation
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/main_app.py", label="⬅️ Zurück", icon="◀️")
with col2:
    st.page_link("pages/dashboard.py", label="➡️ Weiter", icon="▶️")
