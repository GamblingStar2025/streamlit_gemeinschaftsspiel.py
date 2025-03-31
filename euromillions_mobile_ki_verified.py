
import streamlit as st
import pandas as pd
import random
from collections import Counter

st.set_page_config(page_title="EuroMillions KI", layout="centered")
st.title("🎯 EuroMillions KI App (Stabile Version)")

# Init States
if "page" not in st.session_state:
    st.session_state.page = "start"
if "ziehungen" not in st.session_state:
    st.session_state.ziehungen = None

# Start
if st.session_state.page == "start":
    st.subheader("Willkommen zur intelligenten Lottoanalyse")
    if st.button("🚀 Los geht's"):
        st.session_state.page = "spielmodus"

# Spielmodus
elif st.session_state.page == "spielmodus":
    st.subheader("🎮 Spielmodus")
    land = st.selectbox("Land", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇦🇹 Österreich"])
    preis = 3.5 if "Schweiz" in land else 2.5
    waehrung = "CHF" if "Schweiz" in land else "€"

    modus = st.radio("Modus", ["Einzelspieler", "Gemeinschaftsspiel"])
    einsatz = st.slider("Einsatz", 1 if modus == "Einzelspieler" else 50, 50 if modus == "Einzelspieler" else 500, step=1 if modus == "Einzelspieler" else 50)
    tipps = int(einsatz // preis)
    st.info(f"🎟️ Tipps: {tipps} | 💰 {waehrung} {einsatz:.2f}")

    if st.button("➡️ Zur Analyse"):
        st.session_state.tipps = tipps
        st.session_state.page = "analyse"

# Analyse
elif st.session_state.page == "analyse":
    st.subheader("📊 Analyse & Simulation")

    # CSV bleibt im Speicher
    upload = st.file_uploader("📥 Ziehungen (CSV mit 5 Zahlen)", type="csv")
    if upload:
        st.session_state.ziehungen = pd.read_csv(upload)

    if st.session_state.ziehungen is not None:
        df = st.session_state.ziehungen
        zahlen = df.iloc[:, :5].values.tolist()
        flat = [z for ziehung in zahlen for z in ziehung]
        counter = Counter(flat)
        hot = [n for n, _ in counter.most_common(20)]
        rad = [z for i in range(len(zahlen)-10) for z in set(zahlen[i]).intersection(zahlen[i+10])]
        rad = sorted(set(rad))

        st.write("🔥 Hot-Zahlen:", hot[:5])
        st.write("♻️ Wiederkehrer:", rad[:5] if rad else "Keine")

        w_hot = st.slider("Hot/Cold Gewichtung", 0, 200, 40)
        w_rad = st.slider("Rad-Prinzip Gewichtung", 0, 200, 30)
        w_random = st.slider("Zufall Gewichtung", 0, 200, 30)
        simulationen = st.number_input("Anzahl Simulationen", 100, 100000, 1000, 100)

        pool = hot[:10] * w_hot + rad * w_rad + random.sample(range(1, 51), 10) * w_random

        if st.button("🎯 Simulation starten"):
            if pool:
                counter = Counter()
                for _ in range(int(simulationen)):
                    tipp = tuple(sorted(random.sample(pool, 5)))
                    counter[tipp] += 1
                bester = list(counter.most_common(1)[0][0])
                st.session_state.bester_tipp = bester
                st.session_state.page = "auswertung"
            else:
                st.warning("Pool leer – bitte Gewichtungen prüfen.")

# Auswertung
elif st.session_state.page == "auswertung":
    st.subheader("📥 Auswertung")
    gezogen = st.text_input("Gezogene Zahlen (z. B. 1,2,3,4,5)")
    gezogen_set = set(int(x.strip()) for x in gezogen.split(",") if x.strip().isdigit())

    if st.session_state.get("bester_tipp"):
        tipp_set = set(st.session_state.bester_tipp)
        st.info(f"Dein Tipp: {', '.join(map(str, st.session_state.bester_tipp))}")
        if gezogen_set:
            treffer = len(tipp_set.intersection(gezogen_set))
            st.success(f"✅ Treffer: {treffer} von 5")
