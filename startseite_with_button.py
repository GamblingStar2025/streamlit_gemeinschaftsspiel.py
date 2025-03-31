
import streamlit as st

st.set_page_config(page_title="EuroMillions KI-App", layout="wide")

st.markdown("<h1 style='font-size: 48px;'>🎯 Willkommen zur EuroMillions KI-App</h1>", unsafe_allow_html=True)
st.markdown("### Nutze Muster, Wahrscheinlichkeiten und Teamplay für bessere Tipps.")
st.markdown("")

st.markdown("""
    <style>
    .center-button button {
        display: block;
        margin: 2rem auto;
        padding: 1rem 2rem;
        font-size: 24px;
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# Session-State für Navigation
if 'page' not in st.session_state:
    st.session_state.page = 'start'

# Start-Button
if st.button("🚀 Jetzt starten", key="go_to_mode"):
    st.session_state.page = 'spielmodus'

# Navigation (einfaches Umschalten)
if st.session_state.page == 'spielmodus':
    st.switch_page("pages/spielmodus.py")  # Diese Datei muss existieren
