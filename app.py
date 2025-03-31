
import streamlit as st
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="EuroMillions Analyse", layout="wide")

# === Lokale Lottie-Animation ===
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_lotto = load_lottiefile("welcome_animation.json")

# === Intro ===
st.title("🎯 Willkommen zur EuroMillions KI-App")
st.subheader("Nutze Muster, Wahrscheinlichkeiten und Teamplay für bessere Tipps.")
st_lottie(lottie_lotto, height=300)
st.success("Starte dein Spiel oben über die Navigationsleiste! 🎮")
