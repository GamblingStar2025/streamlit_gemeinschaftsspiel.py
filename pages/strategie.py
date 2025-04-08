
import streamlit as st

st.title("🎯 Strategie festlegen")

st.checkbox("🔁 Automatisch gewichten", value=False, key="automatisch")

if not st.session_state.automatisch:
    st.markdown("📊 Manuelle Methode-Gewichtungen (0–200%)")
    hot = st.slider("🔥 Hot/Cold", 0, 200, 100)
    cluster = st.slider("🧩 Cluster", 0, 200, 100)
    rad = st.slider("🔄 Rad-Prinzip", 0, 200, 100)
    mc = st.slider("🎲 Monte-Carlo", 0, 200, 100)
    ki = st.slider("🤖 KI-Einfluss", 0, 200, 100)

    if st.button("💾 Einstellungen speichern"):
        st.session_state["strategie"] = {
            "hot": hot,
            "cluster": cluster,
            "rad": rad,
            "mc": mc,
            "ki": ki
        }
        st.success("Strategie gespeichert!")

# Live-Vorschau anzeigen
strategie = st.session_state.get("strategie", None)
if strategie:
    st.markdown("✅ **Aktive Strategie-Einstellungen:**")
    st.json(strategie)
else:
    st.info("Noch keine Strategie gespeichert.")
