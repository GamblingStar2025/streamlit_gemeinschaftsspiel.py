
import streamlit as st
from custom_style import eurogenius_css
import random
import time

st.set_page_config(page_title="🎮 Gamification", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)
st.title("🎮 Dein Fortschritt & Belohnungen")

# Fortschritt
saved_strategies = st.session_state.get("strategien_anzahl", 5)
max_badge = 30
progress = min(saved_strategies / max_badge, 1.0)

st.markdown("### 🏁 Fortschritt deiner Strategien")
st.progress(progress)
st.info(f"Du hast **{saved_strategies}** Strategien gespeichert")

# Badge-Anzeige
st.markdown("### 🎖️ Deine Badges")
if saved_strategies >= 30:
    st.success("🏆 Gold-Badge freigeschaltet!")
elif saved_strategies >= 10:
    st.success("🥈 Silber-Badge freigeschaltet!")
elif saved_strategies >= 5:
    st.success("🥉 Bronze-Badge freigeschaltet!")
else:
    st.warning("🔓 Noch keine Badges – speichere mehr Strategien!")

# 🎰 Zufallsgenerator mit Sound & Animation
st.markdown("---")
st.markdown("## 🎰 Glücks-Zahlen Generator")
if st.button("🔁 Jetzt drehen"):
    # Play sound via HTML
    st.markdown("""
        <audio autoplay>
            <source src="https://www.myinstants.com/media/sounds/slot-machine.mp3" type="audio/mpeg">
        </audio>
    """, unsafe_allow_html=True)
    st.markdown("🔄 Zahlen werden gemischt...")
    time.sleep(1.2)
    ziehung = sorted(random.sample(range(1, 51), 5))
    sterne = sorted(random.sample(range(1, 13), 2))
    st.success(f"🎯 Deine Zahlen: {ziehung} | ⭐ Sterne: {sterne}")
    st.balloons()
