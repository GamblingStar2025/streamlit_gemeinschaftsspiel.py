
import streamlit as st
from datetime import date

# === Seiteneinstellungen ===
st.set_page_config(page_title="EuroMillions Tipps & Analyse", layout="centered")

st.title("🎯 EuroMillions Analyse & Tipp-Generator")

# === Moduswahl ===
modus = st.radio("🧑‍🤝‍🧑 Spielmodus wählen", ["👤 Einzelspieler", "👥 Gemeinschaftsspiel"])

# === Länderauswahl & Währung ===
land = st.selectbox("🌍 Land wählen", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇫🇷 Frankreich", "🇦🇹 Österreich"])
waehrung = "CHF" if "Schweiz" in land else "€"
tipp_preis = 3.5 if "Schweiz" in land else 2.5

# === Simulation & KI-Wichtung ===
ki_gewichtung = st.slider("🧠 KI-Gewichtung (%)", 0, 200, 100, step=10)
sim_stufen = st.slider("🎲 Simulationen", 1, 1_000_000, 100_000, step=1000)

# === Tippanzahl-Slider je nach Modus ===
if modus == "👤 Einzelspieler":
    anzahl_tipps = st.slider("🎟️ Anzahl Tipps", 0, 50, 5)
else:
    anzahl_tipps = st.slider("🎟️ Anzahl Tipps", 0, 500, 50, step=50)

# === Kostenanzeige ===
gesamtkosten = anzahl_tipps * tipp_preis
st.markdown(f"💰 **Gesamtkosten:** {gesamtkosten:.2f} {waehrung}")

# === Methodenanzeige ===
with st.expander("🔬 Eingesetzte Analyse-Methoden"):
    st.markdown("- 🔥 Hot/Cold-Zahlen")
    st.markdown("- ♻️ Rad-Prinzip (wiederkehrende Zahlen)")
    st.markdown("- 🧠 LSTM-KI-Vorhersage")
    st.markdown("- 🧩 Clusterbildung (0–9, 10–19 usw.)")
    st.markdown("- 🔗 Top-Zahl-Paare")
    st.markdown("- 🎲 Monte Carlo Simulation")
    st.markdown(f"- 📊 Gewichtung: {ki_gewichtung}%")
    st.markdown(f"- 🎯 Simulationen: {sim_stufen}")

# === Generierung Button (Platzhalter) ===
if st.button("🚀 Tipps generieren"):
    st.success(f"{anzahl_tipps} Tipps werden mit den gewählten Methoden erstellt...")
    for i in range(anzahl_tipps):
        st.write(f"Tipp {i+1}: [Zahlen folgen ...]")

# === Export CSV Placeholder ===
st.download_button("⬇️ Export als CSV", "Tipp1,2,3,4,5; Sterne1,2\n", file_name="euromillions_tipps.csv")
