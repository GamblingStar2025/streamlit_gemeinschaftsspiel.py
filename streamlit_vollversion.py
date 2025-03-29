import streamlit as st
import pandas as pd
import random
from collections import Counter

# === Gemeinschaftsspiel-Logik ===
def gemeinschaftsspiel_strategie(einsatz):
    base_tips = 14
    multiplier = 8
    stufen = [50, 100, 150, 200, 250]

    if einsatz not in stufen:
        raise ValueError("Einsatz muss 50, 100, 150, 200 oder 250 sein.")

    tipps = base_tips + ((einsatz - 50) // 50) * multiplier
    ki_gewichtung = 50 + ((einsatz - 50) // 50) * 10
    monte_carlo_iterationen = 100000 + ((einsatz - 50) // 50) * 50000

    return {
        "einsatz": einsatz,
        "tipps": tipps,
        "ki_gewichtung": ki_gewichtung,
        "simulationen": monte_carlo_iterationen,
        "stufe": f"Level {stufen.index(einsatz)+1}/5"
    }

# === Dummy-Vorhersagefunktion (Simulation) ===
def generiere_tipps(anzahl, zahlenpool):
    tipps = []
    for _ in range(anzahl):
        haupt = sorted(random.sample(zahlenpool, 5))
        sterne = sorted(random.sample(range(1, 13), 2))
        tipps.append((haupt, sterne))
    return tipps

# === Streamlit UI ===
st.set_page_config(page_title="Gemeinschaftsspiel Euromillions", layout="centered")
st.title("🎯 Gemeinschaftsspiel & Einzelspiel Euromillions")

modus = st.radio("Modus wählen:", ["🎮 Einzelspieler", "👥 Gemeinschaftsspiel"])

if modus == "🎮 Einzelspieler":
    st.header("🔹 Einzelspiel-Vorhersage")
    anzahl = st.slider("Wie viele Tipps möchtest du generieren?", 1, 20, 5)
    if st.button("🔮 Tipps generieren"):
        tipps = generiere_tipps(anzahl, list(range(1, 51)))
        df = pd.DataFrame([{"Tipp": i+1,
                            "Hauptzahlen": ", ".join(map(str, t[0])),
                            "Sternzahlen": ", ".join(map(str, t[1]))} for i, t in enumerate(tipps)])
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 CSV herunterladen", data=csv, file_name="Einzelspiel_Tipps.csv")

if modus == "👥 Gemeinschaftsspiel":
    st.header("🔹 Gemeinschaftsspiel-Strategie")
    einsatz = st.selectbox("💰 Einsatzbetrag wählen:", [50, 100, 150, 200, 250])

    if einsatz:
        strategie = gemeinschaftsspiel_strategie(einsatz)
        st.subheader(f"🧮 Strategie für {strategie['einsatz']}€ Beitrag")
        st.metric("🎟️ Tipps insgesamt", f"{strategie['tipps']}")
        st.metric("🧠 KI-Gewichtung", f"{strategie['ki_gewichtung']}%")
        st.metric("🎲 Simulationen", f"{strategie['simulationen']:,}")
        st.metric("🔢 Stufe", strategie['stufe'])

        if st.button("🧠 Gemeinschaftstipps generieren"):
            tipps = generiere_tipps(strategie['tipps'], list(range(1, 51)))
            df = pd.DataFrame([{"Tipp": i+1,
                                "Hauptzahlen": ", ".join(map(str, t[0])),
                                "Sternzahlen": ", ".join(map(str, t[1]))} for i, t in enumerate(tipps)])
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 CSV herunterladen", data=csv, file_name="Gemeinschaftstipps.csv")
