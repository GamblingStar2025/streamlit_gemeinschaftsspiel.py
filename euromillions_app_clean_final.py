
import streamlit as st
import pandas as pd
import numpy as np
import random
from collections import Counter

st.set_page_config(page_title="EuroMillions KI", layout="centered")
st.title("🎯 EuroMillions KI App")

# === Navigation Tabs ===
tabs = st.tabs(["🏁 Start", "🎮 Spielmodus", "📊 Strategien", "📥 Auswertung"])

# === START ===
with tabs[0]:
    st.subheader("Willkommen zur EuroMillions Analyse-App")
    st.markdown("Erlebe Statistik, KI & Musteranalyse für bessere Gewinnchancen.")
    st.markdown("Wähle deinen Spielmodus und lade echte Ziehungen zur Analyse.")

# === SPIELMODUS ===
with tabs[1]:
    st.subheader("🎮 Spielmodus")
    land = st.selectbox("Wähle dein Land", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇦🇹 Österreich", "🇫🇷 Frankreich", "🇪🇸 Spanien"])
    waehrung = "CHF" if "Schweiz" in land else "€"
    preis = 3.5 if "Schweiz" in land else 2.5

    modus = st.radio("Modus", ["Einzelspieler", "Gemeinschaftsspiel"])
    einsatz = st.slider("Einsatz", 1 if modus == "Einzelspieler" else 50,
                        50 if modus == "Einzelspieler" else 500,
                        step=1 if modus == "Einzelspieler" else 50)

    tipps = int(einsatz / preis)
    st.info(f"📄 Tipps: {tipps} | 💰 Gesamtkosten: {waehrung} {einsatz:.2f}")

    if st.button("🎯 Tipps generieren"):
        tipps_data = []
        for _ in range(tipps):
            haupt = sorted(random.sample(range(1, 51), 5))
            sterne = sorted(random.sample(range(1, 13), 2))
            tipps_data.append({"Hauptzahlen": ", ".join(map(str, haupt)),
                               "Sternzahlen": ", ".join(map(str, sterne))})
        df_tipps = pd.DataFrame(tipps_data)
        st.dataframe(df_tipps)
        csv = df_tipps.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Tipps als CSV speichern", csv, "euromillions_tipps.csv")

# === STRATEGIE ===
with tabs[2]:
    st.subheader("📊 Strategien")
    upload = st.file_uploader("CSV-Datei mit Ziehungen (5 Hauptzahlen)", type="csv")
    if upload:
        df = pd.read_csv(upload)
        zahlen = df.iloc[:, :5].values.tolist()

        alle = [z for zeile in zahlen for z in zeile]
        counter = Counter(alle)
        hot = [n for n, _ in counter.most_common(5)]
        cold = [n for n, _ in counter.most_common()[-5:]]

        st.markdown(f"🔥 **Hot-Zahlen**: {', '.join(map(str, hot))}")
        st.markdown(f"❄️ **Cold-Zahlen**: {', '.join(map(str, cold))}")

        rad = []
        for i in range(len(zahlen) - 10):
            rad.extend(set(zahlen[i]).intersection(zahlen[i+10]))
        if rad:
            st.markdown(f"♻️ **Rad-Zahlen**: {', '.join(map(str, sorted(set(rad))))}")
        else:
            st.info("Keine wiederkehrenden Zahlen erkannt.")

        lstm_tipp = sorted(random.sample(range(1, 51), 5))
        st.markdown(f"🤖 **LSTM-KI-Tipp (Demo)**: {', '.join(map(str, lstm_tipp))}")

# === AUSWERTUNG ===
with tabs[3]:
    st.subheader("📥 Auswertung")
    gezogene = st.text_input("Gezogene Hauptzahlen (z.B. 1,3,14,22,38)")
    gezogene_set = set(int(x.strip()) for x in gezogene.split(",") if x.strip().isdigit())

    datei = st.file_uploader("CSV mit generierten Tipps laden", type="csv")
    if datei and gezogene_set:
        df_check = pd.read_csv(datei)
        df_check["Treffer"] = df_check["Hauptzahlen"].apply(lambda x: len(set(map(int, x.split(","))).intersection(gezogene_set)))
        st.dataframe(df_check.sort_values("Treffer", ascending=False))
