
import streamlit as st
from datetime import date
import random
import pandas as pd
from io import StringIO
from tippgenerator_module_fixed import generiere_tipps

# Beispiel-Ziehungshistorie (Demo)
history = [[random.randint(1, 50) for _ in range(5)] for _ in range(100)]

st.set_page_config(page_title="EuroMillions Tipps", layout="centered")
st.title("🎯 EuroMillions Tipp-Generator mit Auswertung")

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

tipps = []
if st.button("🚀 Tipps generieren"):
    tipps = generiere_tipps(anzahl_tipps, history, ki_gewichtung, sim_stufen)
    for i, (zahlen, sterne) in enumerate(tipps, start=1):
        z = ", ".join(map(str, zahlen))
        s = " & ".join(map(str, sterne))
        st.success(f"Tipp {i}: {z} | Sterne: {s}")

    # CSV Export
    infozeile = f"# Modus: {modus} | KI: {ki_gewichtung}% | Simulationen: {sim_stufen} | Tipps: {anzahl_tipps} | Datum: {date.today()}"
    csv_output = StringIO()
    csv_output.write(infozeile + "\n")
    csv_output.write("Zahl 1,Zahl 2,Zahl 3,Zahl 4,Zahl 5,Stern 1,Stern 2\n")
    for zahlen, sterne in tipps:
        row = list(zahlen) + list(sterne)
        csv_output.write(",".join(map(str, row)) + "\n")
    st.download_button("⬇️ Tipps als CSV exportieren", csv_output.getvalue(), file_name="euromillions_tipps.csv", mime="text/csv")

# === Gewinnprüfung ===
if tipps:
    st.subheader("🏁 Auswertung deiner Tipps")
    gezogene_zahlen = st.text_input("🔢 Aktuelle gezogene Zahlen (5 Zahlen, Komma getrennt)", "10,21,30,42,45")
    gezogene_sterne = st.text_input("🌟 Gezogene Sterne (2 Zahlen)", "1,9")

    try:
        gez_zahlen = set(map(int, gezogene_zahlen.split(",")))
        gez_sterne = set(map(int, gezogene_sterne.split(",")))

        def gewinnklasse(nr, s):
            komb = f"{nr}+{s}"
            tabelle = {
                "5+2": "Jackpot 💰", "5+1": "2. Rang", "5+0": "3. Rang",
                "4+2": "4. Rang", "4+1": "5. Rang", "4+0": "6. Rang",
                "3+2": "7. Rang", "2+2": "8. Rang", "3+1": "9. Rang",
                "3+0": "10. Rang", "1+2": "11. Rang", "2+1": "12. Rang", "2+0": "13. Rang"
            }
            return tabelle.get(komb, "–")

        total_gewinner = 0
        for i, (zahlen, sterne) in enumerate(tipps, start=1):
            n_treffer = len(set(zahlen).intersection(gez_zahlen))
            s_treffer = len(set(sterne).intersection(gez_sterne))
            klasse = gewinnklasse(n_treffer, s_treffer)
            if klasse != "–":
                total_gewinner += 1
                st.success(f"🏆 Tipp {i}: {n_treffer} Zahlen, {s_treffer} Sterne → **{klasse}**")
            else:
                st.info(f"Tipp {i}: {n_treffer} Zahlen, {s_treffer} Sterne → Kein Gewinn")
        st.markdown(f"🎉 **Treffer insgesamt:** {total_gewinner} / {len(tipps)}")

    except Exception as e:
        st.error("❌ Eingabeformat bitte prüfen (z. B. 10,21,30,42,45 und 1,9)")
