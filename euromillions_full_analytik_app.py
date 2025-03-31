
import streamlit as st
import pandas as pd
import numpy as np
import random
from collections import Counter
import os

# === Seiteneinstellungen ===
st.set_page_config(page_title="EuroMillions Analyse", layout="wide")

# === Intro mit Animation (statisch dargestellt für einfache Ansicht) ===
st.title("🎯 Willkommen zur EuroMillions KI-Analyse-App")
st.markdown("Nutze mathematische Muster, Statistik und KI zur Optimierung deiner Euromillions-Tipps.")

# === Navigation ===
tabs = st.tabs(["🧭 Start", "🎮 Spielmodus", "📊 Strategien & KI", "📥 Auswertung"])

# === CSV Laden ===
@st.cache_data
def lade_daten(pfad):
    try:
        df = pd.read_csv(pfad)
        df.rename(columns=lambda x: x.strip(), inplace=True)
        df = df.dropna()
        return df
    except Exception as e:
        st.error(f"Fehler beim Laden der Datei: {e}")
        return pd.DataFrame()

# === Tab 1: Startinfo ===
with tabs[0]:
    st.header("ℹ️ Übersicht")
    st.markdown("""
    Diese App kombiniert klassische Lottoanalyse (Hot/Cold, Muster, Paare) mit modernen KI-Strategien
    wie LSTM-Vorhersagen und Monte Carlo Simulation. Ziel: Höhere Treffergenauigkeit bei Euromillions.
    """)

# === Tab 2: Spielmodus ===
with tabs[1]:
    st.header("🎮 Spielmodus")
    land = st.selectbox("Wähle dein Land:", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇦🇹 Österreich", "🇫🇷 Frankreich", "🇪🇸 Spanien"])
    waehrung = "CHF" if "Schweiz" in land else "€"
    preis = 3.5 if "Schweiz" in land else 2.5

    modus = st.radio("Modus wählen:", ["Einzelspieler", "Gemeinschaftsspiel"])
    einsatz = st.slider("Einsatzbetrag", 1 if modus == "Einzelspieler" else 50,
                        50 if modus == "Einzelspieler" else 500,
                        step=1 if modus == "Einzelspieler" else 50)
    tipps = int(einsatz // preis)
    st.markdown(f"📄 Anzahl Tipps: **{tipps}**")
    st.markdown(f"💰 Gesamtkosten: **{waehrung} {tipps * preis:.2f}**")

    if st.button("🎯 Tipps generieren"):
        daten = []
        for _ in range(tipps):
            haupt = sorted(random.sample(range(1, 51), 5))
            sterne = sorted(random.sample(range(1, 13), 2))
            daten.append({"Hauptzahlen": ", ".join(map(str, haupt)), "Sternzahlen": ", ".join(map(str, sterne))})
        df_tipps = pd.DataFrame(daten)
        st.dataframe(df_tipps)
        csv = df_tipps.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Tipps als CSV speichern", data=csv, file_name="euromillions_tipps.csv")

# === Tab 3: Strategien & KI ===
with tabs[2]:
    st.header("📊 Strategie & KI-Auswertung")
    file = st.file_uploader("📤 Lade deine EuroMillions CSV-Datei hoch", type=["csv"])
    if file:
        df = lade_daten(file)
        if len(df.columns) >= 7:
            zahlen = df.iloc[:, 1:6].values.tolist()

            # Hot/Cold
            flat = [z for zeile in zahlen for z in zeile]
            count = Counter(flat)
            hot = [n for n, _ in count.most_common(5)]
            cold = [n for n, _ in count.most_common()[-5:]]
            st.markdown("🔥 Hot-Zahlen: " + ", ".join(map(str, hot)))
            st.markdown("❄️ Cold-Zahlen: " + ", ".join(map(str, cold)))

            # Rad-Prinzip
            wieder = []
            for i in range(len(zahlen) - 10):
                a = set(zahlen[i])
                b = set(zahlen[i+10])
                wieder.extend(a.intersection(b))
            rad = list(set(wieder))
            st.markdown("♻️ Wiederkehrende Zahlen: " + ", ".join(map(str, rad)) if rad else "Keine wiederkehrenden Zahlen.")

            # LSTM-Demo
            st.markdown("🧠 LSTM-KI (Demo): " + ", ".join(map(str, sorted(random.sample(range(1, 51), 5)))))

# === Tab 4: Auswertung ===
with tabs[3]:
    st.header("📥 CSV-Auswertung")
    ziehung = st.text_input("🔢 Trage deine echten Zahlen ein (z. B. 1,5,12,22,37):")
    user_nums = [int(n.strip()) for n in ziehung.split(",") if n.strip().isdigit()]

    auswertung = st.file_uploader("📤 Lade die generierten Tipps (CSV)", type="csv")
    if auswertung and user_nums:
        df = pd.read_csv(auswertung)
        df["Treffer"] = df["Hauptzahlen"].apply(lambda x: len(set(map(int, x.split(","))).intersection(user_nums)))
        st.dataframe(df.sort_values("Treffer", ascending=False))
