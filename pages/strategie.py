
import streamlit as st
import random
import pandas as pd
from collections import Counter

st.set_page_config(page_title="Strategie & Analyse", layout="wide")
st.title("🧠 Strategie & Musteranalyse")

# Beispiel-Ziehungen (Platzhalter)
ziehungsliste = [
    [1, 3, 12, 24, 45],
    [4, 8, 19, 28, 33],
    [3, 12, 25, 30, 45],
    [7, 14, 18, 21, 44],
    [3, 9, 12, 29, 35],
    [1, 3, 24, 36, 45]
]

alle_zahlen = [z for ziehung in ziehungsliste for z in ziehung]
counter = Counter(alle_zahlen)
hot = [num for num, _ in counter.most_common(5)]
cold = [num for num, _ in counter.most_common()[-5:]]

st.markdown("🔥 **Hot-Zahlen**: " + ", ".join(map(str, hot)))
st.markdown("❄️ **Cold-Zahlen**: " + ", ".join(map(str, cold)))

# Wiederkehrende Zahlen
wiederkehrer = []
for i in range(len(ziehungsliste) - 3):
    a = set(ziehungsliste[i])
    b = set(ziehungsliste[i+3])
    wiederkehrer.extend(a.intersection(b))
rad = list(set(wiederkehrer))
if rad:
    st.markdown("♻️ **Wiederkehrende Zahlen**: " + ", ".join(map(str, rad)))
else:
    st.info("Keine Wiederholungen erkannt.")

# Dummy-KI (LSTM-Ersatz)
ki_tipp = sorted(random.sample(range(1, 51), 5))
st.markdown("🧠 **LSTM-KI-Tipp (Demo)**: " + ", ".join(map(str, ki_tipp)))
