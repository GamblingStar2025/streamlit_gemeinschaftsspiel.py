
import streamlit as st

st.title("🎯 Strategie festlegen")

if not st.session_state.get("is_logged_in") or not st.session_state.get("is_premium"):
    st.warning("🔐 Nur für eingeloggte Premium-Nutzer verfügbar. Bitte zuerst einloggen unter: Login.")
    st.stop()

st.checkbox("🔁 Automatisch gewichten", value=False, key="automatisch")

if not st.session_state.automatisch:
    st.markdown("📊 Manuelle Methode-Gewichtungen (0–200%)")
    hot = st.slider("🔥 Hot/Cold", 0, 200, 100)
    cluster = st.slider("🧩 Cluster", 0, 200, 100)
    rad = st.slider("🔄 Rad-Prinzip", 0, 200, 100)
    mc = st.slider("🎲 Monte-Carlo", 0, 200, 100)
    ki = st.slider("🤖 KI-Einfluss", 0, 200, 100)

    if st.button("💾 Strategie speichern", use_container_width=True):
        st.session_state["strategie"] = {
            "hot": hot,
            "cluster": cluster,
            "rad": rad,
            "mc": mc,
            "ki": ki
        }
        st.success("✅ Strategie-Einstellungen gespeichert!")

strategie = st.session_state.get("strategie", None)
if strategie:
    st.markdown("✅ **Aktive Strategie-Einstellungen:**")
    st.json(strategie)

if st.button("➡️ Weiter zum Tippgenerator"):
    st.switch_page("pages/main_app.py")
