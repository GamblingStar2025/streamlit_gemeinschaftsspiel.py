
import streamlit as st
import pandas as pd

st.title("🏁 Auswertung deiner Tipps")

ziehungen = st.file_uploader("Lade die offiziellen Gewinnzahlen (CSV)", type="csv", key="auswertung_ziehungen")
tipps = st.file_uploader("Lade deine gespeicherten Tipps (CSV)", type="csv", key="auswertung_tipps")

if ziehungen and tipps:
    ziehung_df = pd.read_csv(ziehungen)
    tipps_df = pd.read_csv(tipps)

    st.success("✅ Daten geladen. Auswertung beginnt …")

    def gewinnklasse(haupt, sterne):
        mapping = {
            (5, 2): "🥇 Jackpot (5+2)",
            (5, 1): "🥈 5+1",
            (5, 0): "🥉 5+0",
            (4, 2): "4+2",
            (4, 1): "4+1",
            (3, 2): "3+2",
            (4, 0): "4+0",
            (2, 2): "2+2",
            (3, 1): "3+1",
            (3, 0): "3+0",
            (1, 2): "1+2",
            (2, 1): "2+1",
            (2, 0): "2+0"
        }
        return mapping.get((haupt, sterne), "❌ Kein Gewinn")

    zieh_haupt = set(ziehung_df.iloc[0, 1:6])
    zieh_sterne = set(ziehung_df.iloc[0, 6:8])

    auswertungen = []
    for _, row in tipps_df.iterrows():
        tipp_haupt = set(map(int, row["Hauptzahlen"].split(",")))
        tipp_sterne = set(map(int, row["Sternzahlen"].split(",")))
        haupt_treffer = len(tipp_haupt & zieh_haupt)
        stern_treffer = len(tipp_sterne & zieh_sterne)
        rang = gewinnklasse(haupt_treffer, stern_treffer)
        auswertungen.append({
            "Tipp": row["Hauptzahlen"] + " + " + row["Sternzahlen"],
            "Treffer": f"{haupt_treffer}+{stern_treffer}",
            "Rang": rang
        })

    result_df = pd.DataFrame(auswertungen)
    st.dataframe(result_df)
