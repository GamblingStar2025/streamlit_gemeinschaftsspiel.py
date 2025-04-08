
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

st.title("📊 Analyse der Ziehungsdaten")
uploaded_file = st.file_uploader("Lade eine CSV-Datei mit Euromillion-Ziehungen hoch", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Datei erfolgreich geladen!")
    st.dataframe(df.head())

    # Hauptzahlen extrahieren (Spalten 1-5)
    hauptzahlen = df.iloc[:, 1:6].values.flatten()
    counts = Counter(hauptzahlen)
    häufigste = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:20])

    st.subheader("🔢 Häufigste Hauptzahlen (Top 20)")
    st.bar_chart(pd.Series(häufigste).sort_index())

    # Cluster (z. B. 1–10, 11–20 ...)
    st.subheader("🔗 Verteilung nach Zahlenbereichen (Cluster)")
    cluster_labels = ["1–10", "11–20", "21–30", "31–40", "41–50"]
    cluster_counts = [0]*5
    for num in hauptzahlen:
        if 1 <= num <= 10:
            cluster_counts[0] += 1
        elif 11 <= num <= 20:
            cluster_counts[1] += 1
        elif 21 <= num <= 30:
            cluster_counts[2] += 1
        elif 31 <= num <= 40:
            cluster_counts[3] += 1
        elif 41 <= num <= 50:
            cluster_counts[4] += 1
    cluster_df = pd.DataFrame({"Cluster": cluster_labels, "Anzahl": cluster_counts}).set_index("Cluster")
    st.bar_chart(cluster_df)
