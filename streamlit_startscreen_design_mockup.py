
import streamlit as st
from streamlit_extras.emoji import emoji

st.set_page_config(page_title="Lotto Start", layout="centered")

# 🎨 Farbpsychologie-Farben
primary_color = "#6C2DC7"  # Violett – Fantasie, Magie
accent_color = "#FFD700"   # Gold – Gewinngefühl
background_color = "#1E1E2F"
text_color = "#FFFFFF"

st.markdown(f"""
    <style>
        .stApp {{
            background-color: {background_color};
            color: {text_color};
            font-family: 'Segoe UI', sans-serif;
        }}
        .title {{
            font-size: 3em;
            color: {accent_color};
            text-align: center;
            font-weight: bold;
        }}
        .subtitle {{
            font-size: 1.5em;
            text-align: center;
            color: #AAAAAA;
        }}
        .card {{
            background-color: #292941;
            border-radius: 20px;
            padding: 20px;
            margin: 10px;
            color: white;
            text-align: center;
            transition: 0.3s ease;
        }}
        .card:hover {{
            background-color: {primary_color};
            transform: scale(1.03);
            cursor: pointer;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎯 EuroMillions Spielstart</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Willkommen zurück! Wähle deinen Spielmodus:</div>', unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎮 Einzelspieler", use_container_width=True):
        st.success("Einzelspieler-Modus gewählt")
with col2:
    if st.button("👥 Gemeinschaft", use_container_width=True):
        st.success("Gemeinschaftsmodus gewählt")
with col3:
    if st.button("🤝 Team-Modus", use_container_width=True):
        st.success("Team-Modus gewählt")

st.markdown("---")
st.markdown('<div class="subtitle">🔐 Melde dich an oder erstelle dein Spielerprofil!</div>', unsafe_allow_html=True)
username = st.text_input("👤 Benutzername", placeholder="Dein Name hier")
if st.button("🚀 Loslegen"):
    if username:
        st.success(f"Willkommen {username}!")
    else:
        st.error("Bitte gib einen Benutzernamen ein.")
