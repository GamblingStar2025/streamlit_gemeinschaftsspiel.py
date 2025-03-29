import streamlit as st
import pandas as pd
import random
import os
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense

# === Daten einlesen ===
data_path = "data/EuroMillion_Ziehungen.csv"
if not os.path.exists(data_path):
    st.error("CSV-Datei mit Ziehungen nicht gefunden. Bitte stelle sicher, dass sie im Verzeichnis 'data/' liegt.")
    st.stop()

df = pd.read_csv(data_path)
df.rename(columns=lambda x: x.strip(), inplace=True)
df['Ziehungsdatum'] = pd.to_datetime(df['Ziehungsdatum'], errors='coerce')
df = df.dropna(subset=['Ziehungsdatum'])
df = df.sort_values(by='Ziehungsdatum', ascending=True)

main_numbers = df.iloc[:, 1:6].values.tolist()
star_numbers = df.iloc[:, 6:8].values.tolist()

# === Statistik und KI-Logik ===
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
    return pd.np.array(X).reshape((-1, 5, 1)), pd.np.array(y)

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

# === Vorhersagefunktion ===
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

# === Streamlit UI ===
st.set_page_config(page_title="Euromillions Vorhersage (CSV)", layout="centered")
st.title("🔮 Euromillions Einzelspiel mit CSV-Analyse")

anzahl = st.slider("Wie viele Tipps möchtest du generieren?", 1, 20, 5)
if st.button("Tipps generieren"):
    tipps = echte_vorhersagen(anzahl)
    df_out = pd.DataFrame([{
        "Tipp": i+1,
        "Hauptzahlen": ", ".join(map(str, t[0])),
        "Sternzahlen": ", ".join(map(str, t[1]))
    } for i, t in enumerate(tipps)])
    st.dataframe(df_out)
    csv = df_out.to_csv(index=False).encode('utf-8')
    st.download_button("📥 CSV herunterladen", data=csv, file_name="Euromillions_Tipps.csv")
