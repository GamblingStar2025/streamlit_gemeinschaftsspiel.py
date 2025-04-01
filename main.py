
import streamlit as st
from datetime import date

st.set_page_config(page_title="EuroMillions App", layout="centered")

st.title("🎯 EuroMillions App")
st.markdown("Willkommen bei deiner intelligenten Tipp-App für EuroMillions!")

modus = st.radio("Spielmodus wählen", ["👤 Einzelspieler", "👥 Gemeinschaftsspiel"])
land = st.selectbox("Land", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇫🇷 Frankreich", "🇦🇹 Österreich"])
waehrung = "CHF" if "Schweiz" in land else "€"
preis = 3.5 if "Schweiz" in land else 2.5

anzahl = st.slider("Anzahl Tipps", 1, 50)
ki = st.slider("KI-Gewichtung", 0, 200, 100)
sim = st.slider("Simulationen", 10000, 1000000, 100000, step=10000)

st.write(f"💰 Preis: {anzahl * preis:.2f} {waehrung}")

if st.button("Tipps generieren"):
    st.success("Beispiel-Tipp: 4, 12, 25, 37, 49 ⭐ 3 & 8")
    st.info(f"KI: {ki}%, Simulationen: {sim}")

st.caption(f"© {date.today().year} EuroMillions")
