
import streamlit as st
from datetime import datetime
from collections import Counter
import random

from euromillions_live_api_module import anzeigen_ziehung

st.set_page_config(page_title="EuroMillions Live Analyse", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "start"

st.title("💫 EuroMillions Live-Auswertung")

if st.session_state.page == "start":
    st.image("https://cdn-icons-png.flaticon.com/512/869/869636.png", width=100)
    st.markdown("Willkommen zur Live-Vorhersage & Analyse.")
    if st.button("📡 Zeige aktuelle Ziehung"):
        st.session_state.page = "ziehung"

elif st.session_state.page == "ziehung":
    daten = anzeigen_ziehung()
    if st.button("➡️ Weiter zur Tippprüfung"):
        st.session_state.ziehung = daten
        st.session_state.page = "tippvergleich"

elif st.session_state.page == "tippvergleich":
    st.subheader("🎯 Deine Tipps eingeben (z. B. 5 Zahlen + 2 Sterne)")
    tipps_input = st.text_input("📥 Zahlen (z. B. 5, 12, 21, 30, 45)")
    sterne_input = st.text_input("🌟 Sterne (z. B. 1, 9)")

    if tipps_input and sterne_input and "ziehung" in st.session_state:
        gez = set(int(x.strip()) for x in tipps_input.split(",") if x.strip().isdigit())
        gez_s = set(int(x.strip()) for x in sterne_input.split(",") if x.strip().isdigit())

        daten = st.session_state.ziehung
        gezogen = set(daten["hauptzahlen"])
        sterne = set(daten["sternzahlen"])

        haupt = len(gezogen.intersection(gez))
        sternt = len(sterne.intersection(gez_s))

        gewinn = daten["ränge"].get((haupt, sternt), "Kein Gewinn")

        st.markdown(f"🔍 **Treffer:** {haupt} Zahlen + {sternt} Sterne")
        st.markdown(f"💰 **Ergebnis:** {gewinn}")
