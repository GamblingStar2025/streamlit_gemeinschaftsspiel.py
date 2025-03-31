
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

if st.session_state.page == "start":
    st.image("https://cdn-icons-png.flaticon.com/512/869/869636.png", width=100)
    st.markdown("Willkommen bei deiner persönlichen Lotto-Analyse.")
    if st.button("🎬 Starte App"):
        st.session_state.page = "spiel"

elif st.session_state.page == "spiel":
    st.subheader("🎮 Spielmodus & Einsatz")
    land = st.selectbox("🌍 Dein Land", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇦🇹 Österreich", "🇪🇸 Spanien"])
    preis = 3.5 if "Schweiz" in land else 2.5
    waehrung = "CHF" if "Schweiz" in land else "€"

    modus = st.radio("Wähle Modus", ["Einzelspieler", "Gemeinschaftsspiel"])
    einsatz = st.slider("💰 Einsatz", 1 if modus == "Einzelspieler" else 50, 50 if modus == "Einzelspieler" else 500, step=1 if modus == "Einzelspieler" else 50)
    tipps = int(einsatz // preis)
    st.success(f"🎟️ Anzahl Tipps: {tipps} | Preis je Tipp: {waehrung} {preis:.2f} | Gesamt: {waehrung} {einsatz:.2f}")

    if st.button("➡️ Weiter zur Analyse"):
        st.session_state.tipps = tipps
        st.session_state.page = "analyse"

elif st.session_state.page == "analyse":
    st.subheader("🔎 Analyse & Simulation")

    upload = st.file_uploader("📥 Ziehungen hochladen (CSV mit 5 Zahlen)", type="csv")
    if upload:
        st.session_state.ziehungen = pd.read_csv(upload)

    if st.session_state.ziehungen is not None:
        df = st.session_state.ziehungen
        zahlen_raw = df.iloc[:, :5].values.tolist()
        zahlen = [[int(z) for z in zeile if isinstance(z, (int, float)) and not pd.isna(z)] for zeile in zahlen_raw]
        flat = [z for ziehung in zahlen for z in ziehung if isinstance(z, int)]

        counter = Counter(flat)
        hot = [n for n, _ in counter.most_common(20)]
        rad = [z for i in range(len(zahlen)-10) for z in set(zahlen[i]).intersection(zahlen[i+10])]
        rad = sorted(set(rad))
        cluster = [z for z in flat if isinstance(z, int) and 10 <= z <= 39]

        st.markdown(f"🔥 <b>Hot-Zahlen:</b> {', '.join(map(str, hot[:5]))}", unsafe_allow_html=True)
        st.markdown(f"♻️ <b>Wiederkehrer:</b> {', '.join(map(str, rad[:5])) if rad else 'Keine gefunden'}", unsafe_allow_html=True)

        w_hot = st.slider("Hot/Cold", 0, 200, 40)
        w_rad = st.slider("Rad-Prinzip", 0, 200, 30)
        w_random = st.slider("Zufall", 0, 200, 20)
        w_cluster = st.slider("Cluster (10–39)", 0, 200, 10)
        ki_summe = w_hot + w_rad + w_random + w_cluster
        st.info(f"🧮 KI-Gesamtnutzung: {ki_summe} % von max. 800 %")

        sims = st.number_input("🔁 Simulationen", 100, 1000000, 1000, 100)
        pool = hot[:10] * w_hot + rad * w_rad + cluster * w_cluster + random.sample(range(1, 51), 10) * w_random
        pool_unique = list(set(pool))

        if st.button("🎯 Simulation starten"):
            if len(pool_unique) >= 5:
                zähler = Counter()
                for _ in range(int(sims)):
                    ziehung = tuple(sorted(random.sample(pool_unique, 5)))
                    zähler[ziehung] += 1
                beste_tipps = [list(t[0]) for t in zähler.most_common(st.session_state.tipps)]
                sterne = [tuple(sorted(random.sample(range(1, 13), 2))) for _ in range(len(beste_tipps))]
                st.session_state.beste_tipps = list(zip(beste_tipps, sterne))
                st.session_state.page = "auswertung"
            else:
                st.error("⚠️ Nicht genügend Zahlen im Pool – bitte CSV und Gewichtungen prüfen!")

elif st.session_state.page == "auswertung":
    st.subheader("📊 Auswertung deiner Tipps")
    gezogen = st.text_input("Gezogene Zahlen (z. B. 1,2,3,4,5)")
    sterne_input = st.text_input("Gezogene Sternzahlen (z. B. 1, 12)")
    gez_set = set(int(x.strip()) for x in gezogen.split(",") if x.strip().isdigit())
    sterne_set = set(int(s.strip()) for s in sterne_input.split(",") if s.strip().isdigit())

    if st.session_state.get("beste_tipps"):
        for i, (tipp, sterne) in enumerate(st.session_state.beste_tipps, 1):
            tipp_set = set(tipp)
            treffer = len(tipp_set.intersection(gez_set)) if gez_set else 0
            
sterntreffer = len(set(sterne).intersection(sterne_set)) if sterne_set else 0
        # Beispielhafte Gewinnlogik
        gewinn_matrix = {
            (5, 2): 100000000,
            (5, 1): 500000,
            (5, 0): 50000,
            (4, 2): 4000,
            (4, 1): 200,
            (3, 2): 100,
            (2, 2): 20,
            (3, 1): 15,
            (3, 0): 10,
            (1, 2): 10,
            (2, 1): 8,
        }
        gewinn = gewinn_matrix.get((treffer, sterntreffer), 0)
        gesamt_gewinn = st.session_state.get("gesamt_gewinn", 0) + gewinn
        st.session_state["gesamt_gewinn"] = gesamt_gewinn

            st.markdown(f'''
            <div style="border:1px solid #ccc; border-radius:10px; padding:10px; margin:10px;">
            <strong>Tipp {i}</strong><br>
            &#128290; <b>Zahlen:</b> {', '.join(map(str, tipp))}<br>
            &#127775; <b>Sterne:</b> {sterne[0]} & {sterne[1]}<br>
            &#127919; <b>Haupttreffer:</b> {treffer} von 5<br>
            &#10035;&#65039; <b>Sterntreffer:</b> {sterntreffer} von 2<br>💰 <b>Gewinn:</b> {gewinn:.2f} {waehrung}
            </div>
            ''', unsafe_allow_html=True)

# Gesamtauswertung anzeigen
if "gesamt_gewinn" in st.session_state:
    st.markdown(f"<h3 style='color:green;'>💸 Gesamtgewinn: {st.session_state['gesamt_gewinn']:.2f} {waehrung}</h3>", unsafe_allow_html=True)
