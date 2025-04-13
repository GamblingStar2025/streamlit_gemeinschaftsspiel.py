
import streamlit as st
from custom_style import eurogenius_css
from save_strategy import save_strategy

st.set_page_config(page_title="Strategie-Zentrale", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)
st.title("🧠 Strategie-Zentrale – Dein Lotto-Setup")

email = st.session_state.get("user_email", "gast@demo.com")

with st.expander("🔥 Heiße Zahlen", expanded=False):
    hot = st.slider("Anteil heiße Zahlen (%)", 0, 100, 60, key="hot_slider")
    if st.button("💾 Strategie speichern", key="save_hot"):
        res = save_strategy(email, "Heiße Zahlen", {"anteil": hot})
        st.success("✅ Strategie gespeichert.")

with st.expander("❄️ Kalte Zahlen", expanded=False):
    cold = st.slider("Anteil kalte Zahlen (%)", 0, 100, 30, key="cold_slider")
    if st.button("💾 Strategie speichern", key="save_cold"):
        res = save_strategy(email, "Kalte Zahlen", {"anteil": cold})
        st.success("✅ Strategie gespeichert.")

# andere Tabs wie vorher
