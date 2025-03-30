
import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests

st.set_page_config(page_title="EuroMillions KI-Analyse", layout="wide")

# === Lottie Animation laden ===
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_lotto = load_lottieurl("https://lottie.host/3f3a44f6-7d5a-4ef1-974f-7b7299c4ed16/5lLu8DMCpa.json")

# === Intro ===
st.title("🎯 Willkommen zur EuroMillions KI-App")
st.subheader("Nutze Muster, Wahrscheinlichkeiten und Teamplay für bessere Tipps.")

st_lottie(lottie_lotto, height=300)

st.success("Starte dein Spiel oben über die Navigationsleiste! 🎮")
