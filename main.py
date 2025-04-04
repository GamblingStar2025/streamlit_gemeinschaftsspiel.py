
import streamlit as st

st.title("🎯 KI-Gewichtung pro Methode")

# 🔮 Globaler KI-Gewichtungsfaktor
ki_global = st.slider("🌐 Gesamt-KI-Gewichtung (%)", 0, 200, 100)

# Einzel-Slider pro Methode
hot = st.slider("🔥 Hot-Zahlen (%)", 0, 200, 100)
cold = st.slider("❄️ Cold-Zahlen (%)", 0, 200, 100)
cluster = st.slider("📊 Cluster (%)", 0, 200, 100)
rad = st.slider("♻️ Rad-Prinzip (%)", 0, 200, 100)
monte = st.slider("🎲 Monte Carlo (%)", 0, 200, 100)

# Effektive Gewichtung pro Methode
st.subheader("📈 Effektive Gewichtungen (mit globalem Faktor multipliziert):")
for name, value in {
    "Hot-Zahlen": hot,
    "Cold-Zahlen": cold,
    "Cluster": cluster,
    "Rad-Prinzip": rad,
    "Monte Carlo": monte
}.items():
    effektiv = round(value * ki_global / 100, 2)
    st.progress(min(int(effektiv), 100), text=f"{name}: {effektiv}%")
