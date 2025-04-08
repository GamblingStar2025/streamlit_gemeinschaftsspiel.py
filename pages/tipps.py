
import streamlit as st
import pandas as pd
import random
from collections import Counter

st.title("🎯 Tipp-Erstellung")

uploaded_file = st.file_uploader("Lade deine Ziehungs-CSV hoch", type="csv", key="tipps_csv")
anzahl_tipps = st.slider("Anzahl Tipps", 1, 50, 5)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    zahlen = df.iloc[:, 1:6].values.flatten()
    counter = Counter(zahlen)
    hot = [num for num, _ in counter.most_common(20)]
    all_zahlen = list(range(1, 51))
    all_stars = list(range(1, 13))

    st.subheader("🧠 Generierte Tipps")
    for i in range(anzahl_tipps):
        haupt = sorted(random.sample(hot, 3) + random.sample(all_zahlen, 2))
        sterne = sorted(random.sample(all_stars, 2))
        st.write(f"Tipp {i+1}: **{haupt}** + Sterne: **{sterne}**")
