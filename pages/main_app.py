
import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="EuroGenius Tipps", layout="centered")

st.title("🎯 EuroGenius – Dein KI-Tippassistent")

# Spielmodus und Land
modus = st.radio("Modus", ["👤 Einzelspieler", "👥 Gemeinschaft"])
land = st.selectbox("Land", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇫🇷 Frankreich", "🇦🇹 Österreich"])
waehrung = "CHF" if "Schweiz" in land else "€"
preis = 3.5 if "Schweiz" in land else 2.5

# Parametersteuerung
anzahl = st.slider("Anzahl Tipps", 1, 50 if modus == "👤 Einzelspieler" else 500)
ki = st.slider("KI-Gewichtung", 0, 200, 100)
sim = st.slider("Simulationen", 1000, 1000000, 100000)

# Methodenwahl
st.markdown("### 🧠 Analyse-Strategien")
use_hot = st.checkbox("🔥 Hot/Cold", value=True)
use_cluster = st.checkbox("🧩 Cluster", value=True)
use_rad = st.checkbox("♻️ Rad-Prinzip", value=False)
use_monte = st.checkbox("🎲 Monte Carlo", value=True)

kosten = anzahl * preis
st.markdown(f"💰 **Gesamtkosten:** `{kosten:.2f} {waehrung}`")

# Tipps generieren
if st.button("🚀 Tipps generieren"):
    st.subheader("🎟 Deine Tipps")
    methoden = []
    if use_hot: methoden.append("Hot/Cold")
    if use_cluster: methoden.append("Cluster")
    if use_rad: methoden.append("Rad")
    if use_monte: methoden.append("Monte Carlo")
    methoden_str = ", ".join(methoden)
    for i in range(anzahl):
        zahlen = sorted(random.sample(range(1, 51), 5))
        sterne = sorted(random.sample(range(1, 13), 2))
        st.success(f"Tipp {i+1}: {zahlen} ⭐ {sterne}")
        st.caption(f"Methoden: {methoden_str}")

st.markdown("---")
st.subheader("📊 Auswertung deiner Tipps")

gezogene_zahlen = st.text_input("Gezogene Zahlen (5 Zahlen, Komma getrennt)", "10,21,30,42,45")
gezogene_sterne = st.text_input("Gezogene Sterne (2 Zahlen, Komma getrennt)", "1,9")

if st.button("🔍 Auswertung starten"):
    try:
        gez_z = list(map(int, gezogene_zahlen.split(",")))
        gez_s = list(map(int, gezogene_sterne.split(",")))
        if len(gez_z) == 5 and len(gez_s) == 2:
            treffer = []
            for i in range(anzahl):
                zahlen = sorted(random.sample(range(1, 51), 5))
                sterne = sorted(random.sample(range(1, 13), 2))
                z_treffer = len(set(zahlen).intersection(gez_z))
                s_treffer = len(set(sterne).intersection(gez_s))
                st.info(f"Tipp {i+1}: {zahlen} ⭐ {sterne} → 🎯 {z_treffer} Zahlen, ⭐ {s_treffer} Sterne")
        else:
            st.warning("Bitte genau 5 Zahlen und 2 Sterne eingeben.")
    except:
        st.error("Fehlerhafte Eingabe. Bitte Zahlen durch Komma trennen.")

st.caption(f"© {date.today().year} EuroGenius")
