
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

st.title("📊 Zahlenanalyse deiner CSV-Daten")

uploaded_file = st.file_uploader("Lade eine CSV-Datei hoch", type="csv", key="analyse_csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    zahlen = df.iloc[:, 1:6].values.flatten()
    counter = Counter(zahlen)

    st.markdown("## 🔥 Häufigste Zahlen (Hot)")
    hot = counter.most_common(10)
    hot_df = pd.DataFrame(hot, columns=["Zahl", "Häufigkeit"])
    st.bar_chart(hot_df.set_index("Zahl"))

    st.markdown("## 🧊 Seltenste Zahlen (Cold)")
    cold = counter.most_common()[-10:]
    cold_df = pd.DataFrame(cold, columns=["Zahl", "Häufigkeit"])
    st.bar_chart(cold_df.set_index("Zahl"))

    st.markdown("## ♻️ Rad-Zahlen (Wiederkehrend)")
    rad_zahlen = set()
    for i in range(len(df) - 20):
        vergangen = set(df.iloc[i:i+20, 1:6].values.flatten())
        zukunft = set(df.iloc[i+20:i+25, 1:6].values.flatten())
        rad_zahlen.update(vergangen.intersection(zukunft))
    st.write(sorted(rad_zahlen))

    st.markdown("## 🧩 Cluster nach Zahlenbereichen")
    cluster = {"0–9": [], "10–19": [], "20–29": [], "30–39": [], "40–50": []}
    for zahl in zahlen:
        if 0 <= zahl <= 9:
            cluster["0–9"].append(zahl)
        elif 10 <= zahl <= 19:
            cluster["10–19"].append(zahl)
        elif 20 <= zahl <= 29:
            cluster["20–29"].append(zahl)
        elif 30 <= zahl <= 39:
            cluster["30–39"].append(zahl)
        else:
            cluster["40–50"].append(zahl)
    for k, v in cluster.items():
        st.write(f"{k}: {len(v)} Zahlen")

    st.markdown("## 🎲 Monte Carlo Struktur (Demo)")
    st.info("Hier wird später eine Simulation eingebaut, um Wahrscheinlichkeiten zu analysieren.")
