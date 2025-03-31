
import streamlit as st
import datetime

# ==== Demo Ziehungsdaten ====
aktuelle_ziehung = {
    "datum": "Freitag, 29.03.2025",
    "hauptzahlen": [10, 21, 30, 42, 45],
    "sternzahlen": [1, 9],
    "gewinnstufen": {
        (5, 2): "Jackpot (ca. 100 Mio €)",
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

st.set_page_config(page_title="EuroMillions API-Demo", layout="centered")
st.title("🎯 Aktuelle EuroMillions Ziehung & Gewinnränge")

st.markdown(f"📅 **Ziehungsdatum**: {aktuelle_ziehung['datum']}")
st.markdown(f"🔢 **Hauptzahlen**: {', '.join(map(str, aktuelle_ziehung['hauptzahlen']))}")
st.markdown(f"🌟 **Sternzahlen**: {aktuelle_ziehung['sternzahlen'][0]} & {aktuelle_ziehung['sternzahlen'][1]}")

st.divider()
st.markdown("### 💰 Gewinnstufen (aktuell)")
for (zahlen, sterne), betrag in aktuelle_ziehung["gewinnstufen"].items():
    st.markdown(f"- **{zahlen} Zahlen + {sterne} Sterne** → {betrag}")

st.divider()
st.markdown("⏱️ Daten stammen aus API-Simulation – Integration für Live-Modus vorbereitet.")
