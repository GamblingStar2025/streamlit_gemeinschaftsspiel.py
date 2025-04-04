
import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter
import random
import time

st.markdown(
    "<h1 style='text-align: center; color: gold;'>🎯 EuroGenius – Dein KI-Tippassistent</h1>",
    unsafe_allow_html=True
)
st.markdown("<style>body { background-color: #0b0e11; color: white; }</style>", unsafe_allow_html=True)

st.sidebar.header("🎛 Einstellungen")
anzahl_tipps = st.sidebar.slider("Wie viele Tipps möchtest du generieren?", 1, 50, 5)
ki_gewichtung = st.sidebar.slider("🔬 KI-Gewichtung (%)", 0, 200, 100)
sim_stufen = st.sidebar.slider("🎲 Simulationen (Monte Carlo)", 100, 1000000, 10000, step=100)

st.markdown("## 📥 CSV-Daten hochladen")
csv_file = st.file_uploader("Lade die Datei 'EuroMillion_Ziehungen.csv' hoch", type=["csv"])

if csv_file:
    try:
        df = pd.read_csv(csv_file)
        df = df.dropna(how='all')
        df = df.sort_values(by=df.columns[0])
        st.success("CSV erfolgreich verarbeitet.")

        df_recent = df.tail(2000)
        main_cols = df_recent.columns[1:6]
        zahlen = df_recent[main_cols].values.flatten()
        counts = Counter(zahlen)
        hot = [int(n) for n, _ in counts.most_common(10)]
        cold = [int(n) for n, _ in counts.most_common()[-10:]]

        st.markdown("### 🔥 Hot & ❄️ Cold")
        st.write(f"Hot: {sorted(hot)}")
        st.write(f"Cold: {sorted(cold)}")

        def get_repeating(df, window=20):
            repeats = set()
            for i in range(len(df) - window):
                past = set(df.iloc[i:i+window, 1:6].values.flatten())
                future = set(df.iloc[i+window:i+window+5, 1:6].values.flatten())
                repeats.update(past.intersection(future))
            return sorted(list(repeats))

        repeating = get_repeating(df_recent)
        st.markdown(f"♻️ Wiederkehrende Zahlen: {repeating}")

        if st.button("🚀 Tipps generieren"):
            with st.spinner("🔄 KI analysiert Wahrscheinlichkeiten..."):
                time.sleep(1)
                alle_tipps = []
                for _ in range(anzahl_tipps):
                    top_pool = hot + repeating
                    pool = list(set(top_pool))
                    while len(pool) < 5:
                        pool.append(random.randint(1, 50))
                    tipp = sorted(random.sample(pool, 5))
                    sterne = sorted(random.sample(range(1, 13), 2))
                    alle_tipps.append((tipp, sterne))
                st.success("🎉 Deine Tipps sind bereit – viel Glück!")
                for i, (zahlen, sterne) in enumerate(alle_tipps, 1):
                    st.markdown(f"**Tipp {i}:** {zahlen} ⭐ {sterne}")
    except Exception as e:
        st.error(f"Fehler beim Verarbeiten: {e}")
