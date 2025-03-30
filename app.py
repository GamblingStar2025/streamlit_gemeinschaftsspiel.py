from spielmodus import zeige_spielmodus
import streamlit as st
from streamlit_lottie import st_lottie
import json
import os

st.set_page_config(page_title="EuroMillions Analyse", layout="wide")

# === Lokale Lottie-Animation ===
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Sicherer relativer Pfad (funktioniert auch in Cloud)
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, "welcome_animation.json")
lottie_lotto = load_lottiefile(json_path)

# === Intro ===
st.title("🎯 Willkommen zur EuroMillions KI-App")
st.subheader("Nutze Muster, Wahrscheinlichkeiten und Teamplay für bessere Tipps.")
st_lottie(lottie_lotto, height=300)
st.success("Starte dein Spiel oben über die Navigationsleiste! 🎮")
