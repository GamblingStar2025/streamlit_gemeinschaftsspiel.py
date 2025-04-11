
import streamlit as st
from datetime import datetime

# Simulierte Ziehungsdaten (hier normalerweise API oder Live-Webscraping)
aktuelle_ziehung = {
    "datum": "2025-04-09",
    "zahlen": [5, 23, 28, 44, 48],
    "sterne": [2, 8],
    "jackpot": "CHF 52.5 Mio"
}

st.set_page_config(page_title="EuroMillions Dashboard", layout="centered")

st.markdown("## 📊 Aktuelle EuroMillions Ziehung")
st.markdown(f"**Datum:** {aktuelle_ziehung['datum']}")
st.success(f"**Zahlen:** {', '.join(map(str, aktuelle_ziehung['zahlen']))} ⭐ {', '.join(map(str, aktuelle_ziehung['sterne']))}")
st.markdown(f"🤑 **Nächster Jackpot:** {aktuelle_ziehung['jackpot']}")

# Info: Bald automatisch über API/Webscraper ersetzt
st.info("Diese Daten werden bald automatisch von einer offiziellen Quelle geladen.")
