
import streamlit as st
from custom_style import eurogenius_css
import time

st.set_page_config(page_title="💎 EuroGenius Deluxe", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)

st.markdown("## 💎 Willkommen bei **EuroGenius Deluxe**")
st.markdown("### 🎰 Deine Lotto-Welt mit KI, Statistik und Intuition")

# Theme Header mit Icons
st.markdown("<div style='text-align:center; font-size:70px;'>🎲🎯🧠</div>", unsafe_allow_html=True)
st.markdown("---")

# Fortschrittsanzeige symbolisch
st.markdown("#### 🚀 Fortschritt")
st.progress(0.6)
st.info("🧩 Bronze-Level: 3 Strategien gespeichert")

# Strategie-Flow-Auswahl
st.markdown("### 🧠 Wähle deinen Spielmodus")
option = st.radio("Spielart wählen", ["🔥 Intuition", "📊 Statistik", "🤖 KI"], horizontal=True)

if option == "🔥 Intuition":
    st.markdown("💡 Lass dein Gefühl entscheiden – starte mit heißen Zahlen")
    if st.button("🎯 Jetzt starten"):
        st.success("🎉 Viel Glück! Deine Strategie wird geladen...")
        time.sleep(1)
        st.switch_page("pages/strategie.py")

elif option == "📊 Statistik":
    st.markdown("📈 Nutze Daten und Ziehungsstatistiken für deine Tipps")
    if st.button("📊 Daten entdecken"):
        st.success("📂 Strategien werden geladen...")
        time.sleep(1)
        st.switch_page("pages/meine_strategien.py")

elif option == "🤖 KI":
    st.markdown("🤖 Unsere KI analysiert Millionen von Ziehungen für deinen Tipp")
    if st.button("🧠 KI aktivieren"):
        st.success("🔎 Die KI denkt...")
        time.sleep(2)
        st.switch_page("pages/dashboard_demo.py")

st.markdown("---")

# Belohnungsinfo / Badges
st.markdown("#### 🎖️ Deine Belohnungen")
st.markdown("🔓 Bronze Badge: ✅ 3 Strategien gespeichert")
st.markdown("🔒 Silber Badge: ❌ 10 Strategien erforderlich")
st.markdown("🔒 Gold Badge: ❌ 30 Strategien erforderlich")

# Tipp: Login sichtbar
st.markdown("---")
st.warning("🔐 Logge dich ein, um deinen Fortschritt zu speichern & Premium-Funktionen zu nutzen!")
