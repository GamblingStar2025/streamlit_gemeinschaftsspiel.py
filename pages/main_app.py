
import streamlit as st
import pandas as pd
import random

st.title("🎯 EuroGenius Tipp-Generator & CSV-Analyse")

# === Spielmodus und Tippanzahl ===
modus = st.radio("🧑‍🤝‍🧑 Spielmodus", ["Einzelspieler", "Gemeinschaftsspiel"])
max_tipps = 50 if modus == "Einzelspieler" else 500
anzahl_tipps = st.slider("🎟️ Anzahl Tipps", 1, max_tipps, 5)

# === CSV Upload ===
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



import pandas as pd

st.markdown("## 📂 CSV-Datei hochladen")
uploaded_file = st.file_uploader("Lade deine EuroMillion-Ziehungsdatei hoch (CSV)", type="csv")

if uploaded_file is not None:
    try:
        ziehungen_df = pd.read_csv(uploaded_file)
        ziehungen_df.dropna(inplace=True)
        if len(ziehungen_df) >= 2000:
            st.success("✅ Datei erfolgreich geladen. Die letzten 2000 Ziehungen werden angezeigt.")
            st.dataframe(ziehungen_df.tail(2000))
        else:
            st.warning("⚠️ Die Datei enthält weniger als 2000 Ziehungen.")
    except Exception as e:
        st.error(f"Fehler beim Einlesen der Datei: {e}")
