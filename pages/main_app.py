
import streamlit as st
import random
from custom_style import eurogenius_css

st.set_page_config(page_title="Tippgenerator", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)

if not st.session_state.get("is_logged_in") or st.session_state.get("rolle") != "premium":
    st.warning("🚫 Zugriff nur für eingeloggte Premium-Nutzer.")
    st.stop()

st.title("🎰 EuroGenius Tippgenerator")

anzahl = st.slider("Wie viele Tipps?", 1, 10, 3)
tipps = []

for _ in range(anzahl):
    zahlen = sorted(random.sample(range(1, 51), 5))
    sterne = sorted(random.sample(range(1, 13), 2))
    tipps.append((zahlen, sterne))

if st.button("💾 Tipp speichern"):
    st.success("✅ Tipps gespeichert!")

for idx, (z, s) in enumerate(tipps, 1):
    st.markdown(f"**Tipp {idx}:** {z} ⭐ {s}")
