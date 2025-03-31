
import streamlit as st
import random
import pandas as pd

def zeige_spielmodus(preis_pro_tipp, waehrung):
    st.header("🎮 Spielmodus")
    modus = st.radio("Wähle deinen Modus:", ["🎮 Einzelspieler", "👥 Gemeinschaftsspiel"])

    if modus == "🎮 Einzelspieler":
        einsatz = st.slider("💰 Einsatzbetrag (1–50)", 1, 50, 10)
    else:
        einsatz = st.slider("💰 Gemeinschafts-Einsatz (50–500)", 50, 500, 50)

    anzahl_tipps = int(einsatz // preis_pro_tipp)
    kosten = anzahl_tipps * preis_pro_tipp

    st.markdown(f"📄 **Anzahl Tipps**: {anzahl_tipps}")
    st.markdown(f"💰 **Gesamtkosten**: {waehrung} {kosten:.2f}")

    if st.button("🎯 Tipps generieren", key=f"btn_tipps_{modus}"):
        tipps = []
        for _ in range(anzahl_tipps):
            haupt = sorted(random.sample(range(1, 51), 5))
            sterne = sorted(random.sample(range(1, 13), 2))
            tipps.append((haupt, sterne))
        df = pd.DataFrame([{
            "Tipp": i+1,
            "Hauptzahlen": ", ".join(map(str, h)),
            "Sternzahlen": ", ".join(map(str, s))
        } for i, (h, s) in enumerate(tipps)])
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 CSV herunterladen", data=csv, file_name="Tipps.csv", key=f"dl_{modus}")
