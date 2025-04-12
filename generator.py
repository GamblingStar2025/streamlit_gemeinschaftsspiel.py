
import streamlit as st
import random

st.set_page_config(page_title="Tippgenerator", layout="centered")

st.title("🎰 Tippgenerator")

strategien = ["Zufall", "Hot/Cold", "Cluster", "Monte Carlo (simuliert)"]
strategie = st.selectbox("Strategie wählen", strategien)

gewichtung = st.slider("Gewichtung Heiß/Kalt", 0, 100, 50) if strategie == "Hot/Cold" else None

if st.button("Tipp generieren"):
    if strategie == "Zufall":
        zahlen = sorted(random.sample(range(1, 51), 5))
    elif strategie == "Hot/Cold":
        # Simulierte Heiß/Kalt-Logik
        hot = list(range(1, 21))
        cold = list(range(21, 51))
        hot_count = round(5 * (gewichtung / 100))
        cold_count = 5 - hot_count
        zahlen = sorted(random.sample(hot, hot_count) + random.sample(cold, cold_count))
    elif strategie == "Cluster":
        häufig = list(range(1, 18))
        mittel = list(range(18, 35))
        selten = list(range(35, 51))
        zahlen = sorted(random.sample(häufig, 2) + random.sample(mittel, 2) + random.sample(selten, 1))
    else:
        zahlen = sorted(random.choices(range(1, 51), k=5))  # Simulierte Monte-Carlo

    st.success(f"Dein Tipp: {zahlen}")
    if "email" in st.session_state:
        st.write(f"Eingeloggt als: {st.session_state['email']}")
        st.button("💾 Tipp speichern (Demo)")
    else:
        st.info("🔐 Bitte einloggen, um Tipp zu speichern.")
