
import streamlit as st
import pandas as pd
import random

st.title("🎯 EuroGenius Tipp-Generator & CSV-Analyse")

# === Spielmodus und Tippanzahl ===
modus = st.radio("🧑‍🤝‍🧑 Spielmodus", ["Einzelspieler", "Gemeinschaftsspiel"])
max_tipps = 50 if modus == "Einzelspieler" else 500
anzahl_tipps = st.slider("🎟️ Anzahl Tipps", 1, max_tipps, 5)

# === CSV Upload ===
st.markdown("## 📁 Ziehungsdaten hochladen")
uploaded_file = st.file_uploader("Lade eine CSV-Datei mit Ziehungsdaten hoch", type=["csv"])
ziehungen_df = None
if uploaded_file:
    ziehungen_df = pd.read_csv(uploaded_file)
    st.success("Datei erfolgreich geladen!")
    st.dataframe(ziehungen_df.head())
    if len(ziehungen_df) >= 2000:
        letzte_2000 = ziehungen_df.tail(2000)
        st.markdown("### 🔢 Letzte 2000 Ziehungen")
        st.dataframe(letzte_2000)
    else:
        st.warning("Die Datei enthält weniger als 2000 Ziehungen. Bitte vollständige CSV verwenden.")


# === Tipp-Generierung ===
st.markdown("## 🔁 Tipps generieren")
if st.button("🎯 Generiere Tipps"):
    tipps = []
    for _ in range(anzahl_tipps):
        hauptzahlen = sorted(random.sample(range(1, 51), 5))
        sterne = sorted(random.sample(range(1, 13), 2))
        tipps.append({
            "Hauptzahlen": " - ".join(map(str, hauptzahlen)),
            "Sternzahlen": " - ".join(map(str, sterne))
        })
    df_tipps = pd.DataFrame(tipps)
    st.dataframe(df_tipps)
