st.set_page_config(page_title="EuroMillions Analyse-App", layout="centered")

import streamlit as st
import pandas as pd
import numpy as np
import random
import os
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense

# === Mobile Style ===
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

# Rest des Codes...


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

st.set_page_config(page_title="EuroMillions Analyse-App", layout="centered")
st.title("🔮 EuroMillions: Einzelspiel & Gemeinschaftsspiel mit CSV-Analyse")

modus = st.radio("Modus wählen:", ["🎮 Einzelspieler", "👥 Gemeinschaftsspiel"])

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
