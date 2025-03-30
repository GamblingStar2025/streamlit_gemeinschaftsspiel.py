import streamlit as st
st.set_page_config(page_title="EuroMillions Analyse-App", layout="centered")

import pandas as pd
import numpy as np
import random
import os
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense

# === CSV einlesen ===
data_path = "data/EuroMillion_Ziehungen.csv"
if not os.path.exists(data_path):
    st.error("CSV-Datei fehlt! Lege sie unter 'data/EuroMillion_Ziehungen.csv' ab.")
    st.stop()

df = pd.read_csv(data_path)
df.rename(columns=lambda x: x.strip(), inplace=True)
df['Ziehungsdatum'] = pd.to_datetime(df['Ziehungsdatum'], errors='coerce')
df = df.dropna(subset=['Ziehungsdatum'])
df = df.sort_values(by='Ziehungsdatum', ascending=True)

main_numbers = df.iloc[:, 1:6].values.tolist()
star_numbers = df.iloc[:, 6:8].values.tolist()

# === Statistik + LSTM ===
all_numbers_flat = [num for draw in main_numbers for num in draw]
number_counts = Counter(all_numbers_flat)
hot_numbers = [num for num, count in number_counts.most_common(20)]

def get_cyclic_numbers(df, window=20):
    repeating_numbers = []
    for i in range(len(df) - window):
        past = set(df.iloc[i:i+window, 1:6].values.flatten())
        future = set(df.iloc[i+window:i+window+5, 1:6].values.flatten())
        repeating_numbers.extend(past.intersection(future))
    return list(set(repeating_numbers))

repeating_numbers = get_cyclic_numbers(df)

def prepare_lstm_data(main_numbers):
    sequences = [sorted(draw) for draw in main_numbers if len(set(draw)) == 5]
    scaler = MinMaxScaler()
    X, y = [], []
    for i in range(len(sequences) - 1):
        seq = scaler.fit_transform(pd.DataFrame(sequences[i])).flatten()
        target = sequences[i + 1]
        X.append(seq)
        y.append(target)
    return np.array(X).reshape((-1, 5, 1)), np.array(y)

