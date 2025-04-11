
import streamlit as st
from translations import get_translations

# Sprache wählen
lang = st.selectbox("🌐 Sprache / Language", ["de", "fr", "it", "en"], index=0)
st.session_state["lang"] = lang
t = get_translations(lang)

st.set_page_config(page_title="EuroGenius", layout="centered")

st.title(f"🎯 {t['welcome']}")
st.button(f"🚀 {t['start']}")

st.markdown("### 📊 EuroMillions")
st.success(f"{t['numbers']}: 5 - 23 - 28 - 44 - 48 ⭐ {t['stars']}: 2 - 8")
st.markdown(f"🤑 {t['jackpot']}: CHF 52.5 Mio")
