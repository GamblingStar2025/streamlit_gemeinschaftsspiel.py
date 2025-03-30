import numpy as np
import streamlit as st
import pandas as pd
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

# === Statistik + LSTM-Vorbereitung ===
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
    model.fit(X, y, epochs=20, verbose=0)
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

# === Gemeinschaftsspiel-Strategie ===
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
    base_tips = 14
    multiplier = 8
    stufen = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

    if einsatz not in stufen:
        raise ValueError("Einsatz muss 50, 100, 150, 200 oder 250 sein.")

    tipps = base_tips + ((einsatz - 50) // 50) * multiplier
    return tipps

# === Streamlit UI ===
st.set_page_config(page_title="EuroMillions Analyse-App", layout="centered")
st.title("🔮 EuroMillions: Einzelspiel & Gemeinschaftsspiel mit CSV-Analyse")

modus = st.radio("Modus wählen:", ["🎮 Einzelspieler", "👥 Gemeinschaftsspiel"])

if modus == "🎮 Einzelspieler":
    einsatz = st.slider("💰 Einsatzbetrag wählen (Einzelspiel):", 1, 50, 10, step=1)
    strategie = strategie_einzelspieler(einsatz)
        "einsatz": einsatz,
        strategie = strategie_einzelspieler(einsatz)
    anzahl = strategie["tipps"]
        "ki_gewichtung": 50 + ((einsatz - 50) // 50) * 10,
        "simulationen": 100000 + ((einsatz - 50) // 50) * 50000,
        "stufe": f"Level {(einsatz - 50) // 50 + 1}/5"
    }
    st.subheader(f"🧮 Strategie für {strategie['einsatz']}€ Beitrag (Einzelspieler)")
    st.metric("🎟️ Tipps insgesamt", f"{strategie['tipps']}")
    st.metric("🧠 KI-Gewichtung", f"{strategie['ki_gewichtung']}%")
    st.metric("🎲 Simulationen", f"{strategie['simulationen']:,}")
    st.metric("🔢 Stufe", strategie['stufe'])
    st.header("🔹 Einzelspiel-Vorhersage")
    anzahl = strategie["tipps"]
    if st.button("Tipps generieren"):
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
    st.header("🔹 Gemeinschaftsspiel-Strategie")
    einsatz = st.selectbox("💰 Einsatzbetrag wählen:", [50, 100, 150, 200, 250, 300, 350, 400, 450, 500])
    if st.button("Tipps generieren"):
        strategie = strategie_gemeinschaft(einsatz)
        anzahl = strategie["tipps"]
        strategie = strategie_einzelspieler(einsatz)
            "einsatz": einsatz,
            "tipps": anzahl,
            "ki_gewichtung": 50 + ((einsatz - 50) // 50) * 10,
            "simulationen": 100000 + ((einsatz - 50) // 50) * 50000,
            "stufe": f"Level {(einsatz - 50) // 50 + 1}/5"
        }
        st.subheader(f"🧮 Strategie für {strategie['einsatz']}€ Beitrag")
        st.metric("🎟️ Tipps insgesamt", f"{strategie['tipps']}")
        st.metric("🧠 KI-Gewichtung", f"{strategie['ki_gewichtung']}%")
        st.metric("🎲 Simulationen", f"{strategie['simulationen']:,}")
        st.metric("🔢 Stufe", strategie['stufe'])
        tipps = echte_vorhersagen(anzahl)
        df_out = pd.DataFrame([{
            "Tipp": i+1,
            "Hauptzahlen": ", ".join(map(str, t[0])),
            "Sternzahlen": ", ".join(map(str, t[1]))
        } for i, t in enumerate(tipps)])
        st.dataframe(df_out)
        csv = df_out.to_csv(index=False).encode('utf-8')
        st.download_button("📥 CSV herunterladen", data=csv, file_name="Gemeinschaftstipps.csv")
