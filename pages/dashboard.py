
import streamlit as st
from translations import get_translations

# ✅ set_page_config MUSS zuerst aufgerufen werden
st.set_page_config(page_title="EuroGenius", layout="centered")

# Sprache wählen
lang = st.selectbox("🌐 Sprache / Language", ["de", "fr", "it", "en"], index=0)
st.session_state["lang"] = lang
t = get_translations(lang)

st.title(f"🎯 {t['welcome']}")
st.button(f"🚀 {t['start']}")

st.markdown("### 📊 EuroMillions")
st.success(f"{t['numbers']}: 5 - 23 - 28 - 44 - 48 ⭐ {t['stars']}: 2 - 8")
st.markdown(f"🤑 {t['jackpot']}: CHF 52.5 Mio")
