
import streamlit as st
from datetime import date
import random
import pandas as pd
from io import StringIO
from tippgenerator_module_fixed import generiere_tipps

# Beispielhafte Ziehungshistorie (Demo)
history = [[random.randint(1, 50) for _ in range(5)] for _ in range(100)]

st.set_page_config(page_title="EuroMillions Tipps", layout="centered")
st.title("🎯 EuroMillions Tipp-Generator mit Analyse")

modus = st.radio("🧑‍🤝‍🧑 Spielmodus wählen", ["👤 Einzelspieler", "👥 Gemeinschaftsspiel"])
land = st.selectbox("🌍 Land wählen", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇫🇷 Frankreich", "🇦🇹 Österreich"])
waehrung = "CHF" if "Schweiz" in land else "€"
tipp_preis = 3.5 if "Schweiz" in land else 2.5

ki_gewichtung = st.slider("🧠 KI-Gewichtung (%)", 0, 200, 100, step=10)
sim_stufen = 1_000_000

if modus == "👤 Einzelspieler":
    anzahl_tipps = st.slider("🎟️ Anzahl Tipps", 0, 50, 5)
else:
    anzahl_tipps = st.slider("🎟️ Anzahl Tipps", 0, 500, 50, step=50)

kosten = anzahl_tipps * tipp_preis
st.markdown(f"💰 **Gesamtkosten:** {kosten:.2f} {waehrung}")

if st.button("🚀 Tipps generieren"):
    tipps = generiere_tipps(anzahl_tipps, history, ki_gewichtung, sim_stufen)
    for i, (zahlen, sterne) in enumerate(tipps, start=1):
        z = ", ".join(map(str, zahlen))
        s = " & ".join(map(str, sterne))
        st.success(f"Tipp {i}: {z} | Sterne: {s}")

    # CSV Export vorbereiten
    infozeile = f"# Modus: {modus} | KI: {ki_gewichtung}% | Simulationen: {sim_stufen} | Tipps: {anzahl_tipps} | Datum: {date.today()}"
    csv_output = StringIO()
    csv_output.write(infozeile + "\n")
    csv_output.write("Zahl 1,Zahl 2,Zahl 3,Zahl 4,Zahl 5,Stern 1,Stern 2\n")
    for zahlen, sterne in tipps:
        row = list(zahlen) + list(sterne)
        csv_output.write(",".join(map(str, row)) + "\n")
    st.download_button("⬇️ Tipps als CSV exportieren", csv_output.getvalue(), file_name="euromillions_tipps.csv", mime="text/csv")
