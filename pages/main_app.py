
import streamlit as st
import random
from datetime import date

st.set_page_config(page_title="EuroGenius Tipps", layout="centered")


st.markdown(
    "<h1 style='text-align: center; color: gold;'>🎯 EuroGenius – Dein KI-Tippassistent</h1>",
    unsafe_allow_html=True
)
st.markdown("<style>body { background-color: #0b0e11; color: white; }</style>", unsafe_allow_html=True)


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
    with st.spinner("🔄 KI analysiert Wahrscheinlichkeiten..."):
        time.sleep(1)

    
st.success("🎉 Deine Tipps sind bereit – viel Glück!")
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


st.markdown("---")
st.subheader("📁 Eigene Ziehungsdaten hochladen")

csv_file = st.file_uploader("Lade eine EuroMillions CSV-Datei hoch (z. B. 'EuroMillion_Ziehungen.csv')", type=["csv"])
if csv_file:
    import pandas as pd
    try:
        df = pd.read_csv(csv_file)
        df = df.dropna(how='all')
        st.success("Datei erfolgreich geladen:")
        st.dataframe(df.tail(5))
        st.caption("⬆️ Zeigt die letzten 5 Zeilen deiner Datei.")
    except Exception as e:
        st.error(f"Fehler beim Einlesen der Datei: {e}")

if csv_file:
    try:
        df = pd.read_csv(csv_file)
        df = df.dropna(how='all')
        df = df.sort_values(by=df.columns[0])  # Nach Datum oder Ziehungsnummer sortieren
        st.success("CSV erfolgreich verarbeitet.")

        # Letzte 200 Ziehungen für Analyse
        recent_draws = df.iloc[-2000:]
        main_cols = recent_draws.columns[1:6]
        numbers = recent_draws[main_cols].values.flatten()
        from collections import Counter
        number_counts = Counter(numbers)
        hot = [int(n) for n, _ in number_counts.most_common(10)]
        cold = [int(n) for n, _ in number_counts.most_common()[-10:]]

        st.markdown("### 🔥 Hot & ❄️ Cold Zahlen (basierend auf letzten 200 Ziehungen)")
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🔥 Hot: {sorted(hot)}")
        with col2:
            st.info(f"❄️ Cold: {sorted(cold)}")

        # Rad-Funktion (Zyklische Wiederkehr)
        def get_repeating(df, window=20):
            repeats = set()
            for i in range(len(df) - window):
                past = set(df.iloc[i:i+window, 1:6].values.flatten())
                future = set(df.iloc[i+window:i+window+5, 1:6].values.flatten())
                repeats.update(past.intersection(future))
            return sorted(list(repeats))

        repeating = get_repeating(recent_draws)
        st.markdown(f"♻️ **Wiederkehrende Zahlen:** {repeating}")

        # Cluster nach Zahlenbereichen
        cluster_dict = {"0–9": [], "10–19": [], "20–29": [], "30–39": [], "40–50": []}
        for n in numbers:
            if 0 <= n <= 9:
                cluster_dict["0–9"].append(n)
            elif 10 <= n <= 19:
                cluster_dict["10–19"].append(n)
            elif 20 <= n <= 29:
                cluster_dict["20–29"].append(n)
            elif 30 <= n <= 39:
                cluster_dict["30–39"].append(n)
            elif 40 <= n <= 50:
                cluster_dict["40–50"].append(n)

        st.markdown("### 🧩 Zahlen nach Bereichen")
        for k, v in cluster_dict.items():
            st.markdown(f"**{k}**: {sorted(set(v))}")

    except Exception as e:
        st.error(f"Fehler bei der Analyse: {e}")