def train_lstm_model(X, y):
    model = Sequential([
        Input(shape=(5, 1)),
        LSTM(50, activation='relu'),
        Dense(50, activation='relu'),
        Dense(5)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=10, verbose=0)
    return model

def echte_vorhersagen(anzahl):
    tipps = []
    top_pool = list(set(hot_numbers + repeating_numbers))
    X_lstm, y_lstm = prepare_lstm_data(main_numbers)
    model = train_lstm_model(X_lstm, y_lstm)
    pred = model.predict(X_lstm[-1].reshape(1, 5, 1))[0]
    lstm_numbers = [int(round(n)) for n in pred if 1 <= round(n) <= 50][:5]

    for _ in range(anzahl):
        haupt = sorted(random.sample(list(set(top_pool + lstm_numbers)), 5))
        sterne = sorted(random.sample(range(1, 13), 2))
        tipps.append((haupt, sterne))
    return tipps

# === Strategien ===
def strategie_einzelspieler(einsatz):
    if einsatz < 1 or einsatz > 50:
        raise ValueError("Einzelspieler-Einsatz muss zwischen 1 und 50€ liegen.")
    tipps = 1 + einsatz // 2
    return {
        "einsatz": einsatz,
        "tipps": tipps,
        "ki_gewichtung": 50 + einsatz,
        "simulationen": 50000 + einsatz * 1500,
        "stufe": f"Level {min(5, einsatz // 10 + 1)}/5"
    }

def strategie_gemeinschaft(einsatz):
    if einsatz not in [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]:
        raise ValueError("Einsatz muss 50, 100, ..., 500 sein.")
    tipps = 14 + ((einsatz - 50) // 50) * 8
    return {
        "einsatz": einsatz,
        "tipps": tipps,
        "ki_gewichtung": 50 + ((einsatz - 50) // 50) * 10,
        "simulationen": 100000 + ((einsatz - 50) // 50) * 50000,
        "stufe": f"Level {(einsatz - 50) // 50 + 1}/10"
    }

# === Streamlit UI ===
if "user" not in st.session_state:
    st.session_state.user = None
if "groups" not in st.session_state:
    st.session_state.groups = {}
if "TEAM_SESSIONS" not in st.session_state:
    st.session_state.TEAM_SESSIONS = {}
if "team_tipps" not in st.session_state:
    st.session_state.team_tipps = {}
if "groups" not in st.session_state:
    st.session_state.groups = {}

    st.session_state.TEAM_SESSIONS = {}
if "team_tipps" not in st.session_state:
    st.session_state.team_tipps = {}
    st.session_state.TEAM_SESSIONS = {}

# === LOGIN-BEREICH ===
st.title("🎟️ EuroMillions Login")
if st.session_state.user is None:
    username = st.text_input("👤 Benutzername eingeben")
    if st.button("✅ Anmelden"):
        if username.strip():
            st.session_state.user = username.strip()
            st.success(f"Willkommen, {st.session_state.user}!")
        else:
            st.warning("Bitte einen gültigen Namen eingeben.")
    st.stop()
else:
    st.markdown(f"👋 Eingeloggt als **{st.session_state.user}**")

# Gruppenauswahl oder -erstellung
gruppe = st.text_input("🧩 Gruppe erstellen oder beitreten")
if gruppe:
    gruppe = gruppe.strip()
    st.session_state.groups[st.session_state.user] = gruppe
    st.success(f"🫂 Du bist jetzt in der Gruppe **{gruppe}**")
    members = [user for user, grp in st.session_state.groups.items() if grp == gruppe]
    st.info(f"👥 Mitglieder in '{gruppe}': {', '.join(members)}")
else:
    st.warning("Bitte gib eine Gruppenzugehörigkeit ein.")
    st.stop()


if "TEAM_SESSIONS" not in st.session_state:
    st.session_state.TEAM_SESSIONS = {}
if "team_tipps" not in st.session_state:
    st.session_state.team_tipps = {}
if "groups" not in st.session_state:
    st.session_state.groups = {}

    st.session_state.TEAM_SESSIONS = {}
if "team_tipps" not in st.session_state:
    st.session_state.team_tipps = {}
    st.session_state.TEAM_SESSIONS = {}
import uuid

st.markdown(
    """
    <style>
    .stButton>button {
        font-size: 18px;
        padding: 0.75em 1.5em;
        border-radius: 10px;
    }
    .stDownloadButton>button {
        font-size: 16px;
        padding: 0.6em 1.2em;
        border-radius: 8px;
    }
    .stSelectbox, .stSlider, .stRadio {
        font-size: 17px !important;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    .stMetric {
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔮 EuroMillions: Einzelspiel & Gemeinschaftsspiel mit CSV-Analyse")

modus = st.radio("Modus wählen:", ["🎮 Einzelspieler", "👥 Gemeinschaftsspiel", "🤝 Team-Modus"])
if st.button("🔙 Zurück zur Modusauswahl"):
    st.session_state.user = None
    st.rerun()

if modus == "🎮 Einzelspieler":
    einsatz = st.slider("💰 Einsatzbetrag wählen (Einzelspiel):", 1, 50, 10, step=1)
    strategie = strategie_einzelspieler(einsatz)
    anzahl = strategie["tipps"]

    st.subheader(f"🧮 Strategie für {strategie['einsatz']}€ Beitrag (Einzelspieler)")
    st.metric("🎟️ Tipps insgesamt", f"{strategie['tipps']}")
    st.metric("🧠 KI-Gewichtung", f"{strategie['ki_gewichtung']}%")
    st.metric("🎲 Simulationen", f"{strategie['simulationen']:,}")
    st.metric("🔢 Stufe", strategie['stufe'])

    if st.button("🎯 Tipps generieren"):
        tipps = echte_vorhersagen(anzahl)
        df_out = pd.DataFrame([{
            "Tipp": i+1,
            "Hauptzahlen": ", ".join(map(str, t[0])),
            "Sternzahlen": ", ".join(map(str, t[1]))
        } for i, t in enumerate(tipps)])
        st.dataframe(df_out)
        csv = df_out.to_csv(index=False).encode('utf-8')
        st.download_button("📥 CSV herunterladen", data=csv, file_name="Einzelspiel_Tipps.csv")

if modus == "👥 Gemeinschaftsspiel":
    einsatz = st.selectbox("💰 Einsatzbetrag wählen (Gemeinschaft):", [50, 100, 150, 200, 250, 300, 350, 400, 450, 500])
    strategie = strategie_gemeinschaft(einsatz)
    anzahl = strategie["tipps"]

    st.subheader(f"🧮 Strategie für {strategie['einsatz']}€ Beitrag (Gemeinschaftsspiel)")
    st.metric("🎟️ Tipps insgesamt", f"{strategie['tipps']}")
    st.metric("🧠 KI-Gewichtung", f"{strategie['ki_gewichtung']}%")
    st.metric("🎲 Simulationen", f"{strategie['simulationen']:,}")
    st.metric("🔢 Stufe", strategie['stufe'])

    if st.button("🤝 Gemeinschafts-Tipps generieren"):
        tipps = echte_vorhersagen(anzahl)
        df_out = pd.DataFrame([{
            "Tipp": i+1,
            "Hauptzahlen": ", ".join(map(str, t[0])),
            "Sternzahlen": ", ".join(map(str, t[1]))
        } for i, t in enumerate(tipps)])
        st.dataframe(df_out)
        csv = df_out.to_csv(index=False).encode('utf-8')
        st.download_button("📥 CSV herunterladen", data=csv, file_name="Gemeinschaft_Tipps.csv")

elif modus == "🤝 Team-Modus":
    st.header("🤝 Team-Spiel mit Code")
    teamcode = st.text_input("🔑 Teamcode eingeben oder generieren")

    if st.button("🔁 Neuen Code erstellen"):
        new_code = str(uuid.uuid4())[:8]
        st.success(f"Dein Teamcode: {new_code}")
        teamcode = new_code

    if not gruppe:
        st.warning("Bitte Gruppe oben eingeben, um den Team-Modus zu nutzen.")
        st.stop()

    if teamcode:
        if teamcode in st.session_state.TEAM_SESSIONS:
            gespeicherte_daten = st.session_state.TEAM_SESSIONS[teamcode]
            tipps = gespeicherte_daten["tipps"]
            st.subheader(f"📜 Letzte Tipps für Team {teamcode}")
            df_out = pd.DataFrame([{
                "Tipp": i+1,
                "Hauptzahlen": ", ".join(map(str, t[0])),
                "Sternzahlen": ", ".join(map(str, t[1]))
            } for i, t in enumerate(tipps)])
            st.dataframe(df_out)
            csv = df_out.to_csv(index=False).encode('utf-8')
            st.download_button("📥 CSV herunterladen", data=csv, file_name=f"Team_{teamcode}_Tipps.csv")

        einsatz = st.selectbox("💰 Einsatzbetrag für dein Team:", [50, 100, 150, 200, 250])
        if st.button("👥 Neue Team-Tipps generieren"):
            strategie = strategie_gemeinschaft(einsatz)
            anzahl = strategie["tipps"]
            st.subheader(f"🧮 Strategie für Team {teamcode}")
            st.metric("🎟️ Tipps insgesamt", f"{strategie['tipps']}")
            st.metric("🧠 KI-Gewichtung", f"{strategie['ki_gewichtung']}%")
            st.metric("🎲 Simulationen", f"{strategie['simulationen']:,}")
            st.metric("🔢 Stufe", strategie['stufe'])

            tipps = echte_vorhersagen(anzahl)
            st.session_state.TEAM_SESSIONS[teamcode] = {
                "strategie": strategie,
                "tipps": tipps
            }

            df_out = pd.DataFrame([{
                "Tipp": i+1,
                "Hauptzahlen": ", ".join(map(str, t[0])),
                "Sternzahlen": ", ".join(map(str, t[1]))
            } for i, t in enumerate(tipps)])
            st.dataframe(df_out)
            csv = df_out.to_csv(index=False).encode('utf-8')
            st.download_button("📥 CSV herunterladen", data=csv, file_name=f"Team_{teamcode}_Tipps.csv")
    else:
        st.info("Bitte einen Teamcode eingeben oder generieren.")


# === Ziehungs-Auswertung ===
st.header("🎯 Ziehungs-Auswertung")
latest_main = st.text_input("Gib die 5 Hauptzahlen der letzten Ziehung ein (z. B. 10,21,30,42,45):")
latest_star = st.text_input("Gib die 2 Sternzahlen der letzten Ziehung ein (z. B. 1,9):")

tipps_quelle = []
if "tipps" in locals():
    tipps_quelle = tipps
elif "df_out" in locals():
    try:
        tipps_quelle = [(list(map(int, row["Hauptzahlen"].split(","))),
                         list(map(int, row["Sternzahlen"].split(","))))
                        for _, row in df_out.iterrows()]
    except:
        tipps_quelle = []
elif "team_tipps" in st.session_state and gruppe in st.session_state.team_tipps:
    tipps_quelle = st.session_state.team_tipps[gruppe][-1]["tipps"]

if not tipps_quelle:
    st.info("⚠️ Es wurden noch keine Tipps generiert oder geladen.")
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

                st.subheader("📈 Auswertungsergebnisse:")
                df_stats = pd.DataFrame(statistik.items(), columns=["Treffer", "Anzahl"])
                st.dataframe(df_stats)
        except:
            st.error("Eingabe ungültig – bitte nur Zahlen und Kommas verwenden.")
