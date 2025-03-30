
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

st.set_page_config(page_title="EuroMillions App", layout="centered")

# === Setup: Session & Speicher ===
if "user" not in st.session_state:
    st.session_state.user = None
if "groups" not in st.session_state:
    st.session_state.groups = {}
if "TEAM_SESSIONS" not in st.session_state:
    st.session_state.TEAM_SESSIONS = {}
if "team_tipps" not in st.session_state:
    st.session_state.team_tipps = {}

# === Tabs ===
tabs = st.tabs(["🏠 Start", "🎮 Spielmodus", "🧠 Strategie & Tipp", "📈 Auswertung", "⚙️ Einstellungen"])

# === TAB 1: Start / Login ===
with tabs[0]:
    st.title("🎯 Willkommen zur EuroMillions App")
    st.markdown("Bitte melde dich mit deinem Spielernamen an:")

    username = st.text_input("👤 Benutzername")
    if st.button("🚀 Login"):
        if username:
            st.session_state.user = username
            st.success(f"Eingeloggt als {username}")
        else:
            st.error("Bitte Namen eingeben.")

# === TAB 2: Spielmodus ===
with tabs[1]:
    st.header("🎮 Wähle deinen Spielmodus")

    modus = st.radio("Modus wählen:", ["🎮 Einzelspieler", "👥 Gemeinschaftsspiel", "🤝 Team-Modus"])
    if modus in ["👥 Gemeinschaftsspiel", "🤝 Team-Modus"]:
        gruppe = st.text_input("🧩 Gruppe erstellen oder beitreten")
        if gruppe:
            st.session_state.groups[st.session_state.user] = gruppe
            st.success(f"Du bist in der Gruppe: {gruppe}")
        else:
            st.info("Bitte Gruppenname eingeben.")

# === TAB 3: Tippstrategie & Generieren ===
with tabs[2]:
    st.header("🧠 Tippstrategie & Generieren")
    
    einsatz = st.slider("💰 Einsatzbetrag (€)", min_value=10, max_value=250, step=10)
    anzahl_tipps = einsatz // 10
    st.markdown(f"🧮 Anzahl Tipps: **{anzahl_tipps}** (1 Tipp = 10 €)")

    if st.button("🎯 Intelligente Tipps generieren"):
        df = pd.read_csv("data/EuroMillion_Ziehungen.csv")
        df.rename(columns=lambda x: x.strip(), inplace=True)
        df['Ziehungsdatum'] = pd.to_datetime(df['Ziehungsdatum'], errors='coerce')
        df = df.dropna(subset=['Ziehungsdatum'])
        df = df.sort_values(by='Ziehungsdatum', ascending=True)

        main_numbers = df.iloc[:, 1:6].values.tolist()
        star_numbers = df.iloc[:, 6:8].values.tolist()

        all_numbers_flat = [num for sublist in main_numbers for num in sublist]
        number_counts = Counter(all_numbers_flat)
        hot_numbers = [num for num, count in number_counts.most_common(20)]
        cold_numbers = [num for num, count in number_counts.most_common()[-20:]]

        def get_cyclic_numbers(df, window=20):
            repeating_numbers = []
            for i in range(len(df) - window):
                past = set(np.array(df.iloc[i:i+window, 1:6]).flatten())
                future = set(np.array(df.iloc[i+window:i+window+5, 1:6]).flatten())
                repeating_numbers.extend(past.intersection(future))
            return list(set(repeating_numbers))

        repeating_numbers = get_cyclic_numbers(df)

        def cluster_stars(stars):
            star_counts = Counter([num for sublist in stars for num in sublist])
            return [num for num, count in star_counts.most_common(8)]

        star_clusters = cluster_stars(star_numbers)

        def monte_carlo_simulation(pool, k, iterations=5000):
            if len(pool) < k:
                pool += list(set(range(1, 51)) - set(pool))
                pool = pool[:k]
            results = Counter()
            for _ in range(iterations):
                draw = tuple(sorted(random.sample(pool, k)))
                results[draw] += 1
            return max(results, key=results.get)

        tipps = []
        for _ in range(anzahl_tipps):
            pool = list(set(hot_numbers + repeating_numbers))
            haupt = monte_carlo_simulation(pool, 5)
            sterne = monte_carlo_simulation(star_clusters + list(range(1, 13)), 2)
            tipps.append((haupt, sterne))

        st.session_state.tipps = tipps
        df_out = pd.DataFrame([{
            "Tipp": i+1,
            "Hauptzahlen": ", ".join(map(str, t[0])),
            "Sternzahlen": ", ".join(map(str, t[1]))
        } for i, t in enumerate(tipps)])
        st.session_state.df_out = df_out
        st.success(f"{anzahl_tipps} Tipps wurden generiert!")

        st.dataframe(df_out)
        csv = df_out.to_csv(index=False).encode('utf-8')
        st.download_button("📥 CSV herunterladen", data=csv, file_name="Intelligente_Tipps.csv")
    

# === TAB 4: Auswertung ===
with tabs[3]:
    st.header("📈 Ziehungs-Auswertung")
    latest_main = st.text_input("Letzte 5 Hauptzahlen (z. B. 10,21,30,42,45):")
    latest_star = st.text_input("Letzte 2 Sternzahlen (z. B. 1,9):")

    tipps_quelle = []
    if "tipps" in st.session_state:
        tipps_quelle = st.session_state.tipps
    elif "df_out" in st.session_state:
        try:
            tipps_quelle = [(list(map(int, row["Hauptzahlen"].split(","))),
                             list(map(int, row["Sternzahlen"].split(","))))
                            for _, row in st.session_state.df_out.iterrows()]
        except:
            tipps_quelle = []
    elif "team_tipps" in st.session_state and st.session_state.groups.get(st.session_state.user) in st.session_state.team_tipps:
        gruppe = st.session_state.groups[st.session_state.user]
        tipps_quelle = st.session_state.team_tipps[gruppe][-1]["tipps"]

    if not tipps_quelle:
        st.info("⚠️ Noch keine Tipps vorhanden.")
    else:
        if st.button("📊 Tipps auswerten"):
            try:
                main_numbers = list(map(int, latest_main.strip().split(",")))
                star_numbers = list(map(int, latest_star.strip().split(",")))

                if len(main_numbers) != 5 or len(star_numbers) != 2:
                    st.warning("Bitte genau 5 Hauptzahlen und 2 Sternzahlen eingeben.")
                else:
                    statistik = {}
                    for haupt, sterne in tipps_quelle:
                        h = len(set(haupt).intersection(main_numbers))
                        s = len(set(sterne).intersection(star_numbers))
                        key = f"{h}R + {s}S"
                        statistik[key] = statistik.get(key, 0) + 1

                    st.subheader("📊 Ergebnis:")
                    df_stats = pd.DataFrame(statistik.items(), columns=["Treffer", "Anzahl"])
                    st.dataframe(df_stats)
            except:
                st.error("Fehlerhafte Eingabe.")

# === TAB 5: Einstellungen ===
with tabs[4]:
    st.header("⚙️ Einstellungen & Zurücksetzen")
    if st.button("🔁 App zurücksetzen"):
        st.session_state.clear()
        st.experimental_rerun()
