
import streamlit as st
import pandas as pd
from collections import Counter

st.title("📊 Analyse")
st.markdown("Zeigt Hot-Zahlen, Cold-Zahlen und Cluster-Auswertung.")

sample_data = [1, 5, 10, 14, 21, 29, 33, 36, 42, 45, 50]
counts = Counter(sample_data)
df = pd.DataFrame.from_dict(counts, orient='index', columns=['Anzahl'])
st.bar_chart(df)
