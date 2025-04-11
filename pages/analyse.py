
import streamlit as st
import pandas as pd

st.title("📂 Ziehungsdaten hochladen")

csv = st.file_uploader("Lade deine EuroMillions CSV-Datei hoch", type="csv")
if csv:
    df = pd.read_csv(csv)
    df = df.tail(2000)
    st.session_state["ziehungen"] = df
    st.success("✅ Datei gespeichert für spätere Nutzung.")
    st.dataframe(df)
