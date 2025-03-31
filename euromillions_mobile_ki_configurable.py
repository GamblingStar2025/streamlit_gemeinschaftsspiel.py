
import streamlit as st
import pandas as pd
import numpy as np
import random
from collections import Counter

st.set_page_config(page_title="EuroMillions KI", layout="centered")
st.markdown("<h2 style='text-align:center;'>🎯 EuroMillions KI App</h2>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "start"

# === Startseite
if st.session_state.page == "start":
    st.markdown("Willkommen zur mobilen KI-gestützten Lottoanalyse.")
    if st.button("🚀 Jetzt starten"):
        st.session_state.page = "spiel"

# === Spielmodus
elif st.session_state.page == "spiel":
    st.subheader("🎮 Spielmodus & Einsatz")
    land = st.selectbox("🌍 Land wählen", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇦🇹 Österreich", "🇫🇷 Frankreich", "🇪🇸 Spanien"])
    preis = 3.5 if "Schweiz" in land else 2.5
    waehrung = "CHF" if "Schweiz" in land else "€"

    modus = st.radio("Modus", ["Einzelspieler", "Gemeinschaftsspiel"])
    einsatz = st.slider("Einsatz", 1 if modus == "Einzelspieler" else 50, 50 if modus == "Einzelspieler" else 500, step=1 if modus == "Einzelspieler" else 50)
    tipps = int(einsatz // preis)
    st.success(f"🎟️ Tipps: {tipps} | 💸 Kosten: {waehrung} {einsatz:.2f}")

    if st.button("📊 Zur Analyse"):
        st.session_state.tipps = tipps
        st.session_state.page = "analyse"

# === Analyse
elif st.session_state.page == "analyse":
    st.subheader("📊 Strategien & Simulation")
    file = st.file_uploader("📥 Ziehungen hochladen (CSV mit 5 Zahlen pro Ziehung)", type="csv")

    if file:
        df = pd.read_csv(file)
        zahlen = df.iloc[:, :5].values.tolist()
        alle = [z for zeile in zahlen for z in zeile]
        counter = Counter(alle)
        hot = [n for n, _ in counter.most_common(20)]
        cold = [n for n, _ in counter.most_common()[-20:]]

        wieder = []
        for i in range(len(zahlen) - 10):
            wieder.extend(set(zahlen[i]).intersection(zahlen[i+10]))
        rad = sorted(set(wieder))

        st.markdown(f"🔥 **Hot-Zahlen:** {', '.join(map(str, hot[:5]))}")
        st.markdown(f"❄️ **Cold-Zahlen:** {', '.join(map(str, cold[:5]))}")
        st.markdown(f"♻️ **Wiederkehrer:** {', '.join(map(str, rad[:5])) if rad else 'Keine'}")

        # Benutzergewichtungen
        st.markdown("### 🧠 KI-Gewichtung (%)")
        w_hot = st.slider("Hot/Cold", 0, 200, 40)
        w_rad = st.slider("Rad-Prinzip", 0, 200, 30)
        w_lstm = st.slider("LSTM-Vorhersage", 0, 200, 20)
        w_mc = st.slider("Monte Carlo", 0, 200, 10)

        # Multiplikator
        st.markdown("### 🔁 Anzahl Analysen (Multiplikation)")
        sim_count = st.number_input("Wieviele Simulationen?", min_value=0, max_value=1_000_000, value=1000, step=100)

        # Tipp generieren
        gewichtete_pool = (
            hot[:10] * w_hot +
            rad * w_rad +
            random.sample(range(1, 51), 10) * w_lstm +
            random.sample(range(1, 51), 10) * w_mc
        )

        if st.button("🎯 Simulation starten"):
            result_counter = Counter()
            for _ in range(int(sim_count)):
                ziehung = tuple(sorted(random.sample(gewichtete_pool, 5)))
                result_counter[ziehung] += 1
            best_tipp = list(result_counter.most_common(1)[0][0])
            st.session_state.best_tipp = best_tipp
            st.session_state.page = "auswertung"

# === Auswertung
elif st.session_state.page == "auswertung":
    st.subheader("📥 Ziehungsauswertung")
    gezogen = st.text_input("Gezogene Zahlen (z. B. 1,2,3,4,5)")
    gez_set = set(int(x.strip()) for x in gezogen.split(",") if x.strip().isdigit())

    if st.session_state.get("best_tipp") and gez_set:
        tipp_set = set(st.session_state.best_tipp)
        treffer = len(tipp_set.intersection(gez_set))
        st.info(f"Dein Tipp: {', '.join(map(str, st.session_state.best_tipp))}")
        st.success(f"✅ Treffer: {treffer} von 5")
