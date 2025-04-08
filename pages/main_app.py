
# === Spielmodus und Tippanzahl-Definition sicherstellen ===
modus = st.radio("🧑‍🤝‍🧑 Spielmodus", ["Einzelspieler", "Gemeinschaftsspiel"])
max_tipps = 50 if modus == "Einzelspieler" else 500
anzahl_tipps = st.slider("🎟️ Anzahl Tipps", 1, max_tipps, 5)


import streamlit as st

st.title("🎯 EuroGenius – Methodeinstellungen")

st.markdown("### 🌐 Gesamt-KI-Faktor")
ki_global = st.slider("KI-Gesamtgewichtung (%)", 0, 200, 100)

st.markdown("### 🔧 Einzelne Methoden-Gewichtungen")
hot = st.slider("🔥 Hot-Zahlen", 0, 200, 100)
cold = st.slider("❄️ Cold-Zahlen", 0, 200, 100)
cluster = st.slider("📊 Cluster", 0, 200, 100)
rad = st.slider("♻️ Rad-Prinzip", 0, 200, 100)
monte = st.slider("🎲 Monte Carlo", 0, 200, 100)

st.markdown("### 📈 Effektive Gewichtung mit globalem KI-Faktor")
for name, val in {
    "Hot-Zahlen": hot,
    "Cold-Zahlen": cold,
    "Cluster": cluster,
    "Rad": rad,
    "Monte Carlo": monte
}.items():
    effektiv = round(val * ki_global / 100, 2)
    st.progress(min(int(effektiv), 100), text=f"{name}: {effektiv}%")

import random
import pandas as pd

# === Tipp-Generierung ===
st.markdown("## 🎯 Tipp-Generator")
if st.button("🔁 Tipps generieren"):
    tipps = []
    for _ in range(anzahl_tipps):
        hauptzahlen = sorted(random.sample(range(1, 51), 5))
        sterne = sorted(random.sample(range(1, 13), 2))
        tipps.append({"Hauptzahlen": hauptzahlen, "Sterne": sterne})

    df_tipps = pd.DataFrame([{
        "Tipp": i+1,
        "Hauptzahlen": " - ".join(map(str, t["Hauptzahlen"])),
        "Sternzahlen": " - ".join(map(str, t["Sterne"]))
    } for i, t in enumerate(tipps)])

    st.dataframe(df_tipps)

# === CSV Upload ===
st.markdown("## 📁 Ziehungsdaten hochladen")
uploaded_file = st.file_uploader("Lade eine CSV-Datei mit Ziehungsdaten hoch", type=["csv"])
if uploaded_file:
    ziehungen_df = pd.read_csv(uploaded_file)
    st.success("Datei erfolgreich geladen!")
    st.dataframe(ziehungen_df.head())
