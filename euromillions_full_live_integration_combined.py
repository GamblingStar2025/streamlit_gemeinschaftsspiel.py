
import streamlit as st
from datetime import datetime, date, timedelta
from collections import Counter
import random

st.set_page_config(page_title="EuroMillions Live Analyse", layout="centered")

# === Ziehungstag-Prüfung ===
def letzter_ziehungstag():
    heute = date.today()
    if heute.weekday() == 1 or heute.weekday() == 4:  # Dienstag oder Freitag
        return heute
    elif heute.weekday() < 1:  # Montag oder Sonntag
        return heute - timedelta(days=(heute.weekday() + 3))
    else:
        offset = (heute.weekday() - 1) % 7
        return heute - timedelta(days=offset)

# === Simulierte API-Daten ===
def abrufen_ziehung_daten():
    return {
        "datum": str(letzter_ziehungstag()),
        "hauptzahlen": [10, 21, 30, 42, 45],
        "sternzahlen": [1, 9],
        "ränge": {
            (5, 2): "Jackpot (~€100 Mio)",
            (5, 1): "600.000 €",
            (5, 0): "80.000 €",
            (4, 2): "5.000 €",
            (4, 1): "300 €",
            (3, 2): "100 €",
            (2, 2): "20 €",
            (3, 1): "15 €",
            (3, 0): "10 €",
            (1, 2): "10 €",
            (2, 1): "8 €",
            (2, 0): "5 €"
        }
    }

# === Anzeige-Modul ===
def anzeigen_ziehung():
    daten = abrufen_ziehung_daten()
    st.markdown(f"### 🗓️ Aktuelle Ziehung vom **{daten['datum']}**")
    st.markdown(f"🔢 **Hauptzahlen**: {', '.join(map(str, daten['hauptzahlen']))}")
    st.markdown(f"🌟 **Sternzahlen**: {daten['sternzahlen'][0]} & {daten['sternzahlen'][1]}")
    st.markdown("---")
    st.markdown("### 💶 Gewinnränge:")
    for (z, s), betrag in daten["ränge"].items():
        st.markdown(f"- **{z} Zahlen + {s} Sterne** → {betrag}")
    return daten

# === Streamlit Navigation ===
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
