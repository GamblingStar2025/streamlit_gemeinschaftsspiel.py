
import streamlit as st
import pandas as pd
import numpy as np
import random
import os
import uuid
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense

st.set_page_config(page_title="EuroMillions KI-App", layout="centered")

# Session-Init
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False
if "user" not in st.session_state:
    st.session_state.user = None
if "groups" not in st.session_state:
    st.session_state.groups = {}
if "TEAM_SESSIONS" not in st.session_state:
    st.session_state.TEAM_SESSIONS = {}
if "team_tipps" not in st.session_state:
    st.session_state.team_tipps = {}

# === INTRO SEITE ===
if not st.session_state.intro_done:
    st.title("🎯 Willkommen zur EuroMillions KI-App")
    st.subheader("Nutze Muster, Wahrscheinlichkeiten und Teamplay für bessere Tipps.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/EuroMillions_logo.svg/320px-EuroMillions_logo.svg.png", width=200)
    st.markdown("---")
    st.success("Wähle deine Strategie. Spiele allein oder im Team.")
    if st.button("🚀 Jetzt starten"):
        st.session_state.intro_done = True
    st.stop()

# === TABS ===
tabs = st.tabs(["🏠 Start", "🎮 Spielmodus", "🧠 Strategie & Tipp", "📈 Auswertung", "⚙️ Einstellungen"])

with tabs[0]:
    st.title("Login")
    username = st.text_input("👤 Benutzername")
    land = st.selectbox("🌍 In welchem Land spielst du?", [
        "🇨🇭 Schweiz", "🇦🇹 Österreich", "🇧🇪 Belgien", "🇫🇷 Frankreich", "🇮🇪 Irland",
        "🇱🇺 Luxemburg", "🇵🇹 Portugal", "🇪🇸 Spanien", "🇬🇧 Vereinigtes Königreich"
    ])
    if st.button("🚀 Login"):
        if username:
            st.session_state.user = username
            st.session_state.land = land
            st.success(f"Eingeloggt als {username} ({land})")
        else:
            st.error("Bitte Namen eingeben.")

with tabs[1]:
    st.header("🎮 Wähle deinen Spielmodus")
    
modus = st.radio("Modus wählen:", ["🎮 Einzelspieler", "👥 Gemeinschaftsspiel", "🤝 Team-Modus"])
st.session_state["modus"] = modus

    if modus in ["👥 Gemeinschaftsspiel", "🤝 Team-Modus"]:
        gruppe = st.text_input("🧩 Gruppe erstellen oder beitreten")
        if gruppe:
            st.session_state.groups[st.session_state.user] = gruppe
            st.success(f"Du bist in der Gruppe: {gruppe}")

with tabs[2]:
    st.header("🧠 Tippstrategie & Generieren")
    land = st.session_state.get("land", "🇦🇹 Österreich")

    def preis_pro_tipp_für_land(land):
        if "🇨🇭" in land or "Schweiz" in land:
            return 3.50
        elif "🇬🇧" in land or "Vereinigtes Königreich" in land:
            return 2.50
        return 2.50

    preis_pro_tipp = preis_pro_tipp_für_land(land)
    
modus = st.session_state.get("modus", "🎮 Einzelspieler")
if modus == "🎮 Einzelspieler":
    einsatz = st.slider("💰 Einsatzbetrag", min_value=1, max_value=50, step=1)
else:
    einsatz = st.slider("💰 Einsatzbetrag", min_value=50, max_value=500, step=50)

    anzahl_tipps = int(einsatz // preis_pro_tipp)

    waehrung = "€"
    if "🇨🇭" in land:
        waehrung = "CHF"
    elif "🇬🇧" in land:
        waehrung = "£"

    st.markdown(f"🧾 Preis pro Tipp in {land}: **{waehrung} {preis_pro_tipp}**")
    st.markdown(f"🎟️ Anzahl Tipps: **{anzahl_tipps}**")

    if st.button("🎯 Tipps generieren"):
        def echte_vorhersagen(n):
            tipps = []
            for _ in range(n):
                haupt = sorted(random.sample(range(1, 51), 5))
                sterne = sorted(random.sample(range(1, 13), 2))
                tipps.append((haupt, sterne))
            return tipps

        tipps = echte_vorhersagen(anzahl_tipps)
        st.session_state.tipps = tipps
        df_out = pd.DataFrame([{
            "Tipp": i+1,
            "Hauptzahlen": ", ".join(map(str, t[0])),
            "Sternzahlen": ", ".join(map(str, t[1]))
        } for i, t in enumerate(tipps)])
        st.session_state.df_out = df_out
        st.dataframe(df_out)
        csv = df_out.to_csv(index=False).encode('utf-8')
        st.download_button("📥 CSV herunterladen", data=csv, file_name="Meine_Tipps.csv")

with tabs[3]:
    st.header("📈 Ziehungs-Auswertung")
    latest_main = st.text_input("Letzte 5 Hauptzahlen (z. B. 10,21,30,42,45):")
    latest_star = st.text_input("Letzte 2 Sternzahlen (z. B. 1,9):")
    tipps_quelle = st.session_state.get("tipps", [])
    if not tipps_quelle:
        st.info("⚠️ Noch keine Tipps vorhanden.")
    else:
        if st.button("📊 Tipps auswerten"):
            try:
                main_numbers = list(map(int, latest_main.strip().split(",")))
                star_numbers = list(map(int, latest_star.strip().split(",")))
                statistik = {}
                for haupt, sterne in tipps_quelle:
                    h = len(set(haupt).intersection(main_numbers))
                    s = len(set(sterne).intersection(star_numbers))
                    key = f"{h}R + {s}S"
                    statistik[key] = statistik.get(key, 0) + 1
                df_stats = pd.DataFrame(statistik.items(), columns=["Treffer", "Anzahl"])
                st.dataframe(df_stats)
            except:
                st.error("Fehlerhafte Eingabe.")

with tabs[4]:
    st.header("⚙️ Einstellungen & Zurücksetzen")
    if st.button("🔁 App zurücksetzen"):
        st.session_state.clear()
        st.experimental_rerun()
