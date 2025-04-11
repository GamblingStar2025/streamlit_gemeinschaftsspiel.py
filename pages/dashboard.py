
import streamlit as st
from translations import get_translations

# ✅ Muss die allererste Streamlit-Funktion sein
st.set_page_config(page_title="EuroGenius", layout="centered")

# Sprache auswählen
lang = st.selectbox("🌐 Sprache / Language", ["de", "fr", "it", "en"], index=0)

# Nur setzen, wenn noch nicht vorhanden oder geändert
if st.session_state.get("lang") != lang:
    st.session_state["lang"] = lang

t = get_translations(st.session_state["lang"])

st.title(f"🎯 {t['welcome']}")
st.button(f"🚀 {t['start']}")

st.markdown("### 📊 EuroMillions")
st.success(f"{t['numbers']}: 5 - 23 - 28 - 44 - 48 ⭐ {t['stars']}: 2 - 8")
st.markdown(f"🤑 {t['jackpot']}: CHF 52.5 Mio")
