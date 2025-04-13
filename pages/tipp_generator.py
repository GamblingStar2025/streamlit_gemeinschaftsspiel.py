
import streamlit as st
import random
import pandas as pd
from save_strategy import get_client
from collections import Counter

st.set_page_config(page_title="🎯 Tipp Generator", layout="centered")
st.title("🎯 Tipp Generator")

st.markdown("Wähle die Anzahl Tipps und deinen Einsatz pro Tipp:")

anzahl_tipps = st.number_input("Anzahl Tipps", min_value=1, max_value=20, value=5)
einsatz_pro_tipp = st.number_input("Einsatz pro Tipp (CHF)", min_value=0.5, max_value=10.0, value=2.50, step=0.50)

email = st.session_state.get("user_email", "gast@demo.com")

# Ziehungsdaten laden
@st.cache_data
def lade_haeufigkeit():
    df = pd.read_csv("EuroMillion_Ziehungen.csv")
    hauptzahlen_cols = [col for col in df.columns if "Hauptzahl" in col]
    haupt_counter = Counter()
    for col in hauptzahlen_cols:
        haupt_counter.update(df[col].dropna().astype(int).tolist())
    return dict(haupt_counter)

# Strategien laden
def lade_strategien(email):
    client = get_client()
    result = client.table("strategien").select("*").eq("email", email).execute()
    return result.data if result.data else []

# Gewichtete Tippgenerierung
def generiere_gewichteten_tipp(strategien, gewichtung):
    zahlen_pool = list(range(1, 51))
    stern_pool = list(range(1, 13))
    
    # Gewichtsliste basierend auf Ziehungen
    gewichte = [gewichtung.get(z, 1) for z in zahlen_pool]

    # Strategieanpassung: heiße Zahlen verstärken
    for strat in strategien:
        if strat["strategy_name"] == "Heiße Zahlen":
            anteil = strat["parameters"].get("anteil", 50)
            for i, z in enumerate(zahlen_pool):
                gewichte[i] *= (1 + anteil / 100)

    # Normierung und Auswahl
    hauptzahlen = sorted(random.choices(zahlen_pool, weights=gewichte, k=10))
    hauptzahlen = sorted(list(set(hauptzahlen)))[:5]
    sternzahlen = sorted(random.sample(stern_pool, 2))
    return hauptzahlen, sternzahlen

if st.button("🎟️ Tipp(s) generieren"):
    gesamt_einsatz = anzahl_tipps * einsatz_pro_tipp
    st.success(f"💰 Gesamteinsatz: {gesamt_einsatz:.2f} CHF")
    st.markdown("---")

    strategien = lade_strategien(email)
    gewichtung = lade_haeufigkeit()

    for i in range(anzahl_tipps):
        h, s = generiere_gewichteten_tipp(strategien, gewichtung)
        st.markdown(f"**Tipp {i+1}:** 🎯 Hauptzahlen: {h} ⭐️ Sterne: {s}")
