
import streamlit as st
import pandas as pd
import random
from collections import Counter

st.set_page_config(page_title="EuroMillions KI", layout="centered")
st.markdown("<h1 style='text-align:center;'>💫 EuroMillions Mobile App</h1>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "start"
if "ziehungen" not in st.session_state:
    st.session_state.ziehungen = None

# START
if st.session_state.page == "start":
    st.image("https://cdn-icons-png.flaticon.com/512/869/869636.png", width=100)
    st.markdown("Willkommen bei deiner persönlichen Lotto-Analyse.")
    if st.button("🎬 Starte App"):
        st.session_state.page = "spiel"

# SPIELMODUS
elif st.session_state.page == "spiel":
    st.subheader("🎮 Spielmodus & Einsatz")
    land = st.selectbox("🌍 Dein Land", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇦🇹 Österreich", "🇪🇸 Spanien"])
    preis = 3.5 if "Schweiz" in land else 2.5
    waehrung = "CHF" if "Schweiz" in land else "€"

    modus = st.radio("Wähle Modus", ["Einzelspieler", "Gemeinschaftsspiel"])
    einsatz = st.slider("💰 Einsatz", 1 if modus == "Einzelspieler" else 50,
                        50 if modus == "Einzelspieler" else 500,
                        step=1 if modus == "Einzelspieler" else 50)
    tipps = int(einsatz // preis)
    st.success(f"🎟️ Anzahl Tipps: {tipps} | Preis je Tipp: {waehrung} {preis:.2f} | Gesamt: {waehrung} {einsatz:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Zurück"):
            st.session_state.page = "start"
    with col2:
        if st.button("➡️ Weiter zur Analyse"):
            st.session_state.tipps = tipps
            st.session_state.page = "analyse"

# ANALYSE
elif st.session_state.page == "analyse":
    st.subheader("🔎 Analyse & Simulation")

    upload = st.file_uploader("📥 Ziehungen hochladen (CSV mit 5 Zahlen)", type="csv")
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
        cluster = [z for z in flat if 10 <= z <= 39]

        st.markdown(f"🔥 **Hot-Zahlen**: {', '.join(map(str, hot[:5]))}")
        st.markdown(f"♻️ **Wiederkehrer**: {', '.join(map(str, rad[:5])) if rad else 'Keine gefunden'}")

        # Gewichtungen
        st.markdown("### 🧠 KI-Gewichtungen")
        w_hot = st.slider("Hot/Cold", 0, 200, 40)
        w_rad = st.slider("Rad-Prinzip", 0, 200, 30)
        w_random = st.slider("Zufall", 0, 200, 20)
        w_cluster = st.slider("Cluster (10–39)", 0, 200, 10)
        ki_summe = w_hot + w_rad + w_random + w_cluster
        st.info(f"🧮 KI-Gesamtnutzung: {ki_summe} % von max. 800 %")

        sims = st.number_input("🔁 Simulationen", 100, 100000, 1000, 100)

        pool = hot[:10] * w_hot + rad * w_rad + cluster * w_cluster + random.sample(range(1, 51), 10) * w_random
        pool_unique = list(set(pool))

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Zurück"):
                st.session_state.page = "spiel"
        with col2:
            if st.button("🎯 Simulation starten"):
                if len(pool_unique) >= 5:
                    zähler = Counter()
                    for _ in range(int(sims)):
                        ziehung = tuple(sorted(random.sample(pool_unique, 5)))
                        zähler[ziehung] += 1
                    beste_tipps = [list(t[0]) for t in zähler.most_common(st.session_state.tipps)]
                    st.session_state.beste_tipps = beste_tipps
                    st.session_state.page = "auswertung"
                else:
                    st.error("⚠️ Nicht genügend verschiedene Zahlen im Pool – bitte CSV und Gewichtungen prüfen!")

# AUSWERTUNG
elif st.session_state.page == "auswertung":
    st.subheader("📊 Auswertung deiner Tipps")
    gezogen = st.text_input("Gezogene Zahlen (z. B. 1,2,3,4,5)")
    gez_set = set(int(x.strip()) for x in gezogen.split(",") if x.strip().isdigit())

    if st.session_state.get("beste_tipps"):
        for i, tipp in enumerate(st.session_state.beste_tipps, 1):
            st.info(f"Tipp {i}: {', '.join(map(str, tipp))}")
            if gez_set:
                treffer = len(set(tipp).intersection(gez_set))
                st.success(f"🎯 Treffer: {treffer} von 5")

    if st.button("⬅️ Zurück zur Analyse"):
        st.session_state.page = "analyse"
