
import streamlit as st
import pandas as pd
import numpy as np
import random
from collections import Counter

st.set_page_config(page_title="EuroMillions KI-Analyse", layout="wide")

# === Session Init ===
if "page" not in st.session_state:
    st.session_state.page = "intro"

# === Intro / Startseite ===
if st.session_state.page == "intro":
    st.title("🎯 Willkommen zur EuroMillions KI-App")
    st.image("https://cdn-icons-png.flaticon.com/512/9455/9455170.png", width=120)
    st.markdown("Erlebe intelligente Strategien, Statistik und KI für bessere Lottotipps.")
    if st.button("🚀 Jetzt starten"):
        st.session_state.page = "spielmodus"
    st.stop()

# === Spielmodus-Seite ===
if st.session_state.page == "spielmodus":
    st.header("🎮 Spielmodus & Einstellungen")
    land = st.selectbox("🌍 Wähle dein Land:", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇫🇷 Frankreich", "🇪🇸 Spanien", "🇦🇹 Österreich"])
    preis = 3.5 if "Schweiz" in land else 2.5
    waehrung = "CHF" if "Schweiz" in land else "€"

    modus = st.radio("Modus wählen:", ["Einzelspieler", "Gemeinschaftsspiel"])
    einsatz = st.slider("💰 Einsatz", min_value=1 if modus == "Einzelspieler" else 50,
                        max_value=50 if modus == "Einzelspieler" else 500,
                        step=1 if modus == "Einzelspieler" else 50)

    tipps = int(einsatz // preis)
    st.success(f"🎟️ Anzahl Tipps: {tipps} | 💸 Kosten: {waehrung} {einsatz:.2f}")

    if st.button("📊 Zur Strategie & Analyse"):
        st.session_state.page = "strategie"

# === Strategie-Seite ===
if st.session_state.page == "strategie":
    st.header("📊 Strategien & KI-Analyse")

    file = st.file_uploader("📥 Ziehungsdaten hochladen (CSV mit 5 Hauptzahlen pro Ziehung)", type="csv")
    if file:
        df = pd.read_csv(file)
        if df.shape[1] >= 5:
            zahlen = df.iloc[:, :5].values.tolist()

            # Hot/Cold
            alle = [z for ziehung in zahlen for z in ziehung]
            hot = [n for n, _ in Counter(alle).most_common(5)]
            cold = [n for n, _ in Counter(alle).most_common()[-5:]]
            st.markdown(f"🔥 **Hot-Zahlen:** {', '.join(map(str, hot))}")
            st.markdown(f"❄️ **Cold-Zahlen:** {', '.join(map(str, cold))}")

            # Rad-Prinzip
            wiederkehrer = []
            for i in range(len(zahlen) - 10):
                s1, s2 = set(zahlen[i]), set(zahlen[i+10])
                wiederkehrer.extend(s1.intersection(s2))
            rad = sorted(set(wiederkehrer))
            st.markdown(f"♻️ **Wiederkehrende Zahlen:** {', '.join(map(str, rad)) if rad else 'Keine'}")

            # KI-Tipp
            ki = sorted(random.sample(range(1, 51), 5))
            st.markdown(f"🤖 **LSTM-KI-Demo-Tipp:** {', '.join(map(str, ki))}")

            # Button zur Auswertung
            if st.button("📥 Zur Auswertung"):
                st.session_state.page = "auswertung"

# === Auswertung ===
if st.session_state.page == "auswertung":
    st.header("📥 Tipp-Auswertung")
    gezogene = st.text_input("🎯 Ziehungszahlen eingeben (z. B. 1,5,12,22,37):")
    eingabe = [int(n.strip()) for n in gezogene.split(",") if n.strip().isdigit()]

    auswertung = st.file_uploader("📤 Generierte Tipps (CSV)", type="csv")
    if auswertung and eingabe:
        df = pd.read_csv(auswertung)
        if "Hauptzahlen" in df.columns:
            df["Treffer"] = df["Hauptzahlen"].apply(lambda x: len(set(map(int, x.split(","))).intersection(eingabe)))
            st.dataframe(df.sort_values("Treffer", ascending=False))
