
import streamlit as st
from datetime import date

st.set_page_config(page_title="EuroMillions Generator", layout="centered")

st.title("🎯 EuroMillions App")
st.markdown("Willkommen bei deiner intelligenten Tipp-App für EuroMillions!")

# Schritt 1: Spielmodus
modus = st.radio("Spielmodus", ["👤 Einzelspieler", "👥 Gemeinschaftsspiel"])

# Schritt 2: Länderauswahl
land = st.selectbox("Land", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇫🇷 Frankreich", "🇦🇹 Österreich"])
waehrung = "CHF" if "Schweiz" in land else "€"
tipp_preis = 3.5 if "Schweiz" in land else 2.5

# Schritt 3: Einstellungen
ki_gewichtung = st.slider("KI-Gewichtung (%)", 0, 200, 100, step=10)
sim_stufen = st.slider("Simulationen", 1000, 1000000, 100000, step=10000)

# Methoden aktivieren
st.markdown("### 📊 Analyse-Strategien")
hot = st.checkbox("Hot/Cold aktivieren", value=True)
cluster = st.checkbox("Cluster-Analyse", value=True)
rad = st.checkbox("Rad-Prinzip (Zyklen)", value=False)
monte = st.checkbox("Monte Carlo Simulation", value=True)

# Dummy Tipps anzeigen
if st.button("🚀 Tipps generieren"):
    st.success("Beispiel-Tipp: 7, 12, 25, 33, 45 ⭐ 3 & 11")
    st.info(f"Modus: {modus}, Land: {land}, KI: {ki_gewichtung}%, Simulationen: {sim_stufen}")
    aktive_methoden = []
    if hot: aktive_methoden.append("Hot/Cold")
    if cluster: aktive_methoden.append("Cluster")
    if rad: aktive_methoden.append("Rad")
    if monte: aktive_methoden.append("Monte Carlo")
    st.markdown("**Aktive Methoden:** " + ", ".join(aktive_methoden))

st.markdown("---")
st.caption(f"© {date.today().year} EuroMillions App • Entwickelt mit ❤️")
