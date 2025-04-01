
import streamlit as st
from datetime import date
import random

st.set_page_config(page_title="EuroMillions App", layout="centered")

st.title("🎯 EuroMillions App")
st.markdown("Willkommen bei deiner intelligenten Tipp-App für EuroMillions!")

modus = st.radio("Spielmodus wählen", ["👤 Einzelspieler", "👥 Gemeinschaftsspiel"])
land = st.selectbox("Land", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇫🇷 Frankreich", "🇦🇹 Österreich"])
waehrung = "CHF" if "Schweiz" in land else "€"
preis = 3.5 if "Schweiz" in land else 2.5

anzahl = st.slider("Anzahl Tipps", 1, 50 if modus == "👤 Einzelspieler" else 500)
ki = st.slider("KI-Gewichtung", 0, 200, 100)
sim = st.slider("Simulationen", 10000, 1000000, 100000, step=10000)

# Methoden-Auswahl
st.markdown("### 📊 Analyse-Strategien")
use_hot = st.checkbox("🔥 Hot/Cold", value=True)
use_cluster = st.checkbox("🧩 Cluster", value=True)
use_rad = st.checkbox("♻️ Rad-Prinzip", value=False)
use_monte = st.checkbox("🎲 Monte Carlo", value=True)

kosten = anzahl * preis
st.markdown(f"💰 **Gesamtkosten:** {kosten:.2f} {waehrung}")

if st.button("🚀 Tipps generieren"):
    st.subheader("🧮 Generierte Tipps")
    for i in range(anzahl):
        zahlen = sorted(random.sample(range(1, 51), 5))
        sterne = sorted(random.sample(range(1, 13), 2))
        z = ", ".join(map(str, zahlen))
        s = " ⭐ ".join(map(str, sterne))
        methoden = []
        if use_hot: methoden.append("Hot/Cold")
        if use_cluster: methoden.append("Cluster")
        if use_rad: methoden.append("Rad")
        if use_monte: methoden.append("Monte Carlo")
        methode_str = ", ".join(methoden)
        st.success(f"Tipp {i+1}: {z} ⭐ {s}")
        st.caption(f"🧠 Methoden: {methode_str}")

st.caption(f"© {date.today().year} EuroMillions")
